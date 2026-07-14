# Topic library

A menu for topic selection. First pick the **discipline track** (frontend,
backend, or mobile; fullstack blends two). Always include the **shared core**, then
add the discipline track and any **cross-cutting** or **framework-specific** topics
the JD names. Adapt specifics to the JD's actual stack; do not include a topic the
role does not touch. Aim for 6 to 12 topics total.

Each entry lists what a strong version covers and sample Q&A themes.

---

## Shared core (all disciplines)

### Language fundamentals (of the JD's primary language)
- Cover: memory/execution model, concurrency/async model and pitfalls, collections
  and complexity, error handling, key idioms and recent features.
- Q&A: a classic gotcha, an async/concurrency question, a "why is this slow" one.
- JS/TS: event loop, micro/macro tasks, closures, prototypes, `this`, promises/
  async-await, modules, TS generics/narrowing.
- Java: JVM/GC, JMM + happens-before, `volatile` vs atomic, virtual threads (21),
  collections Big-O, generics/PECS, streams, records/sealed.
- Python: GIL, asyncio vs threads vs multiprocessing, generators, decorators,
  type hints, dataclasses/Pydantic.
- Swift: value vs reference types, ARC + retain cycles, optionals, protocols,
  async-await/actors. Kotlin: coroutines, null-safety, data classes, flows.

### Problem-solving / DS & algorithms
- Cover: arrays/strings/hashmaps, stacks/queues, trees/graphs, sorting, recursion,
  Big-O, and the discipline's common patterns (two pointers, sliding window, BFS/
  DFS). Right-size to the JD (product roles lean lighter than infra roles).
- Q&A: complexity of a proposed approach, space/time tradeoff, a "how would you
  optimize this" prompt.

### System design (framed for the discipline)
- Backend: distributed system design (see backend track).
- Frontend: component/app architecture, rendering strategy, data-fetching and
  caching, state architecture, design system, performance budget.
- Mobile: app architecture, offline-first data flow, sync, navigation, release/
  versioning constraints.
- Q&A: "first thing you clarify," one end-to-end design walk, the key tradeoff.

### Behavioral & questions to ask
- Cover: STAR; stories for disagreement, incident/bug ownership, shipping-vs-rigor,
  and why this company; plus sharp questions to ask them.
- Q&A: the common behavioral prompts with a structure for each.

---

## Backend track

### Data & consistency
- Cover: ACID and isolation levels (and the anomaly each prevents), BASE, CAP and
  PACELC, consistency models (linearizable, causal, read-your-writes, eventual),
  replication and quorums, why 2PC is avoided. Add the named DB's specifics
  (Postgres: MVCC, row-level security, JSONB, pgvector).
- Q&A: "explain CAP and the real choice," "C in ACID vs C in CAP," "design
  consistency for feature X."

### Microservices patterns
- Cover: decomposition (DDD, strangler fig), data (db-per-service, CQRS, event
  sourcing), transactions (saga, outbox, idempotent consumer), communication
  (REST/gRPC/GraphQL, Kafka), deployment (canary, expand/contract migrations),
  observability, anti-patterns (distributed monolith). Include the "modular
  monolith first for a small team" stance.
- Q&A: outbox/dual-write, choreography vs orchestration, exactly-once reality.

### Resilience & rate limiting
- Cover: timeout, retry (backoff + jitter, amplification), circuit breaker
  (3 states), bulkhead, fallback, load shedding/backpressure, health checks,
  idempotency. Rate limiting: token/leaky bucket, fixed/sliding window, distributed
  via a shared store, 429 + Retry-After, per-tenant fairness.
- Q&A: circuit-breaker states, when not to retry, token vs leaky bucket.

---

## Frontend track

### JavaScript / TypeScript deep dive
- Cover: the event loop and task/microtask ordering, closures and scope,
  prototypal inheritance and `this`, promises/async-await, memory leaks, ES modules
  and bundling, and TS types (generics, unions, narrowing, `unknown` vs `any`).
- Q&A: output-of-this-snippet event-loop question, a closure gotcha, `==` vs `===`
  and coercion.

### UI framework (React / Vue / Angular; use the one named)
- Cover (React example): the render/reconciliation model and virtual DOM, hooks and
  their rules, `useEffect` dependencies and cleanup, memoization (`useMemo`/
  `useCallback`/`React.memo`) and avoiding needless re-renders, controlled vs
  uncontrolled inputs, keys, context vs a state library, Suspense/concurrent
  features, SSR/hydration.
- Q&A: why a component re-renders, stale-closure in `useEffect`, when memoization
  helps vs hurts.

### Rendering, the browser & the network
- Cover: the critical rendering path, DOM/CSSOM, reflow vs repaint, event bubbling/
  delegation, rendering strategies (CSR/SSR/SSG/ISR) and their tradeoffs, cookies/
  storage, CORS, and caching headers.
- Q&A: CSR vs SSR tradeoff, what causes layout thrashing, how CORS works.

### Performance
- Cover: Core Web Vitals (LCP, CLS, INP), code-splitting and lazy loading, bundle
  size, image optimization, caching/CDN, debounce/throttle, virtualization of long
  lists, avoiding re-renders.
- Q&A: diagnose a slow page, reduce bundle size, fix a CLS/LCP regression.

### State management
- Cover: local vs global state, Context vs Redux/Zustand, server-state libraries
  (React Query/SWR) and cache invalidation, normalization, derived vs stored state,
  optimistic updates.
- Q&A: when to reach for a global store, server state vs client state, optimistic
  update with rollback.

### CSS & layout
- Cover: box model, flexbox and grid, the cascade/specificity, stacking contexts,
  responsive design and container queries, CSS modules vs CSS-in-JS.
- Q&A: center-and-scale a layout, specificity conflict, flexbox vs grid choice.

### Accessibility (a11y)
- Cover: semantic HTML, ARIA roles/labels (and when not to use ARIA), keyboard
  navigation and focus management, color contrast, and WCAG basics.
- Q&A: make a custom widget accessible, manage focus in a modal, alt-text rules.

### Frontend security
- Cover: XSS (and how frameworks escape by default), CSP, CSRF, sanitizing
  user/HTML input, secure token handling in the browser (why not localStorage for
  sensitive tokens), and supply-chain risk.
- Q&A: prevent XSS in a React app, where to store an auth token, what CSP buys you.

### Frontend testing
- Cover: the testing pyramid for UIs, unit (Jest/Vitest), component (Testing
  Library, testing behavior not implementation), and e2e (Playwright/Cypress).
- Q&A: what to unit vs e2e test, testing an async component, flaky-test causes.

---

## Mobile track

### Platform core (iOS / Android / cross-platform; use the one named)
- iOS: Swift, SwiftUI vs UIKit, ARC and retain cycles, GCD/async-await/actors, the
  app and view-controller lifecycle.
- Android: Kotlin, coroutines/flows, the activity/fragment lifecycle, Jetpack
  Compose vs Views, memory management.
- Cross-platform: React Native (bridge/JSI, native modules) or Flutter (widget tree,
  rendering, Dart isolates).
- Q&A: a lifecycle question, the main-thread rule, a memory-leak/retain-cycle cause.

### App architecture
- Cover: MVVM/MVI/VIPER/Clean, unidirectional data flow, dependency injection, and
  separating UI from domain and data layers.
- Q&A: why MVVM over MVC, where business logic lives, testable architecture.

### Concurrency & performance
- Cover: keeping work off the main thread, structured concurrency (coroutines/
  async-await), avoiding jank (60/120fps), startup time, battery and network
  efficiency, list recycling (RecyclerView/UITableView/LazyColumn).
- Q&A: fix a janky scroll, background a long task, reduce cold-start time.

### Persistence & offline
- Cover: local storage (Core Data/Room/SQLite/Realm), offline-first sync, caching,
  conflict resolution (last-write-wins vs CRDTs), and migrations.
- Q&A: design offline sync, resolve a sync conflict, cache-invalidation strategy.

### Networking on mobile
- Cover: REST/GraphQL clients, caching, retries with backoff, pagination, handling
  flaky/low-bandwidth networks, idempotency, background upload/download.
- Q&A: make a request resilient on a flaky network, pagination approach, idempotent
  retries.

### Mobile security & release
- Cover: Keychain/Keystore, certificate pinning, secure storage, biometric auth,
  obfuscation; plus release realities: app-store review, staged rollout, forced vs
  optional update, and backward-compatible APIs (you cannot force-upgrade clients).
- Q&A: store a token securely on device, roll out a risky change, keep the backend
  compatible with old app versions in the wild.

---

## Cross-cutting (add when relevant to any discipline)

### Auth (OAuth2 / OIDC)
- Include when the product ships login or names an auth provider.
- Cover: OAuth2 vs OIDC, grants (Authorization Code + PKCE, client credentials,
  refresh), token types and JWT validation (JWKS + iss/aud/exp), sessions vs
  tokens, build vs buy, and platform token storage (browser vs Keychain/Keystore).
- Q&A: OAuth2 vs OIDC, why PKCE (web and mobile), revoking stateless JWTs.

### AI in production
- Include when the JD mentions models/ML/LLMs/AI.
- Cover: non-determinism (evals, golden sets, guardrails, structured output),
  latency/cost tradeoffs, resilient model calls (timeout/retry/circuit breaker/
  fallback), prompt injection and treating output as untrusted, RAG basics.
- Q&A: test a non-deterministic feature, defend against prompt injection, sketch a
  RAG pipeline on their stack.

### SaaS & multi-tenancy (backend/fullstack products)
- Cover: tenancy models (db/schema/shared-row) and isolation-vs-cost tradeoffs,
  tenant isolation as the top security bug class, noisy-neighbor limits, plan-
  gating, metering.
- Q&A: compare tenancy models, how row-level security enforces isolation.

---

## Framework-specific (add when named)

### Spring / Spring Boot (Java backend)
- Cover: IoC/DI lifecycle, constructor vs field injection, the AOP proxy model and
  the self-invocation gotcha, `@Transactional` propagation + rollback rules,
  autoconfiguration, Spring Security filter chain + resource server, testing slices
  + Testcontainers, N+1 and DTO-vs-entity.
- Q&A: self-invocation, checked-exception rollback, N+1 fix, JWT validation.

Add analogous framework topics for other stacks the JD names (Django/FastAPI for
Python, Express/Nest for Node, .NET for C#, and the UI/mobile frameworks above),
following the same shape: mechanisms, gotchas, and testing.
