# Polymarket REST Endpoints

Generated from the official Polymarket OpenAPI specs on 2026-03-10T20:44:20+00:00.
Regenerate with `scripts/refresh_catalog.py`.

## Gamma API

Base URL: `https://gamma-api.polymarket.com`

| Method | Path | Auth | Operation ID | Summary | Docs |
| --- | --- | --- | --- | --- | --- |
| GET | `/comments` | `public` | `listComments` | List comments | [Docs](https://docs.polymarket.com/api-reference/comments/list-comments) |
| GET | `/comments/user_address/{user_address}` | `public` | `getCommentsByUserAddress` | Get comments by user address | [Docs](https://docs.polymarket.com/api-reference/comments/get-comments-by-user-address) |
| GET | `/comments/{id}` | `public` | `getCommentsById` | Get comments by comment id | [Docs](https://docs.polymarket.com/api-reference/comments/get-comments-by-comment-id) |
| GET | `/events` | `public` | `listEvents` | List events | [Docs](https://docs.polymarket.com/api-reference/events/list-events) |
| GET | `/events/creators` | `public` | `listEventCreators` | List event creators | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/events/creators/{id}` | `public` | `getEventCreator` | Get event creator by id | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/events/pagination` | `public` | `listEventsPagination` | List events (paginated) | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/events/results` | `public` | `listSportEventsResults` | List sport events results | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/events/slug/{slug}` | `public` | `getEventBySlug` | Get event by slug | [Docs](https://docs.polymarket.com/api-reference/events/get-event-by-slug) |
| GET | `/events/{id}` | `public` | `getEvent` | Get event by id | [Docs](https://docs.polymarket.com/api-reference/events/get-event-by-id) |
| GET | `/events/{id}/comments/count` | `public` | `getEventCommentsCount` | Get event comment count | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/events/{id}/tags` | `public` | `getEventTags` | Get event tags | [Docs](https://docs.polymarket.com/api-reference/events/get-event-tags) |
| GET | `/events/{id}/tweet-count` | `public` | `getEventTweetCount` | Get event tweet count | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/markets` | `public` | `listMarkets` | List markets | [Docs](https://docs.polymarket.com/api-reference/markets/list-markets) |
| POST | `/markets/abridged` | `public` | `getAbridgedMarkets` | Query abridged markets by information filters | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| POST | `/markets/information` | `public` | `getMarketsInformation` | Query markets by information filters | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/markets/slug/{slug}` | `public` | `getMarketBySlug` | Get market by slug | [Docs](https://docs.polymarket.com/api-reference/markets/get-market-by-slug) |
| GET | `/markets/{id}` | `public` | `getMarket` | Get market by id | [Docs](https://docs.polymarket.com/api-reference/markets/get-market-by-id) |
| GET | `/markets/{id}/description` | `public` | `getMarketDescription` | Get market description by id | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/markets/{id}/tags` | `public` | `getMarketTags` | Get market tags by id | [Docs](https://docs.polymarket.com/api-reference/markets/get-market-tags-by-id) |
| GET | `/profiles/user_address/{user_address}` | `public` | `getPublicProfileByUserAddress` | Get public profile by user address | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/public-profile` | `public` | `getPublicProfile` | Get public profile by wallet address | [Docs](https://docs.polymarket.com/api-reference/profiles/get-public-profile-by-wallet-address) |
| GET | `/public-search` | `public` | `publicSearch` | Search markets, events, and profiles | [Docs](https://docs.polymarket.com/api-reference/search/search-markets-events-and-profiles) |
| GET | `/series` | `public` | `listSeries` | List series | [Docs](https://docs.polymarket.com/api-reference/series/list-series) |
| GET | `/series-summary/slug/{slug}` | `public` | `getSeriesSummaryBySlug` | Get series summary by slug | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/series-summary/{id}` | `public` | `getSeriesSummaryById` | Get series summary by id | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/series/{id}` | `public` | `getSeries` | Get series by id | [Docs](https://docs.polymarket.com/api-reference/series/get-series-by-id) |
| GET | `/series/{id}/comments/count` | `public` | `getSeriesCommentsCount` | Get series comment count | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/sports` | `public` | `getSportsMetadata` | Get sports metadata information | [Docs](https://docs.polymarket.com/api-reference/sports/get-sports-metadata-information) |
| GET | `/sports/market-types` | `public` | `getSportsMarketTypes` | Get valid sports market types | [Docs](https://docs.polymarket.com/api-reference/sports/get-valid-sports-market-types) |
| GET | `/status` | `public` | `getGammaStatus` | Gamma API Health check | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/tags` | `public` | `listTags` | List tags | [Docs](https://docs.polymarket.com/api-reference/tags/list-tags) |
| GET | `/tags/slug/{slug}` | `public` | `getTagBySlug` | Get tag by slug | [Docs](https://docs.polymarket.com/api-reference/tags/get-tag-by-slug) |
| GET | `/tags/slug/{slug}/related-tags` | `public` | `getRelatedTagsBySlug` | Get related tags (relationships) by tag slug | [Docs](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug) |
| GET | `/tags/slug/{slug}/related-tags/tags` | `public` | `getTagsRelatedToATagBySlug` | Get tags related to a tag slug | [Docs](https://docs.polymarket.com/api-reference/tags/get-tags-related-to-a-tag-slug) |
| GET | `/tags/{id}` | `public` | `getTag` | Get tag by id | [Docs](https://docs.polymarket.com/api-reference/tags/get-tag-by-id) |
| GET | `/tags/{id}/related-tags` | `public` | `getRelatedTagsById` | Get related tags (relationships) by tag id | [Docs](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-id) |
| GET | `/tags/{id}/related-tags/tags` | `public` | `getTagsRelatedToATagById` | Get tags related to a tag id | [Docs](https://docs.polymarket.com/api-reference/tags/get-tags-related-to-a-tag-id) |
| GET | `/teams` | `public` | `listTeams` | List teams | [Docs](https://docs.polymarket.com/api-reference/sports/list-teams) |
| GET | `/teams/{id}` | `public` | `getTeam` | Get team by id | [Docs](https://docs.polymarket.com/api-reference/introduction) |

## CLOB API

Base URL: `https://clob.polymarket.com`

| Method | Path | Auth | Operation ID | Summary | Docs |
| --- | --- | --- | --- | --- | --- |
| DELETE | `/auth/api-key` | `l2` | `deleteApiKey` | Delete API key | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| POST | `/auth/api-key` | `l1` | `createApiKey` | Create API key | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/auth/api-keys` | `l1` | `getApiKeys` | Get API keys | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/auth/ban-status/closed-only` | `l2` | `getClosedOnlyMode` | Get closed-only mode status | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| DELETE | `/auth/builder-api-key` | `l2` | `revokeBuilderApiKey` | Revoke builder API key | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/auth/builder-api-key` | `l2` | `getBuilderApiKeys` | Get builder API keys | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| POST | `/auth/builder-api-key` | `l2` | `createBuilderApiKey` | Create builder API key | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/auth/derive-api-key` | `l1` | `deriveApiKey` | Derive API key | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/balance-allowance` | `l2` | `getBalanceAllowance` | Get balance and allowance | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| PUT | `/balance-allowance` | `l2` | `updateBalanceAllowance` | Update balance and allowance | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/balance-allowance/update` | `l2` | `getUpdateBalanceAllowance` | Update balance and allowance | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/book` | `public` | `getBook` | Get order book | [Docs](https://docs.polymarket.com/api-reference/market-data/get-order-book) |
| GET | `/books` | `public` | `getBooksGet` | Get order books (query parameters) | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| POST | `/books` | `public` | `getBooksPost` | Get order books (request body) | [Docs](https://docs.polymarket.com/api-reference/market-data/get-order-books-request-body) |
| GET | `/builder/trades` | `l2` | `getBuilderTrades` | Get builder trades | [Docs](https://docs.polymarket.com/api-reference/trade/get-builder-trades) |
| DELETE | `/cancel-all` | `l2` | `cancelAllOrders` | Cancel all orders | [Docs](https://docs.polymarket.com/api-reference/trade/cancel-all-orders) |
| DELETE | `/cancel-market-orders` | `l2` | `cancelMarketOrders` | Cancel orders for a market | [Docs](https://docs.polymarket.com/api-reference/trade/cancel-orders-for-a-market) |
| GET | `/fee-rate` | `public` | `getFeeRate` | Get fee rate | [Docs](https://docs.polymarket.com/api-reference/market-data/get-fee-rate) |
| GET | `/fee-rate/{token_id}` | `public` | `getFeeRateByPath` | Get fee rate by path parameter | [Docs](https://docs.polymarket.com/api-reference/market-data/get-fee-rate-by-path-parameter) |
| POST | `/heartbeats` | `l2` | `sendHeartbeat` | Send heartbeat | [Docs](https://docs.polymarket.com/api-reference/trade/send-heartbeat) |
| GET | `/last-trade-price` | `public` | `getLastTradePrice` | Get last trade price | [Docs](https://docs.polymarket.com/api-reference/market-data/get-last-trade-price) |
| GET | `/last-trades-prices` | `public` | `getLastTradesPricesGet` | Get last trade prices (query parameters) | [Docs](https://docs.polymarket.com/api-reference/market-data/get-last-trade-prices-query-parameters) |
| POST | `/last-trades-prices` | `public` | `getLastTradesPricesPost` | Get last trade prices (request body) | [Docs](https://docs.polymarket.com/api-reference/market-data/get-last-trade-prices-request-body) |
| POST | `/markets/live-activity` | `public` | `getMarketsLiveActivity` | Get live activity markets by condition IDs | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/markets/live-activity/{condition_id}` | `public` | `getMarketLiveActivity` | Get live activity market by condition ID | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/midpoint` | `public` | `getMidpoint` | Get midpoint price | [Docs](https://docs.polymarket.com/api-reference/data/get-midpoint-price) |
| GET | `/midpoints` | `public` | `getMidpointsGet` | Get midpoint prices (query parameters) | [Docs](https://docs.polymarket.com/api-reference/market-data/get-midpoint-prices-query-parameters) |
| POST | `/midpoints` | `public` | `getMidpointsPost` | Get midpoint prices (request body) | [Docs](https://docs.polymarket.com/api-reference/market-data/get-midpoint-prices-request-body) |
| GET | `/neg-risk` | `public` | `getNegRisk` | Get negative risk flag | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/neg-risk/{token_id}` | `public` | `getNegRiskByPath` | Get negative risk flag by path parameter | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| DELETE | `/notifications` | `l2` | `dropNotifications` | Mark notifications as read | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/notifications` | `l2` | `getNotifications` | Get notifications | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| DELETE | `/order` | `l2` | `cancelOrder` | Cancel single order | [Docs](https://docs.polymarket.com/api-reference/trade/cancel-single-order) |
| POST | `/order` | `l2` | `postOrder` | Post a new order | [Docs](https://docs.polymarket.com/api-reference/trade/post-a-new-order) |
| GET | `/order-scoring` | `l2` | `getOrderScoring` | Get order scoring status | [Docs](https://docs.polymarket.com/api-reference/trade/get-order-scoring-status) |
| GET | `/order/{orderID}` | `l2` | `getOrder` | Get single order by ID | [Docs](https://docs.polymarket.com/api-reference/trade/get-single-order-by-id) |
| DELETE | `/orders` | `l2` | `cancelOrders` | Cancel multiple orders | [Docs](https://docs.polymarket.com/api-reference/trade/cancel-multiple-orders) |
| GET | `/orders` | `l2` | `getOrders` | Get user orders | [Docs](https://docs.polymarket.com/api-reference/trade/get-user-orders) |
| POST | `/orders` | `l2` | `postOrders` | Post multiple orders | [Docs](https://docs.polymarket.com/api-reference/trade/post-multiple-orders) |
| GET | `/orders-scoring` | `l2` | `getOrdersScoring` | Get scoring status for multiple orders | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| POST | `/orders-scoring` | `l2` | `postOrdersScoring` | Get scoring status for multiple orders (POST) | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/price` | `public` | `getPrice` | Get market price | [Docs](https://docs.polymarket.com/api-reference/market-data/get-market-price) |
| GET | `/prices` | `public` | `getPricesGet` | Get market prices (query parameters) | [Docs](https://docs.polymarket.com/api-reference/market-data/get-market-prices-query-parameters) |
| POST | `/prices` | `public` | `getPricesPost` | Get market prices (request body) | [Docs](https://docs.polymarket.com/api-reference/market-data/get-market-prices-request-body) |
| GET | `/prices-history` | `public` | `getPricesHistory` | Get prices history | [Docs](https://docs.polymarket.com/api-reference/markets/get-prices-history) |
| GET | `/rebates/current` | `public` | `getCurrentRebatedFees` | Get current rebated fees for a maker | [Docs](https://docs.polymarket.com/api-reference/rebates/get-current-rebated-fees-for-a-maker) |
| GET | `/rewards/user` | `l2` | `getEarningsForUserForDay` | Get earnings for user by date | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/rewards/user/markets` | `l2` | `getUserEarningsAndMarketsConfig` | Get user earnings and markets configuration | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/rewards/user/percentages` | `l2` | `getRewardPercentagesForUser` | Get reward percentages for user | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/rewards/user/total` | `l2` | `getTotalEarningsForUserForDay` | Get total earnings for user by date | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/sampling-markets` | `public` | `getSamplingMarkets` | Get sampling markets | [Docs](https://docs.polymarket.com/api-reference/markets/get-sampling-markets) |
| GET | `/sampling-simplified-markets` | `public` | `getSamplingSimplifiedMarkets` | Get sampling simplified markets | [Docs](https://docs.polymarket.com/api-reference/markets/get-sampling-simplified-markets) |
| GET | `/simplified-markets` | `public` | `getSimplifiedMarkets` | Get simplified markets | [Docs](https://docs.polymarket.com/api-reference/markets/get-simplified-markets) |
| GET | `/spread` | `public` | `getSpread` | Get spread | [Docs](https://docs.polymarket.com/api-reference/market-data/get-spread) |
| POST | `/spreads` | `public` | `getSpreads` | Get spreads | [Docs](https://docs.polymarket.com/api-reference/market-data/get-spreads) |
| GET | `/tick-size` | `public` | `getTickSize` | Get tick size | [Docs](https://docs.polymarket.com/api-reference/market-data/get-tick-size) |
| GET | `/tick-size/{token_id}` | `public` | `getTickSizeByPath` | Get tick size by path parameter | [Docs](https://docs.polymarket.com/api-reference/market-data/get-tick-size-by-path-parameter) |
| GET | `/time` | `public` | `getTime` | Get server time | [Docs](https://docs.polymarket.com/api-reference/data/get-server-time) |
| GET | `/trades` | `l2` | `getTrades` | Get trades | [Docs](https://docs.polymarket.com/api-reference/trade/get-trades) |
| POST | `/v1/heartbeats` | `l2` | `sendHeartbeatV1` | Send heartbeat (v1) | [Docs](https://docs.polymarket.com/api-reference/introduction) |

## Data API

Base URL: `https://data-api.polymarket.com`

| Method | Path | Auth | Operation ID | Summary | Docs |
| --- | --- | --- | --- | --- | --- |
| GET | `/` | `public` | `getDataApiHealth` | Data API Health check | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/activity` | `public` | `get_/activity` | Get user activity | [Docs](https://docs.polymarket.com/api-reference/core/get-user-activity) |
| GET | `/closed-positions` | `public` | `get_/closed-positions` | Get closed positions for a user | [Docs](https://docs.polymarket.com/api-reference/core/get-closed-positions-for-a-user) |
| GET | `/holders` | `public` | `get_/holders` | Get top holders for markets | [Docs](https://docs.polymarket.com/api-reference/core/get-top-holders-for-markets) |
| GET | `/live-volume` | `public` | `get_/live-volume` | Get live volume for an event | [Docs](https://docs.polymarket.com/api-reference/misc/get-live-volume-for-an-event) |
| GET | `/oi` | `public` | `get_/oi` | Get open interest | [Docs](https://docs.polymarket.com/api-reference/misc/get-open-interest) |
| GET | `/other` | `public` | `get_/other` | Get "Other" size for an augmented neg risk event and user | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/positions` | `public` | `get_/positions` | Get current positions for a user | [Docs](https://docs.polymarket.com/api-reference/core/get-current-positions-for-a-user) |
| GET | `/revisions` | `public` | `get_/revisions` | Get moderated revisions for a question | [Docs](https://docs.polymarket.com/api-reference/introduction) |
| GET | `/traded` | `public` | `get_/traded` | Get total markets a user has traded | [Docs](https://docs.polymarket.com/api-reference/misc/get-total-markets-a-user-has-traded) |
| GET | `/trades` | `public` | `get_/trades` | Get trades for a user or markets | [Docs](https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets) |
| GET | `/v1/accounting/snapshot` | `public` | `get_/v1/accounting/snapshot` | Download an accounting snapshot (ZIP of CSVs) | [Docs](https://docs.polymarket.com/api-reference/misc/download-an-accounting-snapshot-zip-of-csvs) |
| GET | `/v1/builders/leaderboard` | `public` | `get_/v1/builders/leaderboard` | Get aggregated builder leaderboard | [Docs](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard) |
| GET | `/v1/builders/volume` | `public` | `get_/v1/builders/volume` | Get daily builder volume time-series | [Docs](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series) |
| GET | `/v1/leaderboard` | `public` | `get_/v1/leaderboard` | Get trader leaderboard rankings | [Docs](https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings) |
| GET | `/v1/market-positions` | `public` | `get_/v1/market-positions` | Get positions for a market | [Docs](https://docs.polymarket.com/api-reference/core/get-positions-for-a-market) |
| GET | `/value` | `public` | `get_/value` | Get total value of a user's positions | [Docs](https://docs.polymarket.com/api-reference/core/get-total-value-of-a-users-positions) |

## Bridge API

Base URL: `https://bridge.polymarket.com`

| Method | Path | Auth | Operation ID | Summary | Docs |
| --- | --- | --- | --- | --- | --- |
| POST | `/deposit` | `public` | `post_/deposit` | Create deposit addresses | [Docs](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses) |
| POST | `/quote` | `public` | `post_/quote` | Get a quote | [Docs](https://docs.polymarket.com/api-reference/bridge/get-a-quote) |
| GET | `/status/{address}` | `public` | `get_/status/{address}` | Get transaction status | [Docs](https://docs.polymarket.com/api-reference/bridge/get-transaction-status) |
| GET | `/supported-assets` | `public` | `get_/supported-assets` | Get supported assets | [Docs](https://docs.polymarket.com/api-reference/bridge/get-supported-assets) |
| POST | `/withdraw` | `public` | `post_/withdraw` | Create withdrawal addresses | [Docs](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses) |

## Relayer API

Base URL: `https://relayer-v2.polymarket.com`

| Method | Path | Auth | Operation ID | Summary | Docs |
| --- | --- | --- | --- | --- | --- |
| GET | `/deployed` | `public` | `get_/deployed` | Check if a safe is deployed | [Docs](https://docs.polymarket.com/api-reference/relayer/check-if-a-safe-is-deployed) |
| GET | `/nonce` | `public` | `get_/nonce` | Get current nonce for a user | [Docs](https://docs.polymarket.com/api-reference/relayer/get-current-nonce-for-a-user) |
| GET | `/relay-payload` | `public` | `get_/relay-payload` | Get relayer address and nonce | [Docs](https://docs.polymarket.com/api-reference/relayer/get-relayer-address-and-nonce) |
| GET | `/relayer/api/keys` | `public` | `get_/relayer/api/keys` | Get all relayer API keys | [Docs](https://docs.polymarket.com/api-reference/relayer-api-keys/get-all-relayer-api-keys) |
| POST | `/submit` | `public` | `post_/submit` | Submit a transaction | [Docs](https://docs.polymarket.com/api-reference/relayer/submit-a-transaction) |
| GET | `/transaction` | `public` | `get_/transaction` | Get a transaction by ID | [Docs](https://docs.polymarket.com/api-reference/relayer/get-a-transaction-by-id) |
| GET | `/transactions` | `public` | `get_/transactions` | Get recent transactions for a user | [Docs](https://docs.polymarket.com/api-reference/relayer/get-recent-transactions-for-a-user) |
