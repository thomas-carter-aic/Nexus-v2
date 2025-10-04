package com.aic.aipaas.appmanagement.controller;

import com.aic.aipaas.appmanagement.model.Application;
import com.aic.aipaas.appmanagement.model.ApplicationRequest;
import com.aic.aipaas.appmanagement.model.ApplicationResponse;
import com.aic.aipaas.appmanagement.service.ApplicationService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * REST Controller for Application Management
 * Handles CRUD operations for AI applications in the AIC-AIPaaS platform
 */
@RestController
@RequestMapping("/api/v1/applications")
@Tag(name = "Application Management", description = "APIs for managing AI applications")
@Validated
@CrossOrigin(origins = "*", maxAge = 3600)
public class AppController {

    private static final Logger logger = LoggerFactory.getLogger(AppController.class);

    @Autowired
    private ApplicationService applicationService;

    /**
     * Get all applications with pagination
     */
    @GetMapping
    @Operation(summary = "Get all applications", description = "Retrieve all applications with pagination support")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved applications"),
        @ApiResponse(responseCode = "401", description = "Unauthorized"),
        @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public ResponseEntity<Page<ApplicationResponse>> getAllApplications(
            @Parameter(description = "Pagination information") Pageable pageable,
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String status) {
        
        logger.info("Fetching applications with search: {}, status: {}", search, status);
        
        try {
            Page<ApplicationResponse> applications = applicationService.getAllApplications(pageable, search, status);
            return ResponseEntity.ok(applications);
        } catch (Exception e) {
            logger.error("Error fetching applications", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Get application by ID
     */
    @GetMapping("/{id}")
    @Operation(summary = "Get application by ID", description = "Retrieve a specific application by its ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved application"),
        @ApiResponse(responseCode = "404", description = "Application not found"),
        @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public ResponseEntity<ApplicationResponse> getApplicationById(
            @Parameter(description = "Application ID") @PathVariable @NotNull UUID id) {
        
        logger.info("Fetching application with ID: {}", id);
        
        Optional<ApplicationResponse> application = applicationService.getApplicationById(id);
        return application.map(ResponseEntity::ok)
                         .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Create a new application
     */
    @PostMapping
    @Operation(summary = "Create new application", description = "Create a new AI application")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Application created successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request data"),
        @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public ResponseEntity<ApplicationResponse> createApplication(
            @Parameter(description = "Application creation request") @Valid @RequestBody ApplicationRequest request) {
        
        logger.info("Creating new application: {}", request.getName());
        
        try {
            ApplicationResponse createdApp = applicationService.createApplication(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(createdApp);
        } catch (IllegalArgumentException e) {
            logger.error("Invalid application data: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        } catch (Exception e) {
            logger.error("Error creating application", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Update an existing application
     */
    @PutMapping("/{id}")
    @Operation(summary = "Update application", description = "Update an existing application")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Application updated successfully"),
        @ApiResponse(responseCode = "404", description = "Application not found"),
        @ApiResponse(responseCode = "400", description = "Invalid request data"),
        @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public ResponseEntity<ApplicationResponse> updateApplication(
            @Parameter(description = "Application ID") @PathVariable @NotNull UUID id,
            @Parameter(description = "Application update request") @Valid @RequestBody ApplicationRequest request) {
        
        logger.info("Updating application with ID: {}", id);
        
        try {
            Optional<ApplicationResponse> updatedApp = applicationService.updateApplication(id, request);
            return updatedApp.map(ResponseEntity::ok)
                           .orElse(ResponseEntity.notFound().build());
        } catch (IllegalArgumentException e) {
            logger.error("Invalid application data: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        } catch (Exception e) {
            logger.error("Error updating application", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Delete an application
     */
    @DeleteMapping("/{id}")
    @Operation(summary = "Delete application", description = "Delete an application by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "Application deleted successfully"),
        @ApiResponse(responseCode = "404", description = "Application not found"),
        @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> deleteApplication(
            @Parameter(description = "Application ID") @PathVariable @NotNull UUID id) {
        
        logger.info("Deleting application with ID: {}", id);
        
        try {
            boolean deleted = applicationService.deleteApplication(id);
            return deleted ? ResponseEntity.noContent().build() 
                          : ResponseEntity.notFound().build();
        } catch (Exception e) {
            logger.error("Error deleting application", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Deploy an application
     */
    @PostMapping("/{id}/deploy")
    @Operation(summary = "Deploy application", description = "Deploy an application to the platform")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Application deployment initiated"),
        @ApiResponse(responseCode = "404", description = "Application not found"),
        @ApiResponse(responseCode = "409", description = "Application already deployed")
    })
    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public ResponseEntity<ApplicationResponse> deployApplication(
            @Parameter(description = "Application ID") @PathVariable @NotNull UUID id) {
        
        logger.info("Deploying application with ID: {}", id);
        
        try {
            Optional<ApplicationResponse> deployedApp = applicationService.deployApplication(id);
            return deployedApp.map(ResponseEntity::ok)
                            .orElse(ResponseEntity.notFound().build());
        } catch (IllegalStateException e) {
            logger.error("Application deployment conflict: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        } catch (Exception e) {
            logger.error("Error deploying application", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Stop an application
     */
    @PostMapping("/{id}/stop")
    @Operation(summary = "Stop application", description = "Stop a running application")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Application stopped successfully"),
        @ApiResponse(responseCode = "404", description = "Application not found"),
        @ApiResponse(responseCode = "409", description = "Application not running")
    })
    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public ResponseEntity<ApplicationResponse> stopApplication(
            @Parameter(description = "Application ID") @PathVariable @NotNull UUID id) {
        
        logger.info("Stopping application with ID: {}", id);
        
        try {
            Optional<ApplicationResponse> stoppedApp = applicationService.stopApplication(id);
            return stoppedApp.map(ResponseEntity::ok)
                           .orElse(ResponseEntity.notFound().build());
        } catch (IllegalStateException e) {
            logger.error("Application stop conflict: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        } catch (Exception e) {
            logger.error("Error stopping application", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Get application metrics
     */
    @GetMapping("/{id}/metrics")
    @Operation(summary = "Get application metrics", description = "Retrieve metrics for a specific application")
    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public ResponseEntity<Object> getApplicationMetrics(
            @Parameter(description = "Application ID") @PathVariable @NotNull UUID id,
            @RequestParam(defaultValue = "1h") String timeRange) {
        
        logger.info("Fetching metrics for application ID: {} with time range: {}", id, timeRange);
        
        try {
            Object metrics = applicationService.getApplicationMetrics(id, timeRange);
            return ResponseEntity.ok(metrics);
        } catch (Exception e) {
            logger.error("Error fetching application metrics", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * Health check endpoint
     */
    @GetMapping("/health")
    @Operation(summary = "Health check", description = "Check the health of the application management service")
    public ResponseEntity<Object> healthCheck() {
        return ResponseEntity.ok().body(Map.of(
            "status", "healthy",
            "service", "app-management",
            "timestamp", System.currentTimeMillis()
        ));
    }
}
