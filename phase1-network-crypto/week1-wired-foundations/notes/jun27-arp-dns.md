# ARP & DNS Deep Dive
**Studied:** June 27, 2026

---

## ARP

### Request/reply cycle — step by step

Your PC (192.168.1.10) wants to ping 192.168.1.20. It knows the IP but not the MAC address. Here's what happens:

1. PC checks its ARP cache: `arp -a` — is 192.168.1.20 already there? No.
2. PC broadcasts an ARP Request to **FF:FF:FF:FF:FF:FF** (every device on the LAN hears it).
   - Frame says: *"Who has 192.168.1.20? Tell 192.168.1.10 (AA:BB:CC:DD:EE:01)"*
3. Every device receives it. Only 192.168.1.20 responds.
4. 192.168.1.20 sends a unicast ARP Reply directly back to your PC:
   - *"192.168.1.20 is at AA:BB:CC:DD:EE:02"*
5. Your PC stores this in its ARP cache (typically for 2–20 minutes depending on the OS).
6. Now your PC wraps the ICMP ping in an Ethernet frame with the correct destination MAC and sends it.

**Key detail:** ARP is Layer 2. It runs *below* IP. Without ARP, IP packets can't leave your host on a local network segment.

---

### Gratuitous ARP — what it is

A gratuitous ARP is an ARP Reply that **nobody asked for**. A device announces its own IP→MAC mapping to the whole LAN without waiting for a request.

**Format:** Sender IP = Target IP = the device's own IP. Sent to broadcast.

**Legitimate uses:**
- When a NIC comes online — it announces itself so everyone updates their caches
- When an IP address changes — forces all neighbors to flush the old mapping
- High-availability failover (e.g. a backup router taking over an IP sends a GARP to redirect all traffic to its MAC)

**Why attackers love it:** Because ARP has **zero authentication**. Any device can send a gratuitous ARP claiming to be any IP. Victims accept it and update their cache without verification. This is the entry point for ARP cache poisoning.

---

### ARP cache poisoning — how it works

**Setup:** Victim A (192.168.1.10), Victim B (192.168.1.20), Attacker (192.168.1.99)

**Goal:** Attacker wants to intercept traffic between A and B (Man-in-the-Middle).

**Step by step:**

1. Attacker sends a spoofed ARP Reply to **Victim A**:
   - *"192.168.1.20 is at [Attacker's MAC]"*
   - Victim A updates its cache: now all traffic meant for B goes to the Attacker's MAC.

2. Attacker simultaneously sends a spoofed ARP Reply to **Victim B**:
   - *"192.168.1.10 is at [Attacker's MAC]"*
   - Victim B updates its cache: all traffic meant for A also goes to the Attacker.

3. Attacker enables IP forwarding on their machine — they relay packets between A and B so neither notices the connection is broken.

4. All traffic between A and B now flows through the Attacker. They can read, modify, or drop it.

**What Victim A's ARP cache looks like after the attack:**
```
192.168.1.20  →  AA:BB:CC:DD:EE:99   [Attacker's MAC — poisoned]
192.168.1.1   →  AA:BB:CC:DD:EE:01   [Gateway — still correct]
```

The cache shows the *correct IP* for B but the *wrong MAC* — the attacker's. Every packet A tries to send to B lands on the attacker's NIC first.

**How to defend:** Dynamic ARP Inspection (DAI) on managed switches — the switch validates ARP packets against a trusted DHCP binding table and drops gratuitous ARPs from untrusted ports.

```
[Victim A]                [Attacker]               [Victim B]
    |                         |                         |
    |<-- Spoofed ARP Reply ---|                         |
    |    "B is at Atk MAC"    |--- Spoofed ARP Reply -->|
    |                         |    "A is at Atk MAC"    |
    |                         |                         |
    |--- packet to "B" ------>|                         |
    |                         |--- relay to B --------->|
    |                         |<-- reply from B --------|
    |<-- relay to A ----------|                         |
    |         (Attacker reads/modifies everything)      |
```

---

## DNS

### Recursive vs iterative resolution

When you type `google.com` in your browser, here's what happens:

**Recursive (what your PC does — asks one resolver to do all the work):**

1. Your PC asks its configured **Recursive Resolver** (e.g. 8.8.8.8 — Google's DNS, or your ISP's resolver): *"What's the IP for google.com?"*
2. The Recursive Resolver does the full lookup on your behalf:
   a. Asks a **Root Nameserver** (`a.root-servers.net`): *"Who handles .com?"* → gets TLD nameserver address
   b. Asks the **.com TLD Nameserver**: *"Who handles google.com?"* → gets Google's authoritative NS
   c. Asks **Google's Authoritative Nameserver**: *"What's the A record for google.com?"* → gets `142.250.x.x`
3. Recursive Resolver caches the answer for the TTL duration, then returns the IP to your PC.
4. Your PC connects directly to `142.250.x.x`.

**Iterative (what resolvers do when talking to other nameservers):**
Each server says "I don't know, but ask *this* server next" — it gives you a referral rather than resolving fully. The resolver does the iteration itself.

**The key distinction:**
- Recursive: "Please do all the work for me" — used by end clients → resolver
- Iterative: "Tell me who to ask next" — used by resolvers → nameservers

---

### TTL — what it controls

TTL (Time to Live) in DNS is a field in each DNS record set by the zone owner (e.g. Google sets TTL on google.com's A record). It tells resolvers **how long to cache the answer** before they must query again.

- TTL = 300 → cache for 5 minutes
- TTL = 86400 → cache for 24 hours

**Why it matters for attacks:**
- High TTL → poisoned/stale records persist in caches for a long time. Once an attacker injects a forged record with a long TTL, victims keep using it without re-querying.
- Low TTL → caches expire quickly, reducing window for poisoning, but increases load on authoritative servers.

---

### DNS cache poisoning mechanics

**The goal:** Make a recursive resolver cache a forged IP address for a legitimate domain. Every client that asks the resolver for that domain gets the attacker's IP.

**Classic Kaminsky attack (2008):**

1. Attacker forces the resolver to make a new query — e.g. by requesting a random nonexistent subdomain like `xyz123.google.com` that isn't cached.
2. Resolver sends a UDP query to Google's authoritative NS, with a random **transaction ID** (16-bit number, 0–65535) in the packet.
3. **Race condition:** Attacker floods the resolver with thousands of forged UDP responses — each guessing a different transaction ID — before the real response arrives.
4. If one forged response with the correct transaction ID arrives first, the resolver accepts it and caches the attacker's IP for `google.com` (not just the subdomain — the attacker includes a fake "glue record" for the parent domain).
5. Now every client asking this resolver for `google.com` gets the attacker's IP.

**What makes this possible:** DNS over UDP has no authentication. Transaction IDs are only 16 bits (65,536 possibilities) — guessable by brute force in seconds with enough parallel attempts.

**Defense:** DNSSEC — adds cryptographic signatures to DNS records. The resolver verifies the signature against the zone's public key. A forged record without a valid signature is rejected. Also: DNS over TLS / DNS over HTTPS encrypts the query, making spoofing much harder.

---

## Self-check

**Draw the ARP poisoning attack from memory — which frames go where?**

```
Attacker sends (unsolicited):
  → To Victim A:  ARP Reply: "192.168.1.20 is at [Attacker MAC]"
  → To Victim B:  ARP Reply: "192.168.1.10 is at [Attacker MAC]"

Result — Victim A's ARP cache:
  192.168.1.20  →  [Attacker MAC]   ← POISONED

All A→B traffic now routes through Attacker first.
Attacker forwards it so neither victim notices.
```

---

## Thesis connection

**Which NSL-KDD features would change during an ARP or DNS attack?**

During an **ARP poisoning / MitM attack:**
- `dst_host_count` — the same destination (the real victim) will accumulate connections routed via the attacker, changing traffic patterns to that host
- `service` — the attacker may forward some services but block or modify others; sudden changes in service distribution per host pair
- `flag` — TCP flags in connections through the MitM may behave differently (RST storms, unexpected SYN patterns) if the attacker is selectively dropping traffic
- `src_bytes` / `dst_bytes` — traffic volumes change when packets are being intercepted and relayed (added latency, different byte counts)

During **DNS cache poisoning:**
- `service` — DNS queries are UDP port 53; a sudden spike in `dns` service entries could indicate flood-based poisoning attempts
- `dst_host_same_srv_rate` — if poisoning redirects many hosts to the same attacker IP, you'd see anomalous concentration of traffic to one destination across many source IPs
- `dst_host_srv_count` — the number of distinct services at the poisoned destination IP will look different from a legitimate web server

**The core insight:** ARP/DNS attacks manipulate Layer 2/3 addressing — but their *side effects* on traffic statistics (connection counts, service distributions, byte counts) are exactly what NSL-KDD features capture. Your CNN won't see the ARP frame directly — it will detect the *statistical anomaly signature* that the attack leaves behind.