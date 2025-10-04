import { DocSection, DocArticle, DocNavigation } from '@/types/docs'
import { gettingStartedArticles } from './getting-started'
import { apiReferenceArticles } from './api-reference'

// Additional articles for other sections
const userGuidesArticles: DocArticle[] = [
  {
    id: 'project-management',
    title: 'Project Management',
    description: 'Managing AI projects and workflows effectively',
    slug: 'project-management',
    sectionId: 'user-guides',
    order: 1,
    difficulty: 'intermediate',
    tags: ['projects', 'management', 'workflows'],
    lastUpdated: '2024-07-04',
    readTime: 12,
    content: `
# Project Management

Learn how to effectively manage AI projects and workflows in the Nexus platform.

## Project Lifecycle

Every AI project in Nexus follows a structured lifecycle:

1. **Planning** - Define objectives and requirements
2. **Development** - Build and configure AI agents
3. **Testing** - Validate performance and accuracy
4. **Deployment** - Launch to production environment
5. **Monitoring** - Track performance and optimize

## Creating Projects

### Project Setup

\`\`\`javascript
const project = {
  name: "Customer Service Automation",
  description: "Automate customer support with AI agents",
  type: "agent_deployment",
  priority: "high",
  team: ["user1", "user2", "user3"]
}
\`\`\`

### Project Templates

Choose from pre-built templates:
- **Customer Service** - Support automation
- **Sales Assistant** - Lead qualification
- **Data Analysis** - Automated insights
- **Content Generation** - Marketing automation

## Workflow Management

### Creating Workflows

Build automated processes that connect multiple components:

\`\`\`yaml
workflow:
  name: "Lead Processing"
  trigger: "form_submission"
  steps:
    - validate_data
    - score_lead
    - assign_to_agent
    - send_notification
\`\`\`

### Workflow Monitoring

Track workflow performance:
- Execution success rates
- Processing times
- Error rates and types
- Resource utilization

## Team Collaboration

### Role-Based Access

Assign appropriate roles to team members:
- **Project Manager** - Full project access
- **Developer** - Code and configuration access
- **Analyst** - Read-only analytics access
- **Stakeholder** - Dashboard and reports access

### Communication Tools

- **Comments** - Add notes to projects and components
- **Activity Feed** - Track all project changes
- **Notifications** - Stay updated on important events
- **Reports** - Share progress with stakeholders

## Best Practices

### Project Organization

- Use clear, descriptive names
- Maintain comprehensive documentation
- Set up proper version control
- Implement testing procedures

### Performance Optimization

- Monitor resource usage
- Optimize agent configurations
- Implement caching strategies
- Use appropriate scaling settings

### Risk Management

- Set up monitoring alerts
- Implement backup procedures
- Plan for failure scenarios
- Maintain audit trails
    `
  }
]

const bestPracticesArticles: DocArticle[] = [
  {
    id: 'ai-model-optimization',
    title: 'AI Model Optimization',
    description: 'Best practices for optimizing AI model performance and accuracy',
    slug: 'ai-model-optimization',
    sectionId: 'best-practices',
    order: 1,
    difficulty: 'advanced',
    tags: ['optimization', 'performance', 'models', 'ai'],
    lastUpdated: '2024-07-04',
    readTime: 18,
    content: `
# AI Model Optimization

Optimize your AI models for better performance, accuracy, and efficiency.

## Performance Optimization

### Model Architecture

Choose the right architecture for your use case:

\`\`\`python
# Example model configuration
model_config = {
    "architecture": "transformer",
    "layers": 12,
    "hidden_size": 768,
    "attention_heads": 12,
    "dropout": 0.1
}
\`\`\`

### Training Optimization

- **Learning Rate Scheduling** - Adjust learning rates during training
- **Batch Size Optimization** - Find optimal batch sizes for your hardware
- **Gradient Clipping** - Prevent exploding gradients
- **Early Stopping** - Avoid overfitting

### Inference Optimization

- **Model Quantization** - Reduce model size and improve speed
- **Batch Processing** - Process multiple requests together
- **Caching** - Cache frequent predictions
- **Hardware Acceleration** - Use GPUs or specialized chips

## Accuracy Improvement

### Data Quality

- **Data Cleaning** - Remove noise and inconsistencies
- **Data Augmentation** - Increase training data variety
- **Feature Engineering** - Create meaningful input features
- **Balanced Datasets** - Ensure representative training data

### Training Techniques

- **Transfer Learning** - Start with pre-trained models
- **Ensemble Methods** - Combine multiple models
- **Cross-Validation** - Validate model performance
- **Hyperparameter Tuning** - Optimize model parameters

## Monitoring and Maintenance

### Performance Metrics

Track key metrics:
- **Accuracy** - Prediction correctness
- **Latency** - Response time
- **Throughput** - Requests per second
- **Resource Usage** - CPU, memory, GPU utilization

### Model Drift Detection

Monitor for changes in model performance:

\`\`\`python
def detect_drift(current_metrics, baseline_metrics, threshold=0.05):
    accuracy_drift = abs(current_metrics['accuracy'] - baseline_metrics['accuracy'])
    return accuracy_drift > threshold
\`\`\`

### Continuous Improvement

- **A/B Testing** - Compare model versions
- **Feedback Loops** - Incorporate user feedback
- **Regular Retraining** - Update models with new data
- **Performance Reviews** - Regular model assessments
    `
  }
]

// Define all sections
export const docSections: DocSection[] = [
  {
    id: 'getting-started',
    title: 'Getting Started',
    description: 'Quick start guides and basic concepts',
    icon: 'Zap',
    color: 'bg-green-100 text-green-600',
    order: 1,
    articles: gettingStartedArticles
  },
  {
    id: 'api-reference',
    title: 'API Reference',
    description: 'Complete API documentation and examples',
    icon: 'Code',
    color: 'bg-blue-100 text-blue-600',
    order: 2,
    articles: apiReferenceArticles
  },
  {
    id: 'user-guides',
    title: 'User Guides',
    description: 'Step-by-step guides for common tasks',
    icon: 'Users',
    color: 'bg-purple-100 text-purple-600',
    order: 3,
    articles: userGuidesArticles
  },
  {
    id: 'best-practices',
    title: 'Best Practices',
    description: 'Expert recommendations and guidelines',
    icon: 'FileText',
    color: 'bg-orange-100 text-orange-600',
    order: 4,
    articles: bestPracticesArticles
  }
]

// Combine all articles
export const allArticles: DocArticle[] = [
  ...gettingStartedArticles,
  ...apiReferenceArticles,
  ...userGuidesArticles,
  ...bestPracticesArticles
]

// Create navigation structure
export const docNavigation: DocNavigation = {
  sections: docSections
}

// Helper functions
export function getArticleBySlug(slug: string): DocArticle | undefined {
  return allArticles.find(article => article.slug === slug)
}

export function getArticlesBySection(sectionId: string): DocArticle[] {
  return allArticles
    .filter(article => article.sectionId === sectionId)
    .sort((a, b) => a.order - b.order)
}

export function getSectionById(sectionId: string): DocSection | undefined {
  return docSections.find(section => section.id === sectionId)
}

export function searchArticles(query: string): DocArticle[] {
  const searchTerm = query.toLowerCase()
  return allArticles.filter(article => 
    article.title.toLowerCase().includes(searchTerm) ||
    article.description.toLowerCase().includes(searchTerm) ||
    article.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
    article.content.toLowerCase().includes(searchTerm)
  )
}
