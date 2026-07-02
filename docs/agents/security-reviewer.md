# security-reviewer

A read-only, stack-agnostic security auditor for web apps that use OAuth2/OIDC
(OpenID Connect) authentication. It works with any frontend and backend against
any OIDC provider (Keycloak, Auth0, Okta, Cognito, Entra ID, Google, a custom
authorization server, etc.), discovering the relevant files rather than assuming
a layout. It reports findings grouped by severity (Critical / High / Medium /
Low / Info), with `file:line` locations and concrete recommended fixes. It does
not modify files.

**Agent file:** [`agents/security-reviewer.md`](../../agents/security-reviewer.md)

## What it looks at

- **OIDC client config**: client confidentiality, enabled flows, redirect URIs
  and web origins, token/session lifespans, PKCE usage.
- **Frontend / client auth**: client secret stays server-side, access token
  kept in memory (not `localStorage`), safe token refresh, no tokens logged,
  state/nonce validated.
- **Backend resource server**: token validation (signature/issuer/audience/
  expiry), endpoints requiring authentication, scope/authorization enforcement,
  CORS scoped to known origins, no secrets in logs.
- **Issuer / transport**: consistent issuer between frontend and backend, TLS
  for real environments, and flags local-only shortcuts (plain HTTP, relaxed
  hostname/cert checks) that must change before production.
- **Secrets & configuration**: secrets from a secure source, not hardcoded or
  committed for non-local targets; secure session cookies.
- **Dependencies**: obviously outdated or known-vulnerable auth libraries.

It is environment-aware: for an explicit local/non-production demo it treats
clearly-marked dev-only placeholder secrets as acceptable, while holding
anything production-bound to a production bar.

## Usage

Copy the agent file into a project's `.claude/agents/` directory (or into
`~/.claude/agents/` to make it available everywhere), then invoke it as
`security-reviewer`.

## Example output

Below is a representative report from running the agent against the
[`nextjs-springboot-keycloak-poc`](https://github.com/hcussi/nextjs-springboot-keycloak-poc)
project (Next.js + next-auth, Spring Boot resource server, Keycloak). Every
finding here was subsequently fixed (the IDs map to the `Fix H-1`, `Fix M-1`, …
commits in that repo), which is exactly how the report is meant to be used: as an
actionable, prioritized worklist.

---

### Security review: nextjs-springboot-keycloak-poc

**Critical**: none.

**High**

- **H-1**: `backend/.../config/SecurityConfig.java`: The resource server
  validates the JWT signature, issuer, and expiry but not the `aud` claim. Any
  token the realm issues for another client is therefore accepted by this API.
  *Fix:* add an audience validator (`DelegatingOAuth2TokenValidator` +
  `AudienceValidator`) so only tokens minted for this API are accepted.

**Medium**

- **M-1**: `frontend/src/lib/auth.ts`: Signing out clears the local next-auth
  session but leaves the Keycloak SSO session alive, so the next "Log in" silently
  re-authenticates without credentials. *Fix:* call the Keycloak end-session /
  back-channel logout endpoint on `signOut`.
- **M-2**: `keycloak/realm-export.json`: Refresh tokens are long-lived and
  reusable; a leaked refresh token stays valid. *Fix:* enable
  `revokeRefreshToken` with `refreshTokenMaxReuse: 0` so each refresh rotates the
  token and reuse is rejected.
- **M-3**: `keycloak/realm-export.json`: The client requests broad default
  scopes (and `fullScopeAllowed`), so tokens carry more claims/roles than the app
  needs. *Fix:* set `fullScopeAllowed: false` and trim default client scopes to
  least privilege.

**Low**

- **L-1**: `keycloak/realm-export.json`: PKCE is not enforced on the client, so
  the authorization-code flow can run without it. *Fix:* set
  `pkce.code.challenge.method: S256` on the client.
- **L-2**: `backend/.../web/HelloController.java`: The endpoint logs the
  authenticated username, writing PII to application logs. *Fix:* drop the
  username from the log line (or log a non-identifying subject reference).
- **L-3**: `.env` / `docker-compose.yml`: The Keycloak admin password is a
  trivial value (`admin`). Even for local use, a guessable admin credential is
  worth avoiding. *Fix:* use a non-trivial dev password, still clearly marked
  dev-only.
- **L-4**: `keycloak/realm-export.json`: `ssoSessionMaxLifespan` is longer than
  this POC needs, widening the window a stolen session stays valid. *Fix:*
  shorten it to a value appropriate for the app.

**Overall:** One High (missing audience validation) is the priority; the Medium
items harden the logout and token lifecycle, and the Low items are quick
defense-in-depth wins. No Critical issues, and the confidential-client + scoped
CORS/redirect-URI baseline is sound.

---

> The exact findings depend on the current state of the code; treat this as an
> illustration of the format and depth, not a fixed checklist result.
