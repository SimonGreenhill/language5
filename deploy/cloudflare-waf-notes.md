# Cloudflare edge mitigation (preferred) — crawler-trap swarm

Logs show `cdn-cgi/challenge-platform` referrers, so Cloudflare is at least
partly in front of the site. Cloudflare is the **preferred** place to stop the
25,945-IP fake-`Chrome/145.0.0.0` swarm because it can JS/managed-challenge the
fake-UA bots **without blocking real users**, and before traffic ever reaches
the origin `:3298`.

## 0. Confirm CF is actually in front of origin
- In the Cloudflare dashboard, check the DNS records for `transnewguinea.org` /
  `tng.simon.net.nz` are **proxied** (orange cloud), not DNS-only (grey).
- On the origin, check whether inbound IPs are Cloudflare ranges or raw client
  IPs: `awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head`.
  If you see raw client IPs (not CF ranges), some/all traffic is bypassing CF —
  lock the origin firewall to only accept from Cloudflare IP ranges, otherwise
  the swarm just hits nginx directly (that's what `deploy/nginx-crawler-trap.conf`
  is for).

## 1. WAF custom rule — challenge the query-param crawl space
Security → WAF → Custom rules. Create a rule:

- **Expression:**
  ```
  (http.request.uri.query contains "sort=" or http.request.uri.query contains "page=")
  and not cf.client.bot            # let verified good bots (Googlebot/Bingbot) through
  ```
- **Action:** `Managed Challenge` (start here) — humans pass transparently, the
  headless swarm fails. Escalate to `JS Challenge` / `Block` only if needed.

`cf.client.bot` is Cloudflare's verified-bot signal (validated by rDNS/ASN), so
this does **not** rely on the spoofable User-Agent string.

## 2. Bot Fight Mode (quick, coarse)
Security → Bots → enable **Bot Fight Mode** (or Super Bot Fight Mode on paid
plans, which lets you specifically challenge "Definitely automated" traffic).
This challenges obvious automation network-wide. Cheaper to enable but less
targeted than the custom rule above; use both.

## 3. Rate limiting rule (belt-and-suspenders)
Security → WAF → Rate limiting rules:
- Match: same list paths (`/language*`, `/word*`, `/source*`, `/family*`,
  `/cognacy*`).
- Threshold: e.g. > 20 requests / 10s per IP → Managed Challenge.
- Tune against real traffic first.

## Constraints (from fix.md)
- **Do NOT block Googlebot/Bingbot.** `not cf.client.bot` already exempts
  verified crawlers; never block on UA alone (verify by rDNS/ASN).
- **Roll out in challenge mode first**, watch the WAF events for false positives
  on real users, then tighten to Block if the challenge isn't enough.
- Keep it reversible — WAF rules can be disabled instantly from the dashboard.

## Verify after enabling
- Security → Events: confirm the challenged/blocked traffic is the fake-UA swarm
  hitting `?sort=`/`?page=`, not real users.
- Re-check origin nginx logs: 499/502/504 on the list paths should drop sharply
  and upstream `:3298` should stop timing out.
