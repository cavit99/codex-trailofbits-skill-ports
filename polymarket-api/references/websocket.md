# Polymarket WebSocket and RTDS

Use this file for stream selection and payload shape. Use `scripts/polymarket_api.py ws <market|user|sports|rtds>` for a quick summary at the terminal.

## Channel Selection

- Market channel: live CLOB market data by token ID.
- User channel: authenticated account and order updates, optionally filtered by condition ID.
- Sports channel: sports feed updates from the sports socket.
- RTDS: comments and crypto-price streams. This is separate from the CLOB sockets.

## Oddities and Gotchas

- The channels do not share one subscription schema.
  - Market starts with `type: "market"` and later uses `operation`.
  - User starts with `type: "user"` plus `auth` and later uses `operation`.
  - RTDS uses `action: "subscribe"` and `action: "unsubscribe"` with a `subscriptions` array.
  - Sports does not publish a token- or market-filter subscription payload on the public page.
- Heartbeats differ by channel.
  - Market and user: client sends `PING` every 10 seconds and the server returns `PONG`.
  - Sports: server sends `ping` every 5 seconds and the client must respond with `pong` within 10 seconds.
  - RTDS: client sends `PING` every 5 seconds.
- ID semantics differ.
  - Market channel uses token IDs in `assets_ids`.
  - User channel filters by condition IDs in `markets`.
  - RTDS uses logical topics such as `comments`, `crypto_prices`, and `crypto_prices_chainlink`.
- Some market-channel events are opt-in.
  - `best_bid_ask`, `new_market`, and `market_resolved` require `custom_feature_enabled: true`.
- RTDS `filters` are topic-specific rather than globally typed.
  - Binance crypto-price examples use comma-delimited symbols.
  - Chainlink examples use a JSON-encoded string.

## CLOB Market Channel

- Endpoint: `wss://ws-subscriptions-clob.polymarket.com/ws/market`
- Auth: none
- Primary ID: `assets_ids` are token IDs
- Initial subscribe oddities:
  - `type` must be `"market"`
  - `initial_dump` is optional and defaults to `true`
  - `level` is optional and defaults to `2`
  - `custom_feature_enabled` is optional but required for custom-feature events
- Subscribe:

```json
{
  "type": "market",
  "assets_ids": ["TOKEN_ID"],
  "initial_dump": true,
  "level": 2
}
```

- Update without reconnecting:

```json
{
  "operation": "subscribe",
  "assets_ids": ["TOKEN_ID"]
}
```

- Unsubscribe:

```json
{
  "operation": "unsubscribe",
  "assets_ids": ["TOKEN_ID"]
}
```

- Heartbeat: follow the documented ping/pong keepalive for market/user channels and keep a 10-second heartbeat cadence.
- Common event types:
  - `book`
  - `price_change`
  - `tick_size_change`
  - `last_trade_price`
  - `best_bid_ask`, `new_market`, `market_resolved` only when `custom_feature_enabled: true`

## CLOB User Channel

- Endpoint: `wss://ws-subscriptions-clob.polymarket.com/ws/user`
- Auth: CLOB API key credentials required
- Primary ID: optional `markets` filters use condition IDs
- Important oddity: these `markets` are condition IDs, not the YES/NO token IDs used by the market channel.
- Initial authenticated subscribe:

```json
{
  "auth": {
    "apiKey": "your-api-key-uuid",
    "secret": "your-api-secret",
    "passphrase": "your-passphrase"
  },
  "type": "user",
  "markets": ["CONDITION_ID"]
}
```

- If `markets` is omitted in the initial subscribe, the docs say the channel streams all markets for the account.
- Optional market filter update:

```json
{
  "operation": "subscribe",
  "markets": ["CONDITION_ID"]
}
```

- Unsubscribe:

```json
{
  "operation": "unsubscribe",
  "markets": ["CONDITION_ID"]
}
```

- Heartbeat: same keepalive pattern as the market channel.

## Sports Channel

- Endpoint: `wss://sports-api.polymarket.com/ws`
- Auth: none
- Subscription payload: none documented on the public sports channel page
- Heartbeat: respond to server `ping` with `pong` within 10 seconds
- The docs describe the server heartbeat as arriving every 5 seconds.
- Use this for sports feed updates, not for CLOB order books or order entry.
- Example payloads are scoreboard-style updates with fields like `slug`, `live`, `ended`, `score`, `period`, `elapsed`, and `last_update`.

## RTDS

- Endpoint: `wss://ws-live-data.polymarket.com`
- Auth: public for many streams, optional `gamma_auth.address` for some user-specific streams
- Heartbeat: send `PING` every 5 seconds
- Subscription updates can be changed without reconnecting
- Unsubscribe by sending the same payload with `"action": "unsubscribe"`
- Common message envelope fields:
  - `topic`
  - `type`
  - `timestamp`
  - `payload`
- Comment event types documented on the page:
  - `comment_created`
  - `comment_removed`
  - `reaction_created`
  - `reaction_removed`

### RTDS Comments Example

```json
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "comments",
      "type": "comment_created",
      "gamma_auth": {
        "address": "WALLET_ADDRESS"
      }
    }
  ]
}
```

### RTDS Crypto Prices Example

```json
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices",
      "type": "update",
      "filters": "solusdt,btcusdt"
    }
  ]
}
```

### RTDS Chainlink Prices Example

```json
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices_chainlink",
      "type": "*",
      "filters": "{\"symbol\":\"eth/usd\"}"
    }
  ]
}
```

## When Not To Use These Streams

- Do not use RTDS for order books, live orders, or placing trades.
- Do not use market/user sockets for comments or crypto-price side channels.
- Do not use the sports socket as a substitute for Gamma market discovery.
- Do not mix up condition IDs and token IDs when switching between the user and market channels.
