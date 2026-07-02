# spring-oauth2-resource-server

A user-invoked skill that configures a Spring Boot application as an OAuth2
**resource server**: it protects an API so every request must carry a valid
OIDC JWT access token, validated against a configured `issuer-uri`. It is
provider-agnostic (Keycloak, Auth0, Okta, Cognito, Entra ID, or any
OIDC-compliant server) and does not touch the login/authorization-code flow.

**Skill file:** [`skills/spring-oauth2-resource-server/SKILL.md`](../../skills/spring-oauth2-resource-server/SKILL.md)

## What it sets up

- The `spring-boot-starter-oauth2-resource-server` dependency (Gradle, version
  catalog, or Maven).
- A `SecurityConfig`: stateless filter chain (`anyRequest().authenticated()`,
  `oauth2ResourceServer().jwt()`), CORS scoped to configured origins, and a
  `JwtDecoder` bean.
- An `AudienceValidator` wired via `DelegatingOAuth2TokenValidator`, so tokens
  minted for other clients of the same issuer are rejected (confused-deputy
  guard). Optional but recommended.
- Config properties (`issuer-uri`, `audience`, CORS origins), env-overridable.
- A `@WebMvcTest` slice test proving 401 for anonymous requests and 200 for a
  valid JWT, using a mocked `JwtDecoder` so no live issuer is needed.

The skill bundles these as ready-to-adapt reference files under
`skills/spring-oauth2-resource-server/references/`; it discovers the target
project's build tool, Boot version, base package, and config format rather than
assuming them.

## Scope

Resource-server (API) role only. Out of scope: the OAuth2 client/login flow,
opaque-token introspection, and scope/role-based authorization (the skill notes
how to extend to the latter with a `JwtAuthenticationConverter`).

## Usage

Copy the skill directory into a project's `.claude/skills/` (or
`~/.claude/skills/` to make it available everywhere), then invoke it as
`/spring-oauth2-resource-server`. It is user-invoked only, since it writes files.

## Example

Invoked against a Spring Boot 4 service with base package `com.acme.orders` and
Keycloak as the issuer, it would:

1. Add the resource-server starter to `build.gradle` and `spring-security-test`
   to the test dependencies.
2. Create `com/acme/orders/config/SecurityConfig.java` and
   `com/acme/orders/config/AudienceValidator.java`.
3. Add `issuer-uri`, `audience`, and CORS origins to `application.yml`, wired to
   `OAUTH2_ISSUER_URI`, `OAUTH2_AUDIENCE`, and `CORS_ALLOWED_ORIGINS`.
4. Add a `SecurityConfigTest` pointed at an existing protected controller.
5. Suggest running `./gradlew test` and then the `security-reviewer` agent to
   audit the result.

This mirrors the setup in the
[`nextjs-springboot-keycloak-poc`](https://github.com/hcussi/nextjs-springboot-keycloak-poc)
backend, which is where the reference files were generalized from.
