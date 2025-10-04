import React from 'react';
import { FolderOpen, Bot, Workflow, TrendingUp } from 'lucide-react';
import { Project, Agent, Workflow as WorkflowType } from '../../../types';

interface OverviewCardsProps {
  projects: Project[];
  agents: Agent[];
  workflows: WorkflowType[];
}

const OverviewCards: React.FC<OverviewCardsProps> = ({ projects, agents, workflows }) => {
  const activeProjects = projects.filter(p => p.status === 'in-progress').length;
  const activeAgents = agents.filter(a => a.status === 'active').length;
  const activeWorkflows = workflows.filter(w => w.status === 'active').length;
  const avgProgress = projects.reduce((sum, p) => sum + p.progress, 0) / projects.length;

  const cards = [
    {
      title: 'Active Projects',
      value: activeProjects.toString(),
      total: projects.length,
      icon: FolderOpen,
      color: 'blue',
      change: '+2 this month'
    },
    {
      title: 'AI Agents',
      value: activeAgents.toString(),
      total: agents.length,
      icon: Bot,
      color: 'green',
      change: '98.5% uptime'
    },
    {
      title: 'Workflows',
      value: activeWorkflows.toString(),
      total: workflows.length,
      icon: Workflow,
      color: 'purple',
      change: '94% success rate'
    },
    {
      title: 'Avg Progress',
      value: `${Math.round(avgProgress)}%`,
      total: 100,
      icon: TrendingUp,
      color: 'orange',
      change: '+5% this week'
    }
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-50 text-blue-600',
      green: 'bg-green-50 text-green-600',
      purple: 'bg-purple-50 text-purple-600',
      orange: 'bg-orange-50 text-orange-600'
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{card.title}</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{card.value}</p>
            </div>
            <div className={`p-3 rounded-lg ${getColorClasses(card.color)}`}>
              <card.icon className="h-6 w-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center">
            <span className="text-sm text-gray-500">{card.change}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default OverviewCards;
