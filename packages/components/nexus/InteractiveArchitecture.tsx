'use client';

import { useState } from 'react';
import { 
  Database, Cloud, Cpu, Network, Shield, Zap, 
  ArrowRight, CheckCircle, Code, Layers 
} from 'lucide-react';

interface ArchitectureNode {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  position: { x: number; y: number };
  connections: string[];
  details: string[];
}

const architectureNodes: ArchitectureNode[] = [
  {
    id: 'data-layer',
    title: 'Data Layer',
    description: 'Unified data ingestion and processing',
    icon: <Database className="w-6 h-6" />,
    position: { x: 10, y: 80 },
    connections: ['ai-core'],
    details: [
      'Multi-source data connectors',
      'Real-time streaming',
      'Data validation & cleansing',
      'Schema management'
    ]
  },
  {
    id: 'ai-core',
    title: 'AI Core Engine',
    description: 'Central AI processing and orchestration',
    icon: <Cpu className="w-6 h-6" />,
    position: { x: 50, y: 50 },
    connections: ['api-gateway', 'workflow-engine'],
    details: [
      'Model management',
      'Auto-scaling inference',
      'A/B testing framework',
      'Performance monitoring'
    ]
  },
  {
    id: 'workflow-engine',
    title: 'Workflow Engine',
    description: 'Automated process orchestration',
    icon: <Network className="w-6 h-6" />,
    position: { x: 50, y: 20 },
    connections: ['api-gateway'],
    details: [
      'Visual workflow builder',
      'Event-driven automation',
      'Error handling & retry',
      'Audit trail'
    ]
  },
  {
    id: 'api-gateway',
    title: 'API Gateway',
    description: 'Secure API management and routing',
    icon: <Shield className="w-6 h-6" />,
    position: { x: 90, y: 50 },
    connections: [],
    details: [
      'Rate limiting',
      'Authentication & authorization',
      'Request/response transformation',
      'Analytics & monitoring'
    ]
  },
  {
    id: 'cloud-infra',
    title: 'Cloud Infrastructure',
    description: 'Scalable cloud-native foundation',
    icon: <Cloud className="w-6 h-6" />,
    position: { x: 30, y: 80 },
    connections: ['ai-core'],
    details: [
      'Auto-scaling containers',
      'Load balancing',
      'Multi-region deployment',
      'Disaster recovery'
    ]
  }
];

export function InteractiveArchitecture() {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  const selectedNodeData = architectureNodes.find(node => node.id === selectedNode);

  return (
    <section className="py-24 bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Interactive Architecture
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Explore how Nexus components work together to deliver enterprise-grade AI solutions
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-12">
          {/* Architecture Diagram */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-xl p-8 h-96 relative overflow-hidden">
              <svg className="w-full h-full" viewBox="0 0 100 100">
                {/* Connection Lines */}
                {architectureNodes.map(node => 
                  node.connections.map(connectionId => {
                    const targetNode = architectureNodes.find(n => n.id === connectionId);
                    if (!targetNode) return null;
                    
                    return (
                      <line
                        key={`${node.id}-${connectionId}`}
                        x1={node.position.x}
                        y1={node.position.y}
                        x2={targetNode.position.x}
                        y2={targetNode.position.y}
                        stroke="#e2e8f0"
                        strokeWidth="0.5"
                        className={`transition-all duration-300 ${
                          hoveredNode === node.id || hoveredNode === connectionId
                            ? 'stroke-blue-500 stroke-2'
                            : ''
                        }`}
                      />
                    );
                  })
                )}

                {/* Architecture Nodes */}
                {architectureNodes.map(node => (
                  <g key={node.id}>
                    <circle
                      cx={node.position.x}
                      cy={node.position.y}
                      r="8"
                      className={`cursor-pointer transition-all duration-300 ${
                        selectedNode === node.id
                          ? 'fill-blue-600'
                          : hoveredNode === node.id
                          ? 'fill-blue-500'
                          : 'fill-white stroke-gray-300 stroke-2'
                      }`}
                      onMouseEnter={() => setHoveredNode(node.id)}
                      onMouseLeave={() => setHoveredNode(null)}
                      onClick={() => setSelectedNode(selectedNode === node.id ? null : node.id)}
                    />
                    <text
                      x={node.position.x}
                      y={node.position.y + 15}
                      textAnchor="middle"
                      className="text-xs font-medium fill-gray-700 pointer-events-none"
                    >
                      {node.title}
                    </text>
                  </g>
                ))}
              </svg>

              {/* Floating Node Details */}
              {hoveredNode && (
                <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-4 max-w-xs">
                  <div className="flex items-center gap-2 mb-2">
                    {architectureNodes.find(n => n.id === hoveredNode)?.icon}
                    <h4 className="font-semibold text-gray-900">
                      {architectureNodes.find(n => n.id === hoveredNode)?.title}
                    </h4>
                  </div>
                  <p className="text-sm text-gray-600">
                    {architectureNodes.find(n => n.id === hoveredNode)?.description}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Component Details */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Component Details
              </h3>
              
              {selectedNodeData ? (
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
                      {selectedNodeData.icon}
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">
                        {selectedNodeData.title}
                      </h4>
                      <p className="text-sm text-gray-600">
                        {selectedNodeData.description}
                      </p>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h5 className="font-medium text-gray-900">Key Features:</h5>
                    <ul className="space-y-1">
                      {selectedNodeData.details.map((detail, index) => (
                        <li key={index} className="flex items-center gap-2 text-sm text-gray-600">
                          <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                          {detail}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <Layers className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                  <p className="text-gray-500">
                    Click on any component in the diagram to explore its features
                  </p>
                </div>
              )}
            </div>

            {/* Quick Stats */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white">
              <h4 className="font-bold mb-4">Architecture Benefits</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Deployment Speed</span>
                  <span className="font-bold">10x Faster</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Scalability</span>
                  <span className="font-bold">Auto-scaling</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Reliability</span>
                  <span className="font-bold">99.9% Uptime</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
