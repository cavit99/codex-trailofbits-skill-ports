---
name: polymarket-api
description: Comprehensive routing and usage guidance for the Polymarket Gamma, Data, CLOB, Bridge, Relayer, WebSocket, and RTDS APIs. Use when Codex needs to choose the right Polymarket endpoint, understand CLOB L1/L2 authentication or signature types and funder rules, generate safe Polymarket request examples, work with official TypeScript/Python/Rust SDKs, or troubleshoot rate limits and geoblocking before trading workflows.
---

# Polymarket API

## Overview

Use this skill to decide which Polymarket API surface fits a task, then answer with the smallest safe interface: Gamma for discovery, Data for positions and analytics, CLOB for prices and trading, WebSocket or RTDS for streaming, Bridge for funding, and Relayer for gasless flows. Prefer the bundled helper for endpoint lookup and prefer official SDKs for authenticated CLOB work.

## Quick Routing

- Discovery, browsing, events, tags, comments, profiles, search: Gamma
- Positions, user trades, holders, open interest, leaderboards, builder analytics: Data
- Order books, spreads, prices, fee rate, tick size, live order entry, cancellations: CLOB
- Live market books and account/order events: CLOB WebSocket
- Live comments and crypto prices: RTDS
- Deposits, withdrawals, bridge quotes: Bridge
- Gasless transactions and relay state: Relayer

## Workflow

1. Classify the task by surface area first.
2. Use the helper to find the exact endpoint or channel:

```bash
scripts/polymarket_api.py recommend discover
scripts/polymarket_api.py search midpoint
scripts/polymarket_api.py show "GET /markets/{id}"
scripts/polymarket_api.py example "GET /book" --format curl
scripts/polymarket_api.py ws user
```

3. Open only the reference file you need:
   - `references/overview.md` for routing, auth, funder, rate limits, and geoblock checks
   - `references/rest-endpoints.md` for the human-readable REST index
   - `references/websocket.md` for market/user/sports/RTDS channel behavior
   - `references/sdk-clients.md` for official SDK package and repo guidance
   - `references/generated/endpoints.json` for machine-readable endpoint metadata
   - `references/specs/*.yaml` only when exact schema fields matter

4. For authenticated CLOB work, prefer the official clients over handwritten signing. Start from the auth and quickstart docs, then adapt with the helper’s SDK scaffold.
5. For live data, choose the correct socket before building polling loops. Market/user/sports and RTDS solve different problems.
6. When answering WebSocket questions, call out the channel-specific quirks explicitly: heartbeat direction, initial subscribe shape, and the condition-ID versus token-ID split.

## Guardrails

- Do not default to authenticated CLOB flows when a public Gamma, Data, or public CLOB read will do.
- Do not hand-roll L1 or L2 signatures unless the user explicitly needs raw HTTP details. Prefer official clients.
- Do not skip the geoblock check before order-entry guidance.
- Do not use RTDS as a substitute for order-book or order-entry data.
- Do not mix up market-channel token IDs with user-channel condition IDs.
- Do not assume all sockets use the same heartbeat or subscribe schema.
- Do not change the generated REST index or endpoint catalog by hand. Regenerate with `scripts/refresh_catalog.py`.
- Keep secrets server-side. Never emit code that hardcodes private keys, API secrets, or passphrases.
