---
name: spring-oauth2-resource-server
description: Configure a Spring Boot app as an OAuth2 resource server that validates JWT access tokens against any OIDC provider (Keycloak, Auth0, Okta, Cognito, Entra ID). Sets up the security filter chain, JWT decoder with audience validation, CORS, config properties, and a slice test. Use when adding token-based API authentication to a Spring Boot service.
disable-model-invocation: true
---

# spring-oauth2-resource-server

Wire a Spring Boot application to accept and validate OAuth2/OIDC JWT access
tokens (resource-server role). This covers protecting an API with bearer tokens.
It does not configure the login/authorization-code flow (that is the client
role) or opaque-token introspection.

Provider-agnostic: it is driven entirely by an `issuer-uri`, so it works with
Keycloak, Auth0, Okta, Cognito, Entra ID, or any OIDC-compliant authorization
server.

## Before you start

Discover the target project's shape rather than assuming it (use Glob/Grep):

- **Build tool**: `build.gradle` / `build.gradle.kts` vs `pom.xml`, and whether
  Gradle uses a version catalog (`gradle/libs.versions.toml`).
- **Spring Boot version**: read it from the build file. It changes two test
  imports (see `references/dependencies.md`).
- **Base package**: the package under `src/main/java/...` holding the main
  `@SpringBootApplication` class. New classes go in a `config` subpackage of it.
- **Config format**: `application.yml` vs `application.properties`.

Then gather the values to plug in:

- **issuer-uri**: the OIDC issuer base URL.
- **audience**: the value expected in the token's `aud` claim (usually the API's
  client id / identifier).
- **allowed CORS origins**: the browser origins that call this API.

## Steps

Reference files live in this skill's `references/` directory. Copy them into the
project, then substitute `com.example.app` with the real base package and adjust
placeholders.

1. **Add dependencies.** Add `spring-boot-starter-oauth2-resource-server` (main)
   and `spring-security-test` (test) using the snippet in
   `references/dependencies.md` that matches the project's build tool.

2. **Add `SecurityConfig`.** Copy `references/SecurityConfig.java` into
   `<base-package>/config/`. It defines a stateless filter chain
   (`anyRequest().authenticated()`, `oauth2ResourceServer().jwt()`), CORS scoped
   to configured origins, and a `JwtDecoder` that adds audience validation on
   top of the default signature/issuer/expiry checks.

3. **Add `AudienceValidator`.** Copy `references/AudienceValidator.java` into the
   same `config/` package. Recommended: without it, a token minted for any other
   client of the same issuer is accepted. If you deliberately do not want
   audience checking, omit both this class and the `jwtDecoder` bean, and Spring
   auto-configures a decoder from `issuer-uri` alone.

4. **Add config properties.** Merge `references/application.yml` into the
   project's config (or translate to `.properties`), filling in `issuer-uri`,
   `audience`, and `allowed-origins`. Keep them env-overridable.

5. **Add a test.** Copy `references/SecurityConfigTest.java`, point
   `@WebMvcTest` at a protected controller, and set the request path. It proves
   anonymous requests get 401 and a valid JWT is accepted, without a live issuer
   (the `JwtDecoder` is mocked).

6. **Verify.** Build and run the test suite (`./gradlew test` or `mvn test`).
   Then confirm at runtime: a request with no token returns 401, and a request
   with a valid bearer token from the issuer returns 200.

## Notes

- **CSRF** is disabled in the template because a token-authenticated API holds no
  server-side session or auth cookie. If this same app also serves
  cookie/session-authenticated endpoints, do not blanket-disable CSRF.
- **Roles/scopes**: this sets up authentication (valid token required). To
  authorize by scope or role, add a `JwtAuthenticationConverter` and
  `.hasAuthority(...)` rules; out of scope here.
- **Follow-up**: run the `security-reviewer` agent afterward to audit the result
  (audience, CORS, issuer, token handling).
