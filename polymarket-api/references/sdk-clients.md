# Official SDK Clients

Prefer these official clients whenever the task involves authenticated CLOB flows, signing, builder attribution, or relayer submission.

## Core CLOB Clients

- TypeScript
  - Package: `@polymarket/clob-client`
  - Repo: `https://github.com/Polymarket/clob-client`
- Python
  - Package: `py-clob-client`
  - Repo: `https://github.com/Polymarket/py-clob-client`
- Rust
  - Package: `polymarket-client-sdk`
  - Repo: `https://github.com/Polymarket/rs-clob-client`

Use the core CLOB clients for:

- L1 credential creation or derivation
- L2 API-key trading flows
- Local order signing
- Public CLOB market reads when you want a library wrapper instead of raw HTTP

## Builder SDKs

- TypeScript
  - Package: `@polymarket/builder-signing-sdk`
  - Repo: `https://github.com/Polymarket/builder-signing-sdk`
- Python
  - Package: `py_builder_signing_sdk`
  - Repo: `https://github.com/Polymarket/py-builder-signing-sdk`

Use builder SDKs when the task is specifically about Builder Program attribution or builder API keys.

## Relayer SDKs

- TypeScript
  - Package: `@polymarket/builder-relayer-client`
  - Repo: `https://github.com/Polymarket/builder-relayer-client`
- Python
  - Package: `py-builder-relayer-client`
  - Repo: `https://github.com/Polymarket/py-builder-relayer-client`

Use relayer SDKs for gasless transaction submission and relayer-specific flows.

## Practical Defaults

- If the task is authenticated CLOB and not builder- or relayer-specific, default to the core CLOB SDK.
- If the user only needs a one-off public read, direct HTTP is usually simpler than pulling in a client.
- If the task is about order placement, funder selection, or signature types, open the auth doc before coding.
