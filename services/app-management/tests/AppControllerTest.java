package com.aic.aipaas.appmanagement.controller;

import com.aic.aipaas.appmanagement.model.ApplicationRequest;
import com.aic.aipaas.appmanagement.model.ApplicationResponse;
import com.aic.aipaas.appmanagement.service.ApplicationService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Test class for AppController
 * Tests all REST endpoints for application management
 */
@ExtendWith(MockitoExtension.class)
@WebMvcTest(AppController.class)
class AppControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ApplicationService applicationService;

    @Autowired
    private ObjectMapper objectMapper;

    private ApplicationResponse mockApplication;
    private ApplicationRequest mockRequest;
    private UUID testId;

    @BeforeEach
    void setUp() {
        testId = UUID.randomUUID();
        
        mockApplication = ApplicationResponse.builder()
                .id(testId)
                .name("Test Application")
                .description("Test Description")
                .version("1.0.0")
                .status("RUNNING")
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();

        mockRequest = ApplicationRequest.builder()
                .name("Test Application")
                .description("Test Description")
                .version("1.0.0")
                .dockerImage("test/app:latest")
                .build();
    }

    @Test
    @WithMockUser(roles = "USER")
    void getAllApplications_ShouldReturnPagedApplications() throws Exception {
        // Given
        List<ApplicationResponse> applications = Arrays.asList(mockApplication);
        Page<ApplicationResponse> page = new PageImpl<>(applications, PageRequest.of(0, 10), 1);
        
        when(applicationService.getAllApplications(any(Pageable.class), isNull(), isNull()))
                .thenReturn(page);

        // When & Then
        mockMvc.perform(get("/api/v1/applications")
                .param("page", "0")
                .param("size", "10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content[0].name").value("Test Application"))
                .andExpect(jsonPath("$.totalElements").value(1));

        verify(applicationService).getAllApplications(any(Pageable.class), isNull(), isNull());
    }

    @Test
    @WithMockUser(roles = "USER")
    void getAllApplications_WithSearchAndStatus_ShouldReturnFilteredResults() throws Exception {
        // Given
        List<ApplicationResponse> applications = Arrays.asList(mockApplication);
        Page<ApplicationResponse> page = new PageImpl<>(applications, PageRequest.of(0, 10), 1);
        
        when(applicationService.getAllApplications(any(Pageable.class), eq("test"), eq("RUNNING")))
                .thenReturn(page);

        // When & Then
        mockMvc.perform(get("/api/v1/applications")
                .param("search", "test")
                .param("status", "RUNNING"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].status").value("RUNNING"));

        verify(applicationService).getAllApplications(any(Pageable.class), eq("test"), eq("RUNNING"));
    }

    @Test
    @WithMockUser(roles = "USER")
    void getApplicationById_WhenExists_ShouldReturnApplication() throws Exception {
        // Given
        when(applicationService.getApplicationById(testId))
                .thenReturn(Optional.of(mockApplication));

        // When & Then
        mockMvc.perform(get("/api/v1/applications/{id}", testId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(testId.toString()))
                .andExpect(jsonPath("$.name").value("Test Application"));

        verify(applicationService).getApplicationById(testId);
    }

    @Test
    @WithMockUser(roles = "USER")
    void getApplicationById_WhenNotExists_ShouldReturn404() throws Exception {
        // Given
        when(applicationService.getApplicationById(testId))
                .thenReturn(Optional.empty());

        // When & Then
        mockMvc.perform(get("/api/v1/applications/{id}", testId))
                .andExpect(status().isNotFound());

        verify(applicationService).getApplicationById(testId);
    }

    @Test
    @WithMockUser(roles = "USER")
    void createApplication_WithValidData_ShouldReturnCreatedApplication() throws Exception {
        // Given
        when(applicationService.createApplication(any(ApplicationRequest.class)))
                .thenReturn(mockApplication);

        // When & Then
        mockMvc.perform(post("/api/v1/applications")
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(mockRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("Test Application"));

        verify(applicationService).createApplication(any(ApplicationRequest.class));
    }

    @Test
    @WithMockUser(roles = "USER")
    void createApplication_WithInvalidData_ShouldReturn400() throws Exception {
        // Given
        ApplicationRequest invalidRequest = ApplicationRequest.builder()
                .name("") // Invalid empty name
                .build();

        // When & Then
        mockMvc.perform(post("/api/v1/applications")
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest());

        verify(applicationService, never()).createApplication(any());
    }

    @Test
    @WithMockUser(roles = "USER")
    void updateApplication_WhenExists_ShouldReturnUpdatedApplication() throws Exception {
        // Given
        when(applicationService.updateApplication(eq(testId), any(ApplicationRequest.class)))
                .thenReturn(Optional.of(mockApplication));

        // When & Then
        mockMvc.perform(put("/api/v1/applications/{id}", testId)
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(mockRequest)))
                .andExpected(status().isOk())
                .andExpect(jsonPath("$.name").value("Test Application"));

        verify(applicationService).updateApplication(eq(testId), any(ApplicationRequest.class));
    }

    @Test
    @WithMockUser(roles = "USER")
    void updateApplication_WhenNotExists_ShouldReturn404() throws Exception {
        // Given
        when(applicationService.updateApplication(eq(testId), any(ApplicationRequest.class)))
                .thenReturn(Optional.empty());

        // When & Then
        mockMvc.perform(put("/api/v1/applications/{id}", testId)
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(mockRequest)))
                .andExpect(status().isNotFound());

        verify(applicationService).updateApplication(eq(testId), any(ApplicationRequest.class));
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void deleteApplication_WhenExists_ShouldReturn204() throws Exception {
        // Given
        when(applicationService.deleteApplication(testId))
                .thenReturn(true);

        // When & Then
        mockMvc.perform(delete("/api/v1/applications/{id}", testId)
                .with(csrf()))
                .andExpect(status().isNoContent());

        verify(applicationService).deleteApplication(testId);
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void deleteApplication_WhenNotExists_ShouldReturn404() throws Exception {
        // Given
        when(applicationService.deleteApplication(testId))
                .thenReturn(false);

        // When & Then
        mockMvc.perform(delete("/api/v1/applications/{id}", testId)
                .with(csrf()))
                .andExpect(status().isNotFound());

        verify(applicationService).deleteApplication(testId);
    }

    @Test
    @WithMockUser(roles = "USER")
    void deleteApplication_WithUserRole_ShouldReturn403() throws Exception {
        // When & Then
        mockMvc.perform(delete("/api/v1/applications/{id}", testId)
                .with(csrf()))
                .andExpect(status().isForbidden());

        verify(applicationService, never()).deleteApplication(any());
    }

    @Test
    @WithMockUser(roles = "USER")
    void deployApplication_WhenExists_ShouldReturnDeployedApplication() throws Exception {
        // Given
        ApplicationResponse deployedApp = mockApplication.toBuilder()
                .status("DEPLOYING")
                .build();
        
        when(applicationService.deployApplication(testId))
                .thenReturn(Optional.of(deployedApp));

        // When & Then
        mockMvc.perform(post("/api/v1/applications/{id}/deploy", testId)
                .with(csrf()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("DEPLOYING"));

        verify(applicationService).deployApplication(testId);
    }

    @Test
    @WithMockUser(roles = "USER")
    void deployApplication_WhenAlreadyDeployed_ShouldReturn409() throws Exception {
        // Given
        when(applicationService.deployApplication(testId))
                .thenThrow(new IllegalStateException("Application already deployed"));

        // When & Then
        mockMvc.perform(post("/api/v1/applications/{id}/deploy", testId)
                .with(csrf()))
                .andExpect(status().isConflict());

        verify(applicationService).deployApplication(testId);
    }

    @Test
    @WithMockUser(roles = "USER")
    void stopApplication_WhenRunning_ShouldReturnStoppedApplication() throws Exception {
        // Given
        ApplicationResponse stoppedApp = mockApplication.toBuilder()
                .status("STOPPED")
                .build();
        
        when(applicationService.stopApplication(testId))
                .thenReturn(Optional.of(stoppedApp));

        // When & Then
        mockMvc.perform(post("/api/v1/applications/{id}/stop", testId)
                .with(csrf()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("STOPPED"));

        verify(applicationService).stopApplication(testId);
    }

    @Test
    @WithMockUser(roles = "USER")
    void getApplicationMetrics_ShouldReturnMetrics() throws Exception {
        // Given
        Object mockMetrics = Map.of(
            "cpu_usage", 45.2,
            "memory_usage", 67.8,
            "requests_per_second", 120
        );
        
        when(applicationService.getApplicationMetrics(testId, "1h"))
                .thenReturn(mockMetrics);

        // When & Then
        mockMvc.perform(get("/api/v1/applications/{id}/metrics", testId)
                .param("timeRange", "1h"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.cpu_usage").value(45.2));

        verify(applicationService).getApplicationMetrics(testId, "1h");
    }

    @Test
    void healthCheck_ShouldReturnHealthStatus() throws Exception {
        // When & Then
        mockMvc.perform(get("/api/v1/applications/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("healthy"))
                .andExpect(jsonPath("$.service").value("app-management"));
    }

    @Test
    void getAllApplications_WithoutAuthentication_ShouldReturn401() throws Exception {
        // When & Then
        mockMvc.perform(get("/api/v1/applications"))
                .andExpect(status().isUnauthorized());

        verify(applicationService, never()).getAllApplications(any(), any(), any());
    }
}
