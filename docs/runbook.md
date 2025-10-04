# Operations Runbook - AIC AI Platform

## Overview

This runbook provides operational procedures, troubleshooting guides, and maintenance tasks for the AIC AI Platform (AIC-AIPaaS). It's designed for DevOps engineers, SREs, and operations teams.

## System Overview

### Architecture Summary
- **Microservices**: Authentication, Application Management
- **AI Services**: Model Training, Inference, Synthetic Data
- **Data Services**: Data Catalog, Schema Management
- **Infrastructure**: Kubernetes (EKS/AKS), Istio Service Mesh
- **Monitoring**: Prometheus, Grafana, Jaeger
- **Databases**: PostgreSQL, Redis

### Key Metrics
- **Availability Target**: 99.9% uptime
- **Response Time**: < 200ms for API calls
- **Throughput**: 10,000 requests/minute
- **Error Rate**: < 0.1%

## Monitoring and Alerting

### Monitoring Stack

#### Prometheus Metrics
- **System Metrics**: CPU, Memory, Disk, Network
- **Application Metrics**: Request rate, latency, errors
- **Business Metrics**: User registrations, model predictions
- **Infrastructure Metrics**: Kubernetes cluster health

#### Key Dashboards
- **System Overview**: http://grafana.aic-aipaas.local/d/system-overview
- **Application Health**: http://grafana.aic-aipaas.local/d/app-health
- **AI/ML Metrics**: http://grafana.aic-aipaas.local/d/ai-metrics
- **Database Performance**: http://grafana.aic-aipaas.local/d/db-performance

#### Alert Channels
- **Critical**: PagerDuty, Slack #alerts-critical
- **Warning**: Slack #alerts-warning, Email
- **Info**: Slack #alerts-info

### Critical Alerts

#### High Priority Alerts

**Service Down**
- **Trigger**: Service unavailable for > 2 minutes
- **Impact**: Complete service outage
- **Response Time**: Immediate (< 5 minutes)

**High Error Rate**
- **Trigger**: Error rate > 5% for > 5 minutes
- **Impact**: Degraded user experience
- **Response Time**: < 15 minutes

**Database Connection Issues**
- **Trigger**: Database connection pool > 90% for > 2 minutes
- **Impact**: Service degradation or failure
- **Response Time**: < 10 minutes

#### Medium Priority Alerts

**High CPU Usage**
- **Trigger**: CPU usage > 80% for > 10 minutes
- **Impact**: Performance degradation
- **Response Time**: < 30 minutes

**High Memory Usage**
- **Trigger**: Memory usage > 85% for > 10 minutes
- **Impact**: Potential service instability
- **Response Time**: < 30 minutes

**Disk Space Low**
- **Trigger**: Disk usage > 85%
- **Impact**: Service may fail to write data
- **Response Time**: < 1 hour

## Incident Response

### Incident Severity Levels

#### Severity 1 (Critical)
- **Definition**: Complete service outage or data loss
- **Response Time**: < 15 minutes
- **Resolution Time**: < 4 hours
- **Escalation**: Immediate management notification

#### Severity 2 (High)
- **Definition**: Major functionality impaired
- **Response Time**: < 1 hour
- **Resolution Time**: < 24 hours
- **Escalation**: Management notification within 2 hours

#### Severity 3 (Medium)
- **Definition**: Minor functionality impaired
- **Response Time**: < 4 hours
- **Resolution Time**: < 72 hours
- **Escalation**: Daily status updates

#### Severity 4 (Low)
- **Definition**: Cosmetic issues or minor bugs
- **Response Time**: < 24 hours
- **Resolution Time**: Next release cycle
- **Escalation**: Weekly status updates

### Incident Response Process

1. **Detection**: Alert received or issue reported
2. **Assessment**: Determine severity and impact
3. **Response**: Assemble response team
4. **Investigation**: Identify root cause
5. **Resolution**: Implement fix
6. **Communication**: Update stakeholders
7. **Post-mortem**: Document lessons learned

### Emergency Contacts

```
Role                    Primary             Secondary
On-Call Engineer       +1-555-0101         +1-555-0102
DevOps Lead           +1-555-0201         +1-555-0202
Platform Architect    +1-555-0301         +1-555-0302
Engineering Manager   +1-555-0401         +1-555-0402
```

## Service Management

### Service Health Checks

#### Authentication Service
```bash
# Health check
curl -f http://auth-service:8000/health

# Detailed status
curl http://auth-service:8000/auth/status

# Kubernetes health check
kubectl get pods -n microservices -l app=auth-service
kubectl describe pod <pod-name> -n microservices
```

#### Application Management Service
```bash
# Health check
curl -f http://app-management-service:8080/actuator/health

# Metrics endpoint
curl http://app-management-service:8080/actuator/metrics

# Kubernetes health check
kubectl get pods -n microservices -l app=app-management-service
```

### Service Restart Procedures

#### Rolling Restart
```bash
# Restart deployment
kubectl rollout restart deployment/auth-service -n microservices
kubectl rollout restart deployment/app-management-service -n microservices

# Check rollout status
kubectl rollout status deployment/auth-service -n microservices
```

#### Emergency Restart
```bash
# Scale down to 0
kubectl scale deployment/auth-service --replicas=0 -n microservices

# Scale back up
kubectl scale deployment/auth-service --replicas=3 -n microservices
```

### Configuration Management

#### Environment Variables
```bash
# View current configuration
kubectl get configmap app-config -n microservices -o yaml

# Update configuration
kubectl edit configmap app-config -n microservices

# Restart pods to pick up changes
kubectl rollout restart deployment/auth-service -n microservices
```

#### Secrets Management
```bash
# View secrets (values are base64 encoded)
kubectl get secrets app-secrets -n microservices -o yaml

# Update secret
kubectl create secret generic app-secrets \
  --from-literal=jwt-secret=new-secret-value \
  --dry-run=client -o yaml | kubectl apply -f -
```

## Database Operations

### PostgreSQL Management

#### Connection and Status
```bash
# Connect to database
kubectl exec -it postgresql-0 -n data-services -- psql -U postgres

# Check database status
kubectl exec -it postgresql-0 -n data-services -- pg_isready

# View active connections
kubectl exec -it postgresql-0 -n data-services -- psql -U postgres -c "SELECT * FROM pg_stat_activity;"
```

#### Backup and Restore
```bash
# Create backup
kubectl exec -it postgresql-0 -n data-services -- pg_dump -U postgres aic_aipaas > backup.sql

# Restore from backup
kubectl exec -i postgresql-0 -n data-services -- psql -U postgres aic_aipaas < backup.sql

# Automated backup (using CronJob)
kubectl apply -f infrastructure/kubernetes/backup-cronjob.yaml
```

#### Performance Monitoring
```bash
# Check slow queries
kubectl exec -it postgresql-0 -n data-services -- psql -U postgres -c "
SELECT query, mean_time, calls, total_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;"

# Check database size
kubectl exec -it postgresql-0 -n data-services -- psql -U postgres -c "
SELECT datname, pg_size_pretty(pg_database_size(datname)) 
FROM pg_database 
ORDER BY pg_database_size(datname) DESC;"
```

### Redis Management

#### Connection and Status
```bash
# Connect to Redis
kubectl exec -it redis-0 -n data-services -- redis-cli

# Check Redis status
kubectl exec -it redis-0 -n data-services -- redis-cli ping

# View Redis info
kubectl exec -it redis-0 -n data-services -- redis-cli info
```

#### Memory Management
```bash
# Check memory usage
kubectl exec -it redis-0 -n data-services -- redis-cli info memory

# Clear cache (use with caution)
kubectl exec -it redis-0 -n data-services -- redis-cli flushall

# Set memory policy
kubectl exec -it redis-0 -n data-services -- redis-cli config set maxmemory-policy allkeys-lru
```

## Kubernetes Operations

### Cluster Management

#### Node Management
```bash
# View node status
kubectl get nodes -o wide

# Describe node
kubectl describe node <node-name>

# Drain node for maintenance
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Uncordon node
kubectl uncordon <node-name>
```

#### Resource Management
```bash
# View resource usage
kubectl top nodes
kubectl top pods --all-namespaces

# Check resource quotas
kubectl get resourcequota --all-namespaces

# View persistent volumes
kubectl get pv,pvc --all-namespaces
```

### Pod Management

#### Pod Troubleshooting
```bash
# View pod logs
kubectl logs <pod-name> -n <namespace> --tail=100 -f

# Execute commands in pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash

# Port forward for debugging
kubectl port-forward <pod-name> 8080:8080 -n <namespace>

# Copy files to/from pod
kubectl cp <local-file> <namespace>/<pod-name>:<remote-file>
```

#### Pod Debugging
```bash
# Debug pod with temporary container
kubectl debug <pod-name> -n <namespace> --image=busybox --target=<container-name>

# Create debug pod
kubectl run debug-pod --image=busybox --rm -it --restart=Never -- /bin/sh
```

### Networking

#### Service Discovery
```bash
# View services
kubectl get svc --all-namespaces

# Test service connectivity
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nslookup <service-name>.<namespace>.svc.cluster.local

# Check endpoints
kubectl get endpoints <service-name> -n <namespace>
```

#### Ingress Management
```bash
# View ingress resources
kubectl get ingress --all-namespaces

# Check ingress controller logs
kubectl logs -n istio-system -l app=istio-ingressgateway

# Test ingress connectivity
curl -H "Host: auth.aic-aipaas.local" http://<ingress-ip>/health
```

## Performance Tuning

### Application Performance

#### JVM Tuning (Java Services)
```bash
# Update JVM options in deployment
kubectl patch deployment app-management-service -n microservices -p '
{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "app-management-service",
          "env": [{
            "name": "JAVA_OPTS",
            "value": "-Xmx1g -Xms512m -XX:+UseG1GC"
          }]
        }]
      }
    }
  }
}'
```

#### Python Performance (FastAPI Services)
```bash
# Update worker configuration
kubectl patch deployment auth-service -n microservices -p '
{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "auth-service",
          "env": [{
            "name": "WORKERS",
            "value": "4"
          }]
        }]
      }
    }
  }
}'
```

### Database Performance

#### PostgreSQL Tuning
```sql
-- Optimize for read-heavy workloads
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET random_page_cost = 1.1;

-- Reload configuration
SELECT pg_reload_conf();
```

#### Connection Pool Tuning
```yaml
# Update connection pool settings
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
```

## Security Operations

### Certificate Management

#### TLS Certificate Renewal
```bash
# Check certificate expiration
kubectl get certificates --all-namespaces

# Force certificate renewal
kubectl delete certificate <cert-name> -n <namespace>

# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager
```

#### Secret Rotation
```bash
# Rotate JWT secret
kubectl create secret generic auth-secrets \
  --from-literal=jwt-secret=$(openssl rand -base64 32) \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart services to pick up new secret
kubectl rollout restart deployment/auth-service -n microservices
```

### Security Monitoring

#### Audit Logs
```bash
# View Kubernetes audit logs
kubectl logs -n kube-system -l component=kube-apiserver | grep audit

# Check for suspicious activities
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | grep -i "error\|failed\|unauthorized"
```

#### Network Policies
```bash
# View network policies
kubectl get networkpolicies --all-namespaces

# Test network connectivity
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nc -zv <service-name> <port>
```

## Backup and Recovery

### Backup Procedures

#### Database Backup
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
kubectl exec postgresql-0 -n data-services -- pg_dump -U postgres aic_aipaas | \
  gzip > "backup_${DATE}.sql.gz"

# Upload to S3
aws s3 cp "backup_${DATE}.sql.gz" s3://aic-aipaas-backups/database/
```

#### Configuration Backup
```bash
# Backup all Kubernetes resources
kubectl get all --all-namespaces -o yaml > cluster-backup.yaml

# Backup specific namespace
kubectl get all -n microservices -o yaml > microservices-backup.yaml
```

### Recovery Procedures

#### Service Recovery
```bash
# Restore from backup
kubectl apply -f microservices-backup.yaml

# Verify services are running
kubectl get pods -n microservices
kubectl get svc -n microservices
```

#### Database Recovery
```bash
# Restore database from backup
gunzip -c backup_20250115_120000.sql.gz | \
  kubectl exec -i postgresql-0 -n data-services -- psql -U postgres aic_aipaas
```

## Maintenance Tasks

### Regular Maintenance

#### Daily Tasks
- [ ] Check system health dashboards
- [ ] Review error logs and alerts
- [ ] Verify backup completion
- [ ] Monitor resource usage

#### Weekly Tasks
- [ ] Update security patches
- [ ] Review performance metrics
- [ ] Clean up old logs and backups
- [ ] Test disaster recovery procedures

#### Monthly Tasks
- [ ] Review and update documentation
- [ ] Conduct security audit
- [ ] Performance optimization review
- [ ] Capacity planning assessment

### Scheduled Maintenance

#### Maintenance Window
- **Time**: Sundays 2:00 AM - 4:00 AM UTC
- **Duration**: 2 hours maximum
- **Notification**: 48 hours advance notice

#### Maintenance Checklist
1. [ ] Notify stakeholders
2. [ ] Create maintenance branch
3. [ ] Backup critical data
4. [ ] Apply updates/patches
5. [ ] Run smoke tests
6. [ ] Monitor system health
7. [ ] Update documentation
8. [ ] Send completion notification

## Troubleshooting Guide

### Common Issues

#### Service Won't Start
```bash
# Check pod status
kubectl describe pod <pod-name> -n <namespace>

# Check logs
kubectl logs <pod-name> -n <namespace> --previous

# Common fixes:
# 1. Check resource limits
# 2. Verify configuration
# 3. Check dependencies
# 4. Validate secrets
```

#### High Memory Usage
```bash
# Identify memory-consuming pods
kubectl top pods --all-namespaces --sort-by=memory

# Check memory limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Limits"

# Solutions:
# 1. Increase memory limits
# 2. Optimize application code
# 3. Add more replicas
# 4. Enable horizontal pod autoscaling
```

#### Database Connection Issues
```bash
# Check database status
kubectl get pods -n data-services -l app=postgresql

# Test connectivity
kubectl run test-db --image=postgres:13 --rm -it --restart=Never -- \
  psql -h postgresql.data-services.svc.cluster.local -U postgres

# Common fixes:
# 1. Check connection pool settings
# 2. Verify database credentials
# 3. Check network policies
# 4. Restart database service
```

#### SSL/TLS Issues
```bash
# Check certificate status
kubectl get certificates --all-namespaces

# View certificate details
kubectl describe certificate <cert-name> -n <namespace>

# Test SSL connectivity
openssl s_client -connect <hostname>:443 -servername <hostname>

# Common fixes:
# 1. Renew expired certificates
# 2. Update DNS records
# 3. Check cert-manager configuration
# 4. Verify ingress configuration
```

### Emergency Procedures

#### Complete System Outage
1. **Assess Impact**: Determine scope of outage
2. **Activate Incident Response**: Page on-call team
3. **Check Infrastructure**: Verify cloud provider status
4. **Restore Services**: Follow service restoration order
5. **Communicate**: Update status page and stakeholders
6. **Monitor**: Watch for cascading failures

#### Data Corruption
1. **Stop Writes**: Prevent further corruption
2. **Assess Damage**: Determine extent of corruption
3. **Restore from Backup**: Use most recent clean backup
4. **Validate Data**: Verify data integrity
5. **Resume Operations**: Gradually restore service
6. **Post-Incident**: Conduct thorough post-mortem

## Contact Information

### Escalation Matrix

| Level | Role | Contact | Response Time |
|-------|------|---------|---------------|
| L1 | On-Call Engineer | +1-555-0101 | 15 minutes |
| L2 | Senior Engineer | +1-555-0201 | 30 minutes |
| L3 | Engineering Lead | +1-555-0301 | 1 hour |
| L4 | Engineering Manager | +1-555-0401 | 2 hours |

### Communication Channels

- **Slack**: #aic-aipaas-ops
- **Email**: ops@aic-aipaas.com
- **Status Page**: https://status.aic-aipaas.com
- **Documentation**: https://docs.aic-aipaas.com

## References

- [Architecture Documentation](architecture.md)
- [Developer Guide](developer-guide.md)
- [API Specifications](api-specs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Istio Documentation](https://istio.io/latest/docs/)
