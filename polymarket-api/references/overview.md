# Polymarket API Overview

This skill is built from the official Polymarket API docs and spec snapshots current as of March 10, 2026. Use the generated catalog for exact endpoint lookup and use this file for routing and guardrails.

## API Selection

- Gamma: discovery and browsing. Markets, events, tags, comments, series, profiles, sports metadata, and public search all live here.
- Data: account and analytics views. Positions, user trades, activity, holders, value, open interest, and builder/trader leaderboards live here.
- CLOB: tradable market state and trading. Order books, midpoint, prices, spreads, fee rates, tick sizes, history, orders, balances, allowances, and trade posting live here.
- Bridge: funding flows. Supported assets, quotes, deposits, withdrawals, and bridge status live here.
- Relayer: gasless transaction flows. Relay submission, transaction history, nonce checks, deployment checks, and relayer API keys live here.

## CLOB Authentication Model

- Public: Gamma, Data, Bridge, Relayer, and public CLOB read endpoints need no auth.
- L1: private-key auth for creating or deriving CLOB API credentials and for local order signing.
- L2: API-key auth for placing or canceling orders, reading open orders, checking balances and allowances, notifications, rewards, and related account flows.
- Prefer the official SDKs for both L1 and L2. The docs explicitly recommend the clients over raw REST signing.

## Signature Types and Funder

- `0` / `EOA`: standard wallet, funder is the wallet itself.
- `1` / `POLY_PROXY`: Magic-link or proxy-wallet flow. Use the proxy wallet as the funder.
- `2` / `GNOSIS_SAFE`: Safe-based proxy flow. Use the safe or profile address that actually holds funds.
- The funder is the address holding funds on Polymarket, not necessarily the signer key.

## Rate-Limit Cheat Sheet

- Global: `15,000` requests per 10 seconds across all APIs, with Cloudflare throttling on excess.
- Gamma general: `4,000` per 10 seconds. Hotter paths: `/events` `500`, `/markets` `300`, combined listing `900`, `/public-search` `350`.
- Data general: `1,000` per 10 seconds. `/trades` `200`, `/positions` and `/closed-positions` `150`.
- CLOB general: `9,000` per 10 seconds.
- CLOB market data: `/book`, `/price`, and `/midpoint` `1,500` per 10 seconds; `/books`, `/prices`, and `/midpoints` `500`; `/prices-history` `1,000`.
- CLOB trading burst limits: `POST /order` `3,500` per 10 seconds and `36,000` per 10 minutes; `DELETE /order` `3,000` per 10 seconds and `30,000` per 10 minutes.
- Relayer `/submit`: `25` per minute.
- When you are approaching limits, batch where possible, move to sockets for live feeds, and avoid unnecessary discovery polling.

## Geoblock Check

- Before order-entry guidance, check `https://polymarket.com/api/geoblock`.
- That endpoint lives on `polymarket.com`, not on Gamma or CLOB.
- A `blocked: true` response means do not place orders.
- The current docs explicitly list the United States and United Kingdom as blocked and also list some close-only countries or restricted subregions. Use the endpoint result rather than hardcoding jurisdiction logic.

## Working Defaults

- Start with Gamma when the user only knows a question, slug, event, or market theme.
- Switch to CLOB once you have exact market IDs, condition IDs, or token IDs and need tradable pricing or trading.
- Use Data when the user is asking about positions, holdings, trade history, or analytics rather than order entry.
- Use sockets instead of polling for live books, live user order updates, sports feeds, comments, or crypto-price streams.
- Keep signing and authenticated requests on the backend. The docs explicitly warn against exposing private keys or API secrets client-side.
