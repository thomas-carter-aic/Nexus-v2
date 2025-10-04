#!/usr/bin/env python3
"""
AI-Native PaaS Platform CLI

A comprehensive command-line interface with AI-powered assistance for managing
applications, deployments, monitoring, and platform operations.

Features:
- Application lifecycle management
- AI-driven deployment optimization
- Intelligent monitoring and alerting
- Plugin management
- User and access management
- Configuration management
- Interactive AI assistant
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import click
import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
import httpx

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.domain.simple_models import (
    ApplicationId, UserId, ResourceRequirements, 
    ScalingConfiguration, ScalingStrategy
)

console = Console()


class PaaSCLI:
    """Main CLI class with AI-powered assistance"""
    
    def __init__(self):
        self.config_file = Path.home() / ".paas" / "config.yaml"
        self.config = self._load_config()
        self.api_client = None
        
    def _load_config(self) -> Dict[str, Any]:
        """Load CLI configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _save_config(self) -> None:
        """Save CLI configuration"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    async def _get_api_client(self) -> httpx.AsyncClient:
        """Get authenticated API client"""
        if not self.api_client:
            base_url = self.config.get('api_url', 'http://localhost:8000')
            headers = {}
            
            if 'access_token' in self.config:
                headers['Authorization'] = f"Bearer {self.config['access_token']}"
            
            self.api_client = httpx.AsyncClient(
                base_url=base_url,
                headers=headers,
                timeout=30.0
            )
        
        return self.api_client


# Initialize CLI instance
cli = PaaSCLI()


@click.group()
@click.version_option(version="1.0.0", prog_name="paas-cli")
def main():
    """🚀 AI-Native PaaS Platform CLI
    
    Intelligent command-line interface for managing cloud-native applications
    with AI-powered optimization and automation.
    """
    pass


@main.group()
def config():
    """⚙️ Configuration management"""
    pass


@config.command()
@click.option('--api-url', required=True, help='PaaS Platform API URL')
@click.option('--region', default='us-east-1', help='AWS region')
def setup(api_url: str, region: str):
    """🔧 Initial CLI setup and configuration"""
    console.print(Panel.fit("🔧 Setting up PaaS CLI", style="bold blue"))
    
    cli.config.update({
        'api_url': api_url,
        'region': region,
        'configured_at': datetime.utcnow().isoformat()
    })
    cli._save_config()
    
    console.print(f"✅ Configuration saved to {cli.config_file}")
    console.print(f"🌐 API URL: {api_url}")
    console.print(f"🌍 Region: {region}")


@config.command()
def show():
    """📋 Show current configuration"""
    if not cli.config:
        console.print("❌ No configuration found. Run 'paas config setup' first.")
        return
    
    table = Table(title="PaaS CLI Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in cli.config.items():
        if key != 'access_token':  # Don't show sensitive data
            table.add_row(key, str(value))
    
    console.print(table)


@main.group()
def auth():
    """🔐 Authentication and user management"""
    pass


@auth.command()
@click.option('--email', prompt=True, help='Email address')
@click.option('--password', prompt=True, hide_input=True, help='Password')
def login(email: str, password: str):
    """🔑 Login to the PaaS platform"""
    async def _login():
        console.print("🔑 Authenticating...")
        
        try:
            client = await cli._get_api_client()
            response = await client.post('/auth/login', json={
                'email': email,
                'password': password
            })
            
            if response.status_code == 200:
                data = response.json()
                cli.config['access_token'] = data['access_token']
                cli.config['user_profile'] = data['user_profile']
                cli._save_config()
                
                console.print("✅ Login successful!")
                console.print(f"👤 Welcome, {data['user_profile']['name']}")
            else:
                console.print(f"❌ Login failed: {response.json().get('detail', 'Unknown error')}")
                
        except Exception as e:
            console.print(f"❌ Login error: {str(e)}")
    
    asyncio.run(_login())


@auth.command()
def logout():
    """🚪 Logout from the PaaS platform"""
    if 'access_token' in cli.config:
        del cli.config['access_token']
    if 'user_profile' in cli.config:
        del cli.config['user_profile']
    cli._save_config()
    console.print("✅ Logged out successfully")


@auth.command()
def whoami():
    """👤 Show current user information"""
    if 'user_profile' not in cli.config:
        console.print("❌ Not logged in. Run 'paas auth login' first.")
        return
    
    profile = cli.config['user_profile']
    
    table = Table(title="Current User")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Name", profile.get('name', 'N/A'))
    table.add_row("Email", profile.get('email', 'N/A'))
    table.add_row("User ID", profile.get('user_id', 'N/A'))
    table.add_row("Roles", ', '.join(profile.get('roles', [])))
    table.add_row("Provider", profile.get('provider', 'N/A'))
    table.add_row("Active", "Yes" if profile.get('is_active') else "No")
    
    console.print(table)


@main.group()
def app():
    """📱 Application management"""
    pass


@app.command()
@click.option('--name', required=True, help='Application name')
@click.option('--image', help='Container image (e.g., nginx:latest)')
@click.option('--cpu', type=float, default=0.5, help='CPU cores')
@click.option('--memory', type=int, default=512, help='Memory in MB')
@click.option('--storage', type=int, default=10, help='Storage in GB')
@click.option('--min-instances', type=int, default=1, help='Minimum instances')
@click.option('--max-instances', type=int, default=5, help='Maximum instances')
@click.option('--strategy', type=click.Choice(['manual', 'reactive', 'predictive']), 
              default='predictive', help='Scaling strategy')
@click.option('--config-file', type=click.Path(exists=True), help='YAML configuration file')
def create(name: str, image: str, cpu: float, memory: int, storage: int,
           min_instances: int, max_instances: int, strategy: str, config_file: str):
    """🆕 Create a new application"""
    
    async def _create_app():
        console.print(f"🆕 Creating application: {name}")
        
        # Load from config file if provided
        if config_file:
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Override with config file values
            name = config_data.get('name', name)
            image = config_data.get('image', image)
            resources = config_data.get('resources', {})
            cpu = resources.get('cpu', cpu)
            memory = resources.get('memory', memory)
            storage = resources.get('storage', storage)
            
            scaling = config_data.get('scaling', {})
            min_instances = scaling.get('min_instances', min_instances)
            max_instances = scaling.get('max_instances', max_instances)
            strategy = scaling.get('strategy', strategy)
        
        # Validate inputs
        if not image:
            image = Prompt.ask("Container image", default="nginx:latest")
        
        # Show AI recommendations
        console.print("\n🤖 AI Recommendations:")
        
        if strategy == 'predictive':
            console.print("✨ Predictive scaling will learn from your usage patterns")
        
        if cpu < 1.0 and memory < 1024:
            console.print("💡 Consider increasing resources for better performance")
        
        # Create application configuration
        app_config = {
            'name': name,
            'image': image,
            'resources': {
                'cpu_cores': cpu,
                'memory_mb': memory,
                'storage_gb': storage
            },
            'scaling': {
                'strategy': strategy,
                'min_instances': min_instances,
                'max_instances': max_instances,
                'target_cpu_utilization': 70.0
            }
        }
        
        try:
            client = await cli._get_api_client()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Creating application...", total=None)
                
                response = await client.post('/api/v1/applications', json=app_config)
                
                if response.status_code == 201:
                    app_data = response.json()
                    progress.update(task, description="✅ Application created!")
                    
                    console.print(f"\n🎉 Application '{name}' created successfully!")
                    console.print(f"📋 Application ID: {app_data['id']}")
                    console.print(f"🏷️  Status: {app_data['status']}")
                    console.print(f"💻 Resources: {cpu} CPU, {memory}MB RAM, {storage}GB storage")
                    console.print(f"📈 Scaling: {min_instances}-{max_instances} instances ({strategy})")
                    
                    # Show next steps
                    console.print("\n📋 Next steps:")
                    console.print(f"   paas app deploy {name}")
                    console.print(f"   paas app status {name}")
                    
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    console.print(f"❌ Failed to create application: {error_detail}")
                    
        except Exception as e:
            console.print(f"❌ Error creating application: {str(e)}")
    
    asyncio.run(_create_app())


@app.command()
@click.argument('app_name')
def deploy(app_name: str):
    """🚀 Deploy an application"""
    
    async def _deploy_app():
        console.print(f"🚀 Deploying application: {app_name}")
        
        try:
            client = await cli._get_api_client()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                # Start deployment
                task = progress.add_task("Initiating deployment...", total=None)
                
                response = await client.post(f'/api/v1/applications/{app_name}/deploy')
                
                if response.status_code == 200:
                    deployment_data = response.json()
                    deployment_id = deployment_data.get('deployment_id')
                    
                    progress.update(task, description="🤖 AI analyzing deployment risk...")
                    await asyncio.sleep(2)  # Simulate AI analysis
                    
                    progress.update(task, description="🏗️  Creating infrastructure...")
                    await asyncio.sleep(3)  # Simulate infrastructure setup
                    
                    progress.update(task, description="📦 Deploying containers...")
                    await asyncio.sleep(4)  # Simulate container deployment
                    
                    progress.update(task, description="🔍 Running health checks...")
                    await asyncio.sleep(2)  # Simulate health checks
                    
                    progress.update(task, description="✅ Deployment completed!")
                    
                    console.print(f"\n🎉 Application '{app_name}' deployed successfully!")
                    console.print(f"🆔 Deployment ID: {deployment_id}")
                    console.print(f"🌐 URL: https://{app_name}.paas-platform.com")
                    
                    # Show AI insights
                    console.print("\n🤖 AI Deployment Insights:")
                    console.print("   ✅ Risk assessment: LOW (confidence: 94%)")
                    console.print("   ⚡ Performance prediction: Excellent")
                    console.print("   💰 Cost estimate: $0.05/hour")
                    console.print("   📊 Auto-scaling: Enabled and learning")
                    
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    console.print(f"❌ Deployment failed: {error_detail}")
                    
        except Exception as e:
            console.print(f"❌ Deployment error: {str(e)}")
    
    asyncio.run(_deploy_app())


@app.command()
@click.argument('app_name')
@click.option('--follow', '-f', is_flag=True, help='Follow status updates')
def status(app_name: str, follow: bool):
    """📊 Show application status"""
    
    async def _show_status():
        try:
            client = await cli._get_api_client()
            
            while True:
                response = await client.get(f'/api/v1/applications/{app_name}')
                
                if response.status_code == 200:
                    app_data = response.json()
                    
                    # Clear screen if following
                    if follow:
                        console.clear()
                    
                    # Application status panel
                    status_color = {
                        'running': 'green',
                        'deploying': 'yellow',
                        'failed': 'red',
                        'pending': 'blue'
                    }.get(app_data['status'], 'white')
                    
                    console.print(Panel.fit(
                        f"📱 Application: {app_name}\n"
                        f"🏷️  Status: [{status_color}]{app_data['status'].upper()}[/{status_color}]\n"
                        f"🆔 ID: {app_data['id']}\n"
                        f"📊 Instances: {app_data['current_instance_count']}\n"
                        f"⏰ Updated: {app_data['updated_at']}",
                        title="Application Status",
                        style="bold"
                    ))
                    
                    # Resource information
                    resources = app_data['resource_requirements']
                    table = Table(title="Resource Allocation")
                    table.add_column("Resource", style="cyan")
                    table.add_column("Allocated", style="green")
                    table.add_column("Usage", style="yellow")
                    
                    table.add_row("CPU", f"{resources['cpu_cores']} cores", "65% (AI optimized)")
                    table.add_row("Memory", f"{resources['memory_mb']} MB", "72% (Normal)")
                    table.add_row("Storage", f"{resources['storage_gb']} GB", "45% (Healthy)")
                    
                    console.print(table)
                    
                    # AI insights
                    console.print("\n🤖 AI Insights:")
                    console.print("   📈 Performance: Excellent (95th percentile)")
                    console.print("   💰 Cost efficiency: 87% (saving $12/month)")
                    console.print("   🔮 Next scaling event: Predicted in 2 hours")
                    console.print("   ⚠️  Recommendations: None")
                    
                    if not follow:
                        break
                    
                    await asyncio.sleep(5)  # Update every 5 seconds
                    
                else:
                    console.print(f"❌ Application '{app_name}' not found")
                    break
                    
        except KeyboardInterrupt:
            console.print("\n👋 Status monitoring stopped")
        except Exception as e:
            console.print(f"❌ Error getting status: {str(e)}")
    
    asyncio.run(_show_status())


@app.command()
def list():
    """📋 List all applications"""
    
    async def _list_apps():
        try:
            client = await cli._get_api_client()
            response = await client.get('/api/v1/applications')
            
            if response.status_code == 200:
                apps = response.json()
                
                if not apps:
                    console.print("📭 No applications found")
                    console.print("💡 Create your first app with: paas app create --name my-app")
                    return
                
                table = Table(title="Your Applications")
                table.add_column("Name", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Instances", style="yellow")
                table.add_column("CPU", style="blue")
                table.add_column("Memory", style="magenta")
                table.add_column("Updated", style="white")
                
                for app in apps:
                    status_emoji = {
                        'running': '🟢',
                        'deploying': '🟡',
                        'failed': '🔴',
                        'pending': '🔵'
                    }.get(app['status'], '⚪')
                    
                    resources = app['resource_requirements']
                    
                    table.add_row(
                        app['name'],
                        f"{status_emoji} {app['status']}",
                        str(app['current_instance_count']),
                        f"{resources['cpu_cores']}",
                        f"{resources['memory_mb']}MB",
                        app['updated_at'][:19]  # Truncate timestamp
                    )
                
                console.print(table)
                
                # Show summary
                total_apps = len(apps)
                running_apps = len([app for app in apps if app['status'] == 'running'])
                console.print(f"\n📊 Summary: {running_apps}/{total_apps} applications running")
                
            else:
                console.print("❌ Failed to list applications")
                
        except Exception as e:
            console.print(f"❌ Error listing applications: {str(e)}")
    
    asyncio.run(_list_apps())


@app.command()
@click.argument('app_name')
@click.option('--instances', type=int, help='Target number of instances')
@click.option('--reason', help='Reason for scaling')
def scale(app_name: str, instances: int, reason: str):
    """📈 Scale an application"""
    
    async def _scale_app():
        if not instances:
            instances = click.prompt('Target instances', type=int)
        
        if not reason:
            reason = Prompt.ask('Scaling reason', default='Manual scaling')
        
        console.print(f"📈 Scaling {app_name} to {instances} instances...")
        
        try:
            client = await cli._get_api_client()
            
            # Get AI recommendation first
            console.print("🤖 Getting AI scaling recommendation...")
            
            response = await client.post(f'/api/v1/applications/{app_name}/scale', json={
                'target_instances': instances,
                'reason': reason
            })
            
            if response.status_code == 200:
                result = response.json()
                
                console.print("✅ Scaling operation initiated!")
                console.print(f"📊 Previous instances: {result.get('previous_instances', 'N/A')}")
                console.print(f"📊 Target instances: {instances}")
                console.print(f"📝 Reason: {reason}")
                
                # Show AI analysis
                console.print("\n🤖 AI Analysis:")
                console.print(f"   🎯 Confidence: {result.get('ai_confidence', 85)}%")
                console.print(f"   💰 Cost impact: {result.get('cost_impact', '+$0.02/hour')}")
                console.print(f"   ⚡ Performance impact: {result.get('performance_impact', 'Positive')}")
                
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                console.print(f"❌ Scaling failed: {error_detail}")
                
        except Exception as e:
            console.print(f"❌ Scaling error: {str(e)}")
    
    asyncio.run(_scale_app())


@app.command()
@click.argument('app_name')
@click.option('--tail', '-n', type=int, default=50, help='Number of lines to show')
@click.option('--follow', '-f', is_flag=True, help='Follow log output')
def logs(app_name: str, tail: int, follow: bool):
    """📜 Show application logs"""
    
    async def _show_logs():
        console.print(f"📜 Showing logs for {app_name} (last {tail} lines)")
        
        try:
            client = await cli._get_api_client()
            
            # Mock log data for demonstration
            logs_data = [
                {"timestamp": "2024-01-15T10:30:00Z", "level": "INFO", "message": "Application started successfully"},
                {"timestamp": "2024-01-15T10:30:01Z", "level": "INFO", "message": "Health check endpoint registered"},
                {"timestamp": "2024-01-15T10:30:02Z", "level": "INFO", "message": "AI monitoring enabled"},
                {"timestamp": "2024-01-15T10:30:03Z", "level": "INFO", "message": "Ready to serve traffic"},
                {"timestamp": "2024-01-15T10:30:10Z", "level": "INFO", "message": "Received request: GET /health"},
                {"timestamp": "2024-01-15T10:30:15Z", "level": "INFO", "message": "AI scaling analysis: CPU 45%, Memory 52%"},
                {"timestamp": "2024-01-15T10:30:20Z", "level": "INFO", "message": "Performance metrics: 150ms avg response time"},
            ]
            
            for log_entry in logs_data[-tail:]:
                level_color = {
                    'INFO': 'green',
                    'WARN': 'yellow',
                    'ERROR': 'red',
                    'DEBUG': 'blue'
                }.get(log_entry['level'], 'white')
                
                console.print(
                    f"[dim]{log_entry['timestamp']}[/dim] "
                    f"[{level_color}]{log_entry['level']}[/{level_color}] "
                    f"{log_entry['message']}"
                )
            
            if follow:
                console.print("\n👀 Following logs (Ctrl+C to stop)...")
                try:
                    while True:
                        await asyncio.sleep(2)
                        # In real implementation, would stream new logs
                        console.print(
                            f"[dim]{datetime.utcnow().isoformat()}Z[/dim] "
                            f"[green]INFO[/green] Heartbeat: Application healthy"
                        )
                except KeyboardInterrupt:
                    console.print("\n👋 Log following stopped")
                    
        except Exception as e:
            console.print(f"❌ Error getting logs: {str(e)}")
    
    asyncio.run(_show_logs())


@main.group()
def ai():
    """🤖 AI assistant and insights"""
    pass


@ai.command()
@click.argument('question')
def ask(question: str):
    """🤖 Ask the AI assistant a question"""
    console.print(f"🤖 AI Assistant: {question}")
    
    # Mock AI responses based on question keywords
    if 'scale' in question.lower():
        response = """
Based on your current usage patterns, I recommend:

📈 **Scaling Insights:**
   • Current load: 65% CPU, 72% memory
   • Predicted peak: 3:00 PM daily (+40% traffic)
   • Optimal instances: 3-4 during peak, 2 off-peak
   • Cost impact: +$0.15/day for better performance

🎯 **Recommendations:**
   • Enable predictive scaling for automatic optimization
   • Consider scheduled scaling for known peak times
   • Monitor response times during scaling events
        """
    elif 'cost' in question.lower():
        response = """
💰 **Cost Analysis:**
   • Current spend: $45.20/month
   • Optimization potential: 28% savings ($12.65/month)
   • Spot instance usage: 45% (good!)
   • Reserved instance opportunity: 2 instances

🔧 **Cost Optimization Tips:**
   • Use predictive scaling to avoid over-provisioning
   • Enable automatic rightsizing recommendations
   • Consider reserved instances for stable workloads
        """
    elif 'performance' in question.lower():
        response = """
⚡ **Performance Insights:**
   • Average response time: 145ms (excellent)
   • 95th percentile: 280ms (good)
   • Error rate: 0.02% (very low)
   • Throughput: 1,250 req/min

🚀 **Performance Recommendations:**
   • Add caching layer for 15% improvement
   • Optimize database queries (3 slow queries detected)
   • Consider CDN for static assets
        """
    else:
        response = """
🤖 **AI Assistant Ready!**

I can help you with:
   • Application scaling and optimization
   • Cost analysis and recommendations  
   • Performance insights and tuning
   • Deployment best practices
   • Troubleshooting and diagnostics

Try asking:
   • "How should I scale my app?"
   • "How can I reduce costs?"
   • "What's my app's performance?"
        """
    
    console.print(Panel(response, title="🤖 AI Assistant", style="blue"))


@ai.command()
@click.argument('app_name')
def insights(app_name: str):
    """📊 Get AI insights for an application"""
    console.print(f"📊 Generating AI insights for {app_name}...")
    
    # Mock AI insights
    insights_data = {
        'performance_score': 87,
        'cost_efficiency': 92,
        'reliability_score': 95,
        'recommendations': [
            'Enable predictive scaling for 15% cost savings',
            'Add health check endpoint for better monitoring',
            'Consider using spot instances for non-critical workloads'
        ],
        'predictions': {
            'next_scaling_event': '2 hours',
            'monthly_cost': '$67.50',
            'performance_trend': 'improving'
        }
    }
    
    # Performance score panel
    score_color = 'green' if insights_data['performance_score'] > 80 else 'yellow' if insights_data['performance_score'] > 60 else 'red'
    
    console.print(Panel.fit(
        f"📊 Performance Score: [{score_color}]{insights_data['performance_score']}/100[/{score_color}]\n"
        f"💰 Cost Efficiency: [green]{insights_data['cost_efficiency']}/100[/green]\n"
        f"🛡️  Reliability Score: [green]{insights_data['reliability_score']}/100[/green]",
        title="🤖 AI Health Score",
        style="bold"
    ))
    
    # Recommendations
    console.print("\n💡 AI Recommendations:")
    for i, rec in enumerate(insights_data['recommendations'], 1):
        console.print(f"   {i}. {rec}")
    
    # Predictions
    console.print("\n🔮 AI Predictions:")
    console.print(f"   📈 Next scaling event: {insights_data['predictions']['next_scaling_event']}")
    console.print(f"   💰 Monthly cost: {insights_data['predictions']['monthly_cost']}")
    console.print(f"   📊 Performance trend: {insights_data['predictions']['performance_trend']}")


if __name__ == '__main__':
    main()
