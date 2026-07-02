# Dependencies

Add the OAuth2 resource-server starter. Spring Boot's BOM manages the version,
so declare it by module only. For tests, add `spring-security-test`.

## Gradle (Groovy DSL)

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-oauth2-resource-server'

    testImplementation 'org.springframework.security:spring-security-test'
}
```

## Gradle (version catalog: gradle/libs.versions.toml)

```toml
[libraries]
spring-boot-starter-oauth2-resource-server = { module = "org.springframework.boot:spring-boot-starter-oauth2-resource-server" }
spring-security-test = { module = "org.springframework.security:spring-security-test" }
```

```groovy
dependencies {
    implementation libs.spring.boot.starter.oauth2.resource.server
    testImplementation libs.spring.security.test
}
```

## Maven

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-test</artifactId>
    <scope>test</scope>
</dependency>
```

## Notes on Spring Boot version

The Java config in this skill targets Spring Security 6.x (Spring Boot 3.x and
4.x). Two things differ by version, both used by the test template:

- `@MockitoBean` (mock a bean in a slice test) needs Spring Framework 6.2+
  (Boot 3.4+). On older versions use `@MockBean` instead.
- The `@WebMvcTest` import moved in Boot 4:
  - Boot 4.x: `org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest`
  - Boot 3.x: `org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest`
