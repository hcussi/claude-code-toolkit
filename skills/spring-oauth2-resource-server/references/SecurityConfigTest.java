package com.example.app.web;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
// Boot 4.x import. On Boot 3.x use:
// import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.security.oauth2.jwt.JwtDecoder;
// Boot 3.4+/Framework 6.2+. On older versions use @MockBean from
// org.springframework.boot.test.mock.mockito.MockBean.
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import com.example.app.config.SecurityConfig;

/**
 * Slice test for SecurityConfig: anonymous requests are 401, a request carrying
 * a (test) JWT is allowed. No live issuer is needed because the JwtDecoder is
 * mocked so the context loads without fetching JWKS, and spring-security-test's
 * jwt() post-processor injects a pre-authenticated token.
 *
 * Point @WebMvcTest at any protected controller in the target project and
 * replace com.example.app and the request path below.
 */
@WebMvcTest(YourController.class)
@Import(SecurityConfig.class)
class SecurityConfigTest {

    @Autowired
    MockMvc mockMvc;

    // Present only so the resource-server config loads without contacting the
    // issuer's JWKS endpoint during the test.
    @MockitoBean
    JwtDecoder jwtDecoder;

    @Test
    void anonymousRequestIsUnauthorized() throws Exception {
        mockMvc.perform(get("/your-endpoint"))
            .andExpect(status().isUnauthorized());
    }

    @Test
    void requestWithJwtIsAllowed() throws Exception {
        mockMvc.perform(get("/your-endpoint").with(jwt()))
            .andExpect(status().isOk());
    }
}
