'use client'

import { useState, useEffect } from 'react'
import { Play, Pause, RotateCcw, Monitor, Smartphone, Tablet } from 'lucide-react'

interface DemoStep {
  id: string
  title: string
  description: string
  duration: number
  screenshot: string
}

const demoSteps: DemoStep[] = [
  {
    id: 'setup',
    title: 'Project Setup',
    description: 'Create a new AI project with pre-configured templates',
    duration: 3000,
    screenshot: '/images/demo/setup.jpg'
  },
  {
    id: 'data',
    title: 'Data Integration',
    description: 'Connect your data sources with drag-and-drop simplicity',
    duration: 4000,
    screenshot: '/images/demo/data-integration.jpg'
  },
  {
    id: 'model',
    title: 'Model Training',
    description: 'Train AI models with automated hyperparameter optimization',
    duration: 5000,
    screenshot: '/images/demo/model-training.jpg'
  },
  {
    id: 'deploy',
    title: 'Deployment',
    description: 'Deploy to production with one-click deployment',
    duration: 3000,
    screenshot: '/images/demo/deployment.jpg'
  },
  {
    id: 'monitor',
    title: 'Monitoring',
    description: 'Monitor performance with real-time dashboards',
    duration: 4000,
    screenshot: '/images/demo/monitoring.jpg'
  }
]

export function PlatformDemo() {
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [progress, setProgress] = useState(0)
  const [deviceView, setDeviceView] = useState<'desktop' | 'tablet' | 'mobile'>('desktop')

  useEffect(() => {
    let interval: NodeJS.Timeout

    if (isPlaying) {
      interval = setInterval(() => {
        setProgress(prev => {
          const newProgress = prev + 100
          const currentDuration = demoSteps[currentStep].duration
          
          if (newProgress >= currentDuration) {
            // Move to next step
            setCurrentStep(prevStep => {
              const nextStep = (prevStep + 1) % demoSteps.length
              return nextStep
            })
            return 0
          }
          
          return newProgress
        })
      }, 100)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [isPlaying, currentStep])

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying)
  }

  const handleReset = () => {
    setIsPlaying(false)
    setCurrentStep(0)
    setProgress(0)
  }

  const handleStepClick = (stepIndex: number) => {
    setCurrentStep(stepIndex)
    setProgress(0)
    setIsPlaying(false)
  }

  const currentStepData = demoSteps[currentStep]
  const progressPercentage = (progress / currentStepData.duration) * 100

  const getDeviceClasses = () => {
    switch (deviceView) {
      case 'mobile':
        return 'max-w-sm mx-auto'
      case 'tablet':
        return 'max-w-2xl mx-auto'
      default:
        return 'max-w-6xl mx-auto'
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
      {/* Demo Controls */}
      <div className="bg-secondary-900 text-white p-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <button
              onClick={handlePlayPause}
              className="flex items-center justify-center w-12 h-12 bg-primary-600 hover:bg-primary-700 rounded-full transition-colors"
            >
              {isPlaying ? (
                <Pause className="w-5 h-5" />
              ) : (
                <Play className="w-5 h-5 ml-0.5" />
              )}
            </button>
            
            <button
              onClick={handleReset}
              className="flex items-center justify-center w-12 h-12 bg-secondary-700 hover:bg-secondary-600 rounded-full transition-colors"
            >
              <RotateCcw className="w-5 h-5" />
            </button>
            
            <div className="text-left">
              <h3 className="font-semibold">{currentStepData.title}</h3>
              <p className="text-secondary-300 text-sm">{currentStepData.description}</p>
            </div>
          </div>
          
          {/* Device View Toggle */}
          <div className="flex items-center space-x-2 bg-secondary-800 rounded-lg p-1">
            <button
              onClick={() => setDeviceView('desktop')}
              className={`p-2 rounded ${deviceView === 'desktop' ? 'bg-primary-600' : 'hover:bg-secondary-700'} transition-colors`}
            >
              <Monitor className="w-4 h-4" />
            </button>
            <button
              onClick={() => setDeviceView('tablet')}
              className={`p-2 rounded ${deviceView === 'tablet' ? 'bg-primary-600' : 'hover:bg-secondary-700'} transition-colors`}
            >
              <Tablet className="w-4 h-4" />
            </button>
            <button
              onClick={() => setDeviceView('mobile')}
              className={`p-2 rounded ${deviceView === 'mobile' ? 'bg-primary-600' : 'hover:bg-secondary-700'} transition-colors`}
            >
              <Smartphone className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        {/* Progress Bar */}
        <div className="mt-4">
          <div className="bg-secondary-700 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-primary-500 h-full transition-all duration-100 ease-linear"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Demo Steps Navigation */}
      <div className="bg-secondary-50 p-4">
        <div className="flex flex-wrap justify-center gap-2">
          {demoSteps.map((step, index) => (
            <button
              key={step.id}
              onClick={() => handleStepClick(index)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                index === currentStep
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-secondary-700 hover:bg-secondary-100'
              }`}
            >
              {index + 1}. {step.title}
            </button>
          ))}
        </div>
      </div>

      {/* Demo Screen */}
      <div className="p-8 bg-secondary-50">
        <div className={`${getDeviceClasses()} transition-all duration-300`}>
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Mock Browser/App Header */}
            <div className="bg-secondary-100 px-4 py-3 flex items-center space-x-2">
              <div className="flex space-x-2">
                <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                <div className="w-3 h-3 bg-green-400 rounded-full"></div>
              </div>
              <div className="flex-1 bg-white rounded px-3 py-1 text-sm text-secondary-600">
                nexus.aic.com/{currentStepData.id}
              </div>
            </div>
            
            {/* Demo Content */}
            <div className="aspect-video bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center relative overflow-hidden">
              {/* Placeholder for actual demo screenshots */}
              <div className="text-center p-8">
                <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <div className="w-12 h-12 bg-primary-600 rounded-lg"></div>
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                  {currentStepData.title}
                </h3>
                <p className="text-secondary-600 max-w-md">
                  {currentStepData.description}
                </p>
                
                {/* Animated Elements */}
                <div className="mt-6 flex justify-center space-x-2">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className={`w-2 h-2 rounded-full ${
                        (progress / 500) % 5 === i ? 'bg-primary-600' : 'bg-secondary-300'
                      } transition-colors duration-200`}
                    />
                  ))}
                </div>
              </div>
              
              {/* Progress Indicator */}
              {isPlaying && (
                <div className="absolute bottom-4 right-4 bg-white bg-opacity-90 rounded-full p-2">
                  <div className="w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Demo Features */}
      <div className="bg-white p-6 border-t border-secondary-200">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div>
            <div className="text-2xl font-bold text-primary-600 mb-1">5 min</div>
            <div className="text-sm text-secondary-600">Complete Demo</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600 mb-1">10x</div>
            <div className="text-sm text-secondary-600">Faster Setup</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600 mb-1">Zero</div>
            <div className="text-sm text-secondary-600">Code Required</div>
          </div>
        </div>
      </div>
    </div>
  )
}
