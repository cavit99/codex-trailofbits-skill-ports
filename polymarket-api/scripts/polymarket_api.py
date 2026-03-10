#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

CATALOG_PATH = Path(__file__).resolve().parents[1] / "references" / "generated" / "endpoints.json"

OFFICIAL_LINKS = {
    "api_intro": "https://docs.polymarket.com/api-reference/introduction",
    "authentication": "https://docs.polymarket.com/api-reference/authentication",
    "rate_limits": "https://docs.polymarket.com/api-reference/rate-limits",
    "geoblock": "https://docs.polymarket.com/api-reference/geoblock",
    "clients": "https://docs.polymarket.com/api-reference/clients-sdks",
    "first_order": "https://docs.polymarket.com/quickstart/first-order",
    "py_clob_client": "https://github.com/Polymarket/py-clob-client",
    "ts_clob_client": "https://github.com/Polymarket/clob-client",
    "py_builder_client": "https://github.com/Polymarket/py-builder-signing-sdk",
    "ts_builder_client": "https://github.com/Polymarket/builder-signing-sdk",
    "py_relayer_client": "https://github.com/Polymarket/py-builder-relayer-client",
    "ts_relayer_client": "https://github.com/Polymarket/builder-relayer-client",
}

WS_CHANNELS: dict[str, dict[str, Any]] = {
    "market": {
        "title": "CLOB Market Channel",
        "endpoint": "wss://ws-subscriptions-clob.polymarket.com/ws/market",
        "auth": "public",
        "docs": "https://docs.polymarket.com/api-reference/wss/market",
        "subscribe": {
            "type": "market",
            "assets_ids": ["TOKEN_ID"],
        },
        "update_subscription": {
            "operation": "subscribe",
            "assets_ids": ["TOKEN_ID"],
        },
        "unsubscribe": {
            "operation": "unsubscribe",
            "assets_ids": ["TOKEN_ID"],
        },
        "heartbeat": (
            "Use the documented ping/pong heartbeat. The WebSocket overview recommends "
            "sending keepalives every 10 seconds for market/user channels."
        ),
        "ids": "Use ERC-1155 token IDs in `assets_ids`.",
        "notes": "Stream live books, price changes, and last-trade events per token.",
        "event_types": [
            "book",
            "price_change",
            "tick_size_change",
            "last_trade_price",
            "best_bid_ask (custom feature)",
            "new_market (custom feature)",
            "market_resolved (custom feature)",
        ],
        "quirks": [
            "Initial subscribe uses `type: \"market\"`; dynamic add/remove uses `operation: \"subscribe\"` or `\"unsubscribe\"`.",
            "`assets_ids` are token IDs, not condition IDs.",
            "Initial subscribe supports `initial_dump` and `level`; docs say `initial_dump` defaults to true and `level` defaults to 2.",
            "`best_bid_ask`, `new_market`, and `market_resolved` require `custom_feature_enabled: true` on the subscription.",
        ],
    },
    "user": {
        "title": "CLOB User Channel",
        "endpoint": "wss://ws-subscriptions-clob.polymarket.com/ws/user",
        "auth": "l2",
        "docs": "https://docs.polymarket.com/api-reference/wss/user",
        "subscribe": {
            "auth": {
                "apiKey": "your-api-key-uuid",
                "secret": "your-api-secret",
                "passphrase": "your-passphrase",
            },
            "type": "user",
        },
        "update_subscription": {
            "operation": "subscribe",
            "markets": ["CONDITION_ID"],
        },
        "unsubscribe": {
            "operation": "unsubscribe",
            "markets": ["CONDITION_ID"],
        },
        "heartbeat": (
            "Use the documented ping/pong heartbeat. The WebSocket overview recommends "
            "sending keepalives every 10 seconds for market/user channels."
        ),
        "ids": "Authenticate with CLOB API creds; optional `markets` filters use condition IDs.",
        "notes": "Use this for order lifecycle, fills, cancels, and account-specific trade updates.",
        "quirks": [
            "The first message is an authenticated subscribe payload with `auth` plus `type: \"user\"`; it is not an `operation` payload.",
            "`markets` are condition IDs, not token IDs. The docs call this out explicitly.",
            "If `markets` is omitted on the initial subscribe, the socket streams events for all markets visible to the account.",
            "Only the initial subscribe carries API credentials; later subscribe/unsubscribe updates just carry `operation` plus `markets`.",
        ],
    },
    "sports": {
        "title": "Sports WebSocket",
        "endpoint": "wss://sports-api.polymarket.com/ws",
        "auth": "public",
        "docs": "https://docs.polymarket.com/api-reference/wss/sports",
        "subscribe": None,
        "unsubscribe": None,
        "heartbeat": "Respond to server `ping` messages with `pong` within 10 seconds.",
        "ids": "No subscription payload is documented; connect and consume sports feed updates directly.",
        "notes": "Use this for sports schedule, game-state, and score feed updates.",
        "event_types": ["sports result / game-state updates"],
        "quirks": [
            "Heartbeat direction is reversed versus market/user: the server sends `ping` every 5 seconds and the client must answer with `pong` within 10 seconds.",
            "The public sports page does not document a subscribe payload; treat it as a feed you connect to rather than a token-filtered subscription.",
            "Example payloads are scoreboard-style objects with fields like `slug`, `live`, `ended`, `score`, `period`, `elapsed`, and `last_update`.",
        ],
    },
    "rtds": {
        "title": "Real-Time Data Socket",
        "endpoint": "wss://ws-live-data.polymarket.com",
        "auth": "optional",
        "docs": "https://docs.polymarket.com/market-data/websocket/rtds",
        "subscribe": {
            "action": "subscribe",
            "subscriptions": [
                {
                    "topic": "comments",
                    "type": "comment_created",
                }
            ],
        },
        "unsubscribe": {
            "action": "unsubscribe",
            "subscriptions": [
                {
                    "topic": "comments",
                    "type": "comment_created",
                }
            ],
        },
        "heartbeat": "Send `PING` every 5 seconds. Some user-specific streams require `gamma_auth.address`.",
        "ids": (
            "RTDS subscription topics are logical topics such as `comments`, `crypto_prices`, "
            "and `crypto_prices_chainlink` rather than token IDs."
        ),
        "notes": "Use RTDS for comments and crypto-price streams, not for CLOB order placement or books.",
        "event_types": [
            "comments: comment_created, comment_removed, reaction_created, reaction_removed",
            "crypto prices: update",
        ],
        "quirks": [
            "RTDS uses `action: \"subscribe\"` / `\"unsubscribe\"`, not the `type` or `operation` fields used by the CLOB sockets.",
            "Subscriptions live inside a `subscriptions` array and can be added, removed, or modified without reconnecting.",
            "Filter semantics vary by topic: Binance crypto prices use a comma-delimited string like `solusdt,btcusdt`, while Chainlink examples use a JSON-encoded string payload.",
            "The common RTDS message envelope includes `topic`, `type`, `timestamp`, and `payload`.",
            "Some user-specific streams require `gamma_auth.address`; public topics do not.",
        ],
        "examples": [
            {
                "label": "Crypto prices (Binance source)",
                "payload": {
                    "action": "subscribe",
                    "subscriptions": [
                        {
                            "topic": "crypto_prices",
                            "type": "update",
                            "filters": "solusdt,btcusdt",
                        }
                    ],
                },
            },
            {
                "label": "Crypto prices (Chainlink source)",
                "payload": {
                    "action": "subscribe",
                    "subscriptions": [
                        {
                            "topic": "crypto_prices_chainlink",
                            "type": "*",
                            "filters": '{"symbol":"eth/usd"}',
                        }
                    ],
                },
            },
            {
                "label": "Comments with optional Gamma auth",
                "payload": {
                    "action": "subscribe",
                    "subscriptions": [
                        {
                            "topic": "comments",
                            "type": "comment_created",
                            "gamma_auth": {"address": "WALLET_ADDRESS"},
                        }
                    ],
                },
            },
        ],
    },
}

RECOMMENDATIONS: dict[str, dict[str, Any]] = {
    "discover": {
        "use": "Gamma first",
        "services": ["gamma"],
        "why": "Gamma is the browsing/discovery surface for markets, events, tags, comments, series, and public search.",
        "start": ["GET /public-search", "GET /markets", "GET /events"],
        "caution": "Do not use CLOB or Data as your primary market-discovery layer unless you already have exact market IDs or token IDs.",
        "docs": [OFFICIAL_LINKS["api_intro"]],
    },
    "prices": {
        "use": "CLOB market data",
        "services": ["clob"],
        "why": "CLOB exposes tradable order books, prices, spreads, fee rates, tick sizes, and history.",
        "start": ["GET /book", "GET /midpoint", "GET /price", "GET /prices-history"],
        "caution": "Use Gamma for rich metadata; use market WebSocket when polling is too slow.",
        "docs": ["https://docs.polymarket.com/api-reference/market-data/get-order-book"],
    },
    "positions": {
        "use": "Data API",
        "services": ["data"],
        "why": "Data API is the account/analytics surface for positions, user trades, value, holders, open interest, and activity.",
        "start": ["GET /positions", "GET /trades", "GET /activity", "GET /oi"],
        "caution": "Data API is not the order-entry surface and does not replace CLOB auth flows.",
        "docs": ["https://docs.polymarket.com/api-reference/core/get-current-positions-for-a-user"],
    },
    "trade": {
        "use": "Authenticated CLOB + SDK",
        "services": ["clob"],
        "why": "Orders, cancels, allowances, rewards, notifications, and account trade state live behind CLOB authentication.",
        "start": ["POST /order", "DELETE /order", "GET /orders", "GET /balance-allowance"],
        "caution": (
            "Check geoblock eligibility first, choose the right signature type/funder, derive API creds, "
            "and prefer the official clients over raw signed HTTP."
        ),
        "docs": [OFFICIAL_LINKS["authentication"], OFFICIAL_LINKS["geoblock"], OFFICIAL_LINKS["first_order"]],
    },
    "streaming": {
        "use": "Pick the socket by payload type",
        "services": ["clob", "gamma"],
        "why": "Market/user/sports WebSocket handle exchange and sports feed updates; RTDS handles comments and crypto prices.",
        "start": ["market", "user", "sports", "rtds"],
        "caution": "Do not expect RTDS to expose books or order entry. Do not expect market/user WebSocket to expose comments.",
        "docs": [
            "https://docs.polymarket.com/developers/CLOB/websocket/wss-overview",
            "https://docs.polymarket.com/market-data/websocket/rtds",
        ],
    },
    "comments": {
        "use": "Gamma comments or RTDS comments",
        "services": ["gamma"],
        "why": "Use Gamma REST for comment fetches and RTDS for live comment events.",
        "start": ["GET /comments", "GET /comments/{id}", "rtds"],
        "caution": "RTDS comment streams may require `gamma_auth` for some user-specific views.",
        "docs": [
            "https://docs.polymarket.com/api-reference/comments/list-comments",
            "https://docs.polymarket.com/market-data/websocket/rtds",
        ],
    },
    "funding": {
        "use": "Bridge API",
        "services": ["bridge"],
        "why": "Bridge handles supported assets, quotes, deposit addresses, withdrawals, and status checks.",
        "start": ["GET /supported-assets", "POST /quote", "POST /deposit", "POST /withdraw"],
        "caution": "Bridge is not Polymarket market data or CLOB trading. It proxies funding flows.",
        "docs": ["https://docs.polymarket.com/api-reference/bridge/get-supported-assets"],
    },
    "gasless": {
        "use": "Relayer + builder tooling",
        "services": ["relayer"],
        "why": "Relayer is the gasless transaction surface for submit/nonce/status flows and builder relayer API keys.",
        "start": ["POST /submit", "GET /nonce", "GET /transactions", "GET /relayer/api/keys"],
        "caution": "Use this only for relay/gasless transaction flows, not normal CLOB order entry.",
        "docs": ["https://docs.polymarket.com/api-reference/relayer/submit-a-transaction"],
    },
}


def load_catalog() -> list[dict[str, Any]]:
    if not CATALOG_PATH.exists():
        raise SystemExit(
            f"Catalog not found at {CATALOG_PATH}.\n"
            "Run `uv run --with pyyaml python scripts/refresh_catalog.py` first."
        )
    return json.loads(CATALOG_PATH.read_text())


def normalize_identifier(parts: list[str]) -> str:
    return " ".join(part.strip() for part in parts).strip()


def placeholder_name(name: str) -> str:
    snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    snake = re.sub(r"[^A-Za-z0-9]+", "_", snake).strip("_")
    return snake.upper() or "VALUE"


def placeholder_value(parameter: dict[str, Any]) -> str:
    type_name = str(parameter.get("type") or "")
    name = str(parameter.get("name") or "value")
    if type_name.startswith("array"):
        return f"{placeholder_name(name)}_1,{placeholder_name(name)}_2"
    if type_name in {"integer", "number"}:
        return "1"
    if type_name == "boolean":
        return "true"
    return placeholder_name(name)


def fill_path_template(entry: dict[str, Any]) -> str:
    path = entry["path"]
    for parameter in entry.get("path_params", []):
        path = path.replace("{" + parameter["name"] + "}", placeholder_value(parameter))
    return path


def build_query_params(entry: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
    required: dict[str, str] = {}
    optional: dict[str, str] = {}
    for parameter in entry.get("query_params", []):
        value = placeholder_value(parameter)
        target = required if parameter.get("required") else optional
        target[parameter["name"]] = value
    return required, optional


def operation_key(entry: dict[str, Any]) -> str:
    return f"{entry['method']} {entry['path']}"


def score_entry(entry: dict[str, Any], query: str) -> int:
    haystacks = {
        "summary": f"{entry['summary']} {entry.get('description', '')}".lower(),
        "path": entry["path"].lower(),
        "operation_id": str(entry["operation_id"]).lower(),
        "tags": " ".join(entry.get("tags", [])).lower(),
        "service": entry["service"].lower(),
    }
    query_tokens = [token for token in re.split(r"\s+", query.lower()) if token]
    if not query_tokens:
        return 0
    score = 0
    for token in query_tokens:
        if token in haystacks["operation_id"]:
            score += 6
        if token in haystacks["path"]:
            score += 5
        if token in haystacks["summary"]:
            score += 3
        if token in haystacks["tags"]:
            score += 2
        if token == haystacks["service"]:
            score += 2
    joined = " ".join(haystacks.values())
    if query.lower() in joined:
        score += 6
    return score


def resolve_entry(entries: list[dict[str, Any]], raw_identifier: str) -> dict[str, Any]:
    method_path = re.match(r"^(GET|POST|PUT|DELETE|PATCH)\s+(/.+)$", raw_identifier, re.IGNORECASE)
    if method_path:
        method = method_path.group(1).upper()
        path = method_path.group(2)
        for entry in entries:
            if entry["method"] == method and entry["path"] == path:
                return entry
    lowered = raw_identifier.lower()
    exact_operation = [entry for entry in entries if str(entry["operation_id"]).lower() == lowered]
    if len(exact_operation) == 1:
        return exact_operation[0]
    exact_path = [entry for entry in entries if entry["path"].lower() == lowered]
    if len(exact_path) == 1:
        return exact_path[0]
    raise SystemExit(f"Could not resolve endpoint identifier: {raw_identifier}")


def usage_guidance(entry: dict[str, Any]) -> tuple[str, str]:
    service = entry["service"]
    auth_level = entry["auth_level"]
    path = entry["path"]
    if service == "gamma":
        return (
            "Use this for discovery, metadata, events, tags, comments, profiles, and public search.",
            "Do not use Gamma for order placement, authenticated portfolio data, or live tradable order books.",
        )
    if service == "data":
        return (
            "Use this for positions, user trades, holders, open interest, activity, value, and builder analytics.",
            "Do not use Data API for placing or canceling orders or for full discovery-style metadata browsing.",
        )
    if service == "bridge":
        return (
            "Use this for funding flows: supported assets, quotes, deposit addresses, withdrawals, and bridge status.",
            "Do not use Bridge for market discovery, books, prices, or order entry.",
        )
    if service == "relayer":
        return (
            "Use this for gasless/relay transaction flows, relay payloads, nonce checks, and relayer API key management.",
            "Do not use Relayer for ordinary CLOB order entry unless you are explicitly implementing relay-based flows.",
        )
    if auth_level in {"l1", "l2"}:
        return (
            "Use this when you already know you need authenticated CLOB behavior and have the correct wallet, signature type, and funder setup.",
            "Do not call authenticated CLOB endpoints raw unless you understand L1/L2 auth, geoblock limits, and allowance requirements.",
        )
    if any(token in path for token in ["/book", "/price", "/spread", "/midpoint", "/prices-history"]):
        return (
            "Use this for tradable pricing and order-book state straight from CLOB.",
            "Do not use this as your primary discovery surface; start from Gamma when you need richer market metadata.",
        )
    return (
        "Use this for public CLOB market-state reads when you already have the relevant market or token IDs.",
        "Do not use public CLOB endpoints when you need discovery, comments, or account-level portfolio analytics.",
    )


def render_json(payload: Any) -> str:
    return json.dumps(payload, indent=2)


def print_search(entries: list[dict[str, Any]], query: str, service: str | None, auth: str | None, limit: int) -> None:
    matches: list[tuple[int, dict[str, Any]]] = []
    for entry in entries:
        if service and entry["service"] != service:
            continue
        if auth and entry["auth_level"] != auth:
            continue
        score = score_entry(entry, query)
        if score > 0:
            matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1]["service"], item[1]["path"], item[1]["method"]))
    if not matches:
        raise SystemExit("No matching endpoints found.")
    for _, entry in matches[:limit]:
        print(
            f"{operation_key(entry)} [{entry['service']} {entry['auth_level']}] "
            f"{entry['summary']} ({entry['operation_id']})"
        )


def print_show(entry: dict[str, Any]) -> None:
    when_to_use, when_not_to_use = usage_guidance(entry)
    print(f"{operation_key(entry)}")
    print(f"Service: {entry['service_label']} ({entry['service']})")
    print(f"Summary: {entry['summary'] or '-'}")
    print(f"Auth: {entry['auth_level']}")
    print(f"SDK preference: {entry['sdk_preference']}")
    print(f"Server: {entry['server']}")
    print(f"Operation ID: {entry['operation_id']}")
    print(f"Tags: {', '.join(entry.get('tags') or []) or '-'}")
    print(f"Docs: {entry['doc_url']}")
    if entry.get("query_params"):
        names = ", ".join(
            f"{param['name']}{' (required)' if param['required'] else ''}"
            for param in entry["query_params"]
        )
        print(f"Query params: {names}")
    if entry.get("path_params"):
        names = ", ".join(param["name"] for param in entry["path_params"])
        print(f"Path params: {names}")
    if entry.get("request_body"):
        body = entry["request_body"]
        print(
            "Request body: "
            f"required={body['required']} content_types={', '.join(body.get('content_types') or []) or '-'}"
        )
    print(f"When to use: {when_to_use}")
    print(f"When not to use: {when_not_to_use}")


def render_public_get_example(entry: dict[str, Any], output_format: str) -> str:
    path = fill_path_template(entry)
    required_query, optional_query = build_query_params(entry)
    base_url = f"{entry['server']}{path}"
    query_suffix = f"?{urlencode(required_query)}" if required_query else ""
    url = f"{base_url}{query_suffix}"
    optional_note = ""
    if optional_query:
        optional_note = "# Optional query params: " + ", ".join(
            f"{name}={value}" for name, value in optional_query.items()
        )

    if output_format == "curl":
        lines = [
            "curl -s \\",
            "  -H 'Accept: application/json' \\",
            f"  \"{url}\"",
        ]
        if optional_note:
            lines.append(optional_note)
        return "\n".join(lines)

    if output_format == "python":
        query_block = (
            "params = " + repr(required_query) + "\n"
            "url = f\"{base_url}?{urlencode(params)}\""
            if required_query
            else "url = base_url"
        )
        optional_block = ""
        if optional_note:
            optional_block = f"\n# Optional query params: {', '.join(optional_query)}"
        return textwrap.dedent(
            f"""\
            from urllib.parse import urlencode
            from urllib.request import Request, urlopen

            base_url = "{base_url}"
            {query_block}
            request = Request(url, headers={{"Accept": "application/json"}})

            with urlopen(request, timeout=30) as response:
                print(response.read().decode("utf-8"))
            {optional_block}
            """
        ).strip()

    if output_format == "ts":
        params_block = (
            f"const params = new URLSearchParams({json.dumps(required_query)});"
            "\nconst url = `${baseUrl}?${params.toString()}`;"
            if required_query
            else "const url = baseUrl;"
        )
        optional_block = ""
        if optional_note:
            optional_block = f"\n// Optional query params: {', '.join(optional_query)}"
        return textwrap.dedent(
            f"""\
            const baseUrl = "{base_url}";
            {params_block}

            const response = await fetch(url, {{
              headers: {{ Accept: "application/json" }},
            }});

            console.log(await response.json());
            {optional_block}
            """
        ).strip()

    raise SystemExit(f"Unsupported format: {output_format}")


def render_generic_authenticated_example(entry: dict[str, Any], output_format: str) -> str:
    docs = entry["doc_url"]
    if entry["sdk_preference"] == "official-builder-sdk":
        return textwrap.dedent(
            f"""\
            Authenticated builder flow detected.

            Prefer the official builder SDKs:
            - Python: {OFFICIAL_LINKS['py_builder_client']}
            - TypeScript: {OFFICIAL_LINKS['ts_builder_client']}

            Endpoint docs: {docs}
            Auth docs: {OFFICIAL_LINKS['authentication']}
            """
        ).strip()
    if entry["sdk_preference"] == "official-relayer-sdk":
        return textwrap.dedent(
            f"""\
            Relayer flow detected.

            Prefer the official relayer SDKs:
            - Python: {OFFICIAL_LINKS['py_relayer_client']}
            - TypeScript: {OFFICIAL_LINKS['ts_relayer_client']}

            Endpoint docs: {docs}
            """
        ).strip()

    if output_format == "ts":
        return textwrap.dedent(
            f"""\
            // Prefer the official TypeScript CLOB client: {OFFICIAL_LINKS['ts_clob_client']}
            // Docs: {docs}
            // Auth: {OFFICIAL_LINKS['authentication']}
            // Geoblock: {OFFICIAL_LINKS['geoblock']}

            import {{ ClobClient }} from "@polymarket/clob-client";
            import {{ Wallet }} from "@ethersproject/wallet";

            const host = "https://clob.polymarket.com";
            const chainId = 137;
            const signer = new Wallet(process.env.POLYMARKET_PRIVATE_KEY!);

            const seedClient = new ClobClient(host, chainId, signer);
            const creds = await seedClient.createOrDeriveApiKey();

            const client = new ClobClient(
              host,
              chainId,
              signer,
              creds,
              1, // signatureType: 0=EOA, 1=Magic/email, 2=browser proxy
              process.env.POLYMARKET_FUNDER!,
            );

            // Call the matching authenticated method for {entry['operation_id']} here.
            """
        ).strip()

    return textwrap.dedent(
        f"""\
        # Prefer the official Python CLOB client: {OFFICIAL_LINKS['py_clob_client']}
        # Docs: {docs}
        # Auth: {OFFICIAL_LINKS['authentication']}
        # Geoblock: {OFFICIAL_LINKS['geoblock']}

        from py_clob_client.client import ClobClient

        HOST = "https://clob.polymarket.com"
        CHAIN_ID = 137
        PRIVATE_KEY = "<your-private-key>"
        FUNDER = "<your-funder-address>"

        client = ClobClient(
            HOST,
            key=PRIVATE_KEY,
            chain_id=CHAIN_ID,
            signature_type=1,  # 0=EOA, 1=Magic/email, 2=browser proxy
            funder=FUNDER,
        )
        client.set_api_creds(client.create_or_derive_api_creds())

        # Call the matching authenticated method for {entry['operation_id']} here.
        """
    ).strip()


def render_post_order_example(output_format: str) -> str:
    if output_format == "python":
        return textwrap.dedent(
            f"""\
            # Official client: {OFFICIAL_LINKS['py_clob_client']}
            # Quickstart: {OFFICIAL_LINKS['first_order']}
            # Auth: {OFFICIAL_LINKS['authentication']}

            from py_clob_client.client import ClobClient
            from py_clob_client.clob_types import OrderArgs, OrderType
            from py_clob_client.order_builder.constants import BUY

            HOST = "https://clob.polymarket.com"
            CHAIN_ID = 137
            PRIVATE_KEY = "<your-private-key>"
            FUNDER = "<your-funder-address>"

            client = ClobClient(
                HOST,
                key=PRIVATE_KEY,
                chain_id=CHAIN_ID,
                signature_type=1,  # 0=EOA, 1=Magic/email, 2=browser proxy
                funder=FUNDER,
            )
            client.set_api_creds(client.create_or_derive_api_creds())

            order = OrderArgs(token_id="TOKEN_ID", price=0.55, size=5.0, side=BUY)
            signed = client.create_order(order)
            response = client.post_order(signed, OrderType.GTC)
            print(response)
            """
        ).strip()

    if output_format == "ts":
        return textwrap.dedent(
            f"""\
            // Official client: {OFFICIAL_LINKS['ts_clob_client']}
            // Quickstart: {OFFICIAL_LINKS['first_order']}

            import {{ ClobClient, OrderType, Side }} from "@polymarket/clob-client";
            import {{ Wallet }} from "@ethersproject/wallet";

            const host = "https://clob.polymarket.com";
            const chainId = 137;
            const signer = new Wallet(process.env.POLYMARKET_PRIVATE_KEY!);

            const seedClient = new ClobClient(host, chainId, signer);
            const creds = await seedClient.createOrDeriveApiKey();

            const client = new ClobClient(
              host,
              chainId,
              signer,
              creds,
              1, // signatureType: 0=EOA, 1=Magic/email, 2=browser proxy
              process.env.POLYMARKET_FUNDER!,
            );

            const response = await client.createAndPostOrder(
              {{
                tokenID: "TOKEN_ID",
                price: 0.55,
                side: Side.BUY,
                size: 5,
              }},
              {{ tickSize: "0.01", negRisk: false }},
              OrderType.GTC,
              false,
              false,
            );

            console.log(response);
            """
        ).strip()

    return textwrap.dedent(
        f"""\
        Authenticated CLOB order flow detected.

        Prefer the official SDK rather than raw cURL:
        - Python: {OFFICIAL_LINKS['py_clob_client']}
        - TypeScript: {OFFICIAL_LINKS['ts_clob_client']}

        Supporting docs:
        - {OFFICIAL_LINKS['first_order']}
        - {OFFICIAL_LINKS['authentication']}
        - {OFFICIAL_LINKS['geoblock']}
        """
    ).strip()


def print_example(entry: dict[str, Any], output_format: str) -> None:
    if entry["auth_level"] == "public" and entry["method"] == "GET":
        print(render_public_get_example(entry, output_format))
        return
    if entry["operation_id"] == "postOrder":
        print(render_post_order_example(output_format))
        return
    print(render_generic_authenticated_example(entry, output_format))


def print_recommendation(choice: str) -> None:
    recommendation = RECOMMENDATIONS[choice]
    print(f"{choice}: {recommendation['use']}")
    print(f"Why: {recommendation['why']}")
    print("Start with:")
    for item in recommendation["start"]:
        print(f"- {item}")
    print(f"Caution: {recommendation['caution']}")
    print("Docs:")
    for url in recommendation["docs"]:
        print(f"- {url}")


def print_ws(channel: str) -> None:
    config = WS_CHANNELS[channel]
    print(config["title"])
    print(f"Endpoint: {config['endpoint']}")
    print(f"Auth: {config['auth']}")
    print(f"Docs: {config['docs']}")
    print(f"Heartbeat: {config['heartbeat']}")
    print(f"ID semantics: {config['ids']}")
    print(f"Notes: {config['notes']}")
    if config.get("event_types"):
        print("Event types:")
        for item in config["event_types"]:
            print(f"- {item}")
    if config.get("quirks"):
        print("Quirks:")
        for item in config["quirks"]:
            print(f"- {item}")
    if config.get("subscribe") is not None:
        print("Subscribe:")
        print(render_json(config["subscribe"]))
    if config.get("update_subscription") is not None:
        print("Update subscription:")
        print(render_json(config["update_subscription"]))
    if config.get("unsubscribe") is not None:
        print("Unsubscribe:")
        print(render_json(config["unsubscribe"]))
    for example in config.get("examples", []):
        print(example["label"] + ":")
        print(render_json(example["payload"]))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search and explain Polymarket API endpoints.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search the endpoint catalog.")
    search_parser.add_argument("query", nargs="+")
    search_parser.add_argument("--service", choices=["gamma", "clob", "data", "bridge", "relayer"])
    search_parser.add_argument("--auth", choices=["public", "l1", "l2", "optional"])
    search_parser.add_argument("--limit", type=int, default=20)

    show_parser = subparsers.add_parser("show", help="Show a single endpoint.")
    show_parser.add_argument("identifier", nargs="+")

    example_parser = subparsers.add_parser("example", help="Generate an example request or SDK scaffold.")
    example_parser.add_argument("identifier", nargs="+")
    example_parser.add_argument("--format", choices=["curl", "python", "ts"], default="curl")

    recommend_parser = subparsers.add_parser("recommend", help="Recommend the right API family for a task.")
    recommend_parser.add_argument(
        "target",
        choices=["discover", "prices", "positions", "trade", "streaming", "comments", "funding", "gasless"],
    )

    ws_parser = subparsers.add_parser("ws", help="Show WebSocket or RTDS channel details.")
    ws_parser.add_argument("channel", choices=["market", "user", "sports", "rtds"])

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    catalog = load_catalog()

    if args.command == "search":
        print_search(
            catalog,
            normalize_identifier(args.query),
            args.service,
            args.auth,
            args.limit,
        )
        return 0

    if args.command == "show":
        print_show(resolve_entry(catalog, normalize_identifier(args.identifier)))
        return 0

    if args.command == "example":
        print_example(resolve_entry(catalog, normalize_identifier(args.identifier)), args.format)
        return 0

    if args.command == "recommend":
        print_recommendation(args.target)
        return 0

    if args.command == "ws":
        print_ws(args.channel)
        return 0

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
