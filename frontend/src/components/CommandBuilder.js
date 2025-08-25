import React, { useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus, 
  Trash2, 
  Play, 
  Save, 
  Copy,
  MousePointer2,
  Type,
  Navigation,
  Search,
  Eye,
  Clock,
  Settings,
  Zap,
  ArrowDown,
  ArrowRight,
  X
} from 'lucide-react';

const CommandBuilder = ({ isOpen, onClose, onExecuteCommand }) => {
  const [workflow, setWorkflow] = useState({
    name: '',
    description: '',
    steps: []
  });
  const [draggedItem, setDraggedItem] = useState(null);
  const [draggedIndex, setDraggedIndex] = useState(null);
  const [previewMode, setPreviewMode] = useState(false);
  
  const dragRef = useRef(null);

  // Available command types
  const commandTypes = [
    { 
      type: 'navigate', 
      icon: Navigation, 
      label: 'Navigate to URL', 
      color: 'bg-blue-100 text-blue-700',
      params: ['url']
    },
    { 
      type: 'click', 
      icon: MousePointer2, 
      label: 'Click Element', 
      color: 'bg-green-100 text-green-700',
      params: ['selector', 'description']
    },
    { 
      type: 'type', 
      icon: Type, 
      label: 'Type Text', 
      color: 'bg-purple-100 text-purple-700',
      params: ['selector', 'text']
    },
    { 
      type: 'search', 
      icon: Search, 
      label: 'Search', 
      color: 'bg-orange-100 text-orange-700',
      params: ['query', 'engine']
    },
    { 
      type: 'wait', 
      icon: Clock, 
      label: 'Wait/Delay', 
      color: 'bg-gray-100 text-gray-700',
      params: ['duration']
    },
    { 
      type: 'screenshot', 
      icon: Eye, 
      label: 'Take Screenshot', 
      color: 'bg-indigo-100 text-indigo-700',
      params: ['filename']
    }
  ];

  const handleDragStart = (e, item, index = null) => {
    setDraggedItem(item);
    setDraggedIndex(index);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e, targetIndex) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e, targetIndex) => {
    e.preventDefault();
    
    if (draggedItem) {
      if (draggedIndex !== null) {
        // Reordering existing steps
        const newSteps = [...workflow.steps];
        const [movedStep] = newSteps.splice(draggedIndex, 1);
        newSteps.splice(targetIndex, 0, movedStep);
        
        setWorkflow(prev => ({
          ...prev,
          steps: newSteps
        }));
      } else {
        // Adding new step from command palette
        const newStep = {
          id: Date.now(),
          type: draggedItem.type,
          label: draggedItem.label,
          icon: draggedItem.icon,
          color: draggedItem.color,
          params: draggedItem.params.reduce((acc, param) => {
            acc[param] = '';
            return acc;
          }, {}),
          completed: false
        };
        
        const newSteps = [...workflow.steps];
        newSteps.splice(targetIndex, 0, newStep);
        
        setWorkflow(prev => ({
          ...prev,
          steps: newSteps
        }));
      }
    }
    
    setDraggedItem(null);
    setDraggedIndex(null);
  };

  const updateStepParam = (stepId, paramName, value) => {
    setWorkflow(prev => ({
      ...prev,
      steps: prev.steps.map(step => 
        step.id === stepId 
          ? { ...step, params: { ...step.params, [paramName]: value }}
          : step
      )
    }));
  };

  const removeStep = (stepId) => {
    setWorkflow(prev => ({
      ...prev,
      steps: prev.steps.filter(step => step.id !== stepId)
    }));
  };

  const executeWorkflow = async () => {
    if (workflow.steps.length === 0) return;
    
    // Convert workflow to command format
    const commands = workflow.steps.map(step => ({
      type: step.type,
      params: step.params
    }));
    
    // Execute through parent component
    if (onExecuteCommand) {
      await onExecuteCommand({
        type: 'workflow',
        workflow: {
          name: workflow.name || 'Untitled Workflow',
          steps: commands
        }
      });
    }
  };

  const saveWorkflow = () => {
    // Save to localStorage for now
    const savedWorkflows = JSON.parse(localStorage.getItem('kairo_workflows') || '[]');
    const workflowToSave = {
      ...workflow,
      id: Date.now(),
      createdAt: new Date().toISOString()
    };
    
    savedWorkflows.push(workflowToSave);
    localStorage.setItem('kairo_workflows', JSON.stringify(savedWorkflows));
    
    alert('Workflow saved successfully!');
  };

  const copyWorkflow = () => {
    navigator.clipboard.writeText(JSON.stringify(workflow, null, 2));
    alert('Workflow copied to clipboard!');
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl h-[80vh] flex overflow-hidden"
        >
          {/* Header */}
          <div className="absolute top-0 left-0 right-0 bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-t-2xl z-10">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold">Visual Command Builder</h2>
                <p className="text-green-100 text-sm">Drag and drop to create automated workflows</p>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setPreviewMode(!previewMode)}
                  className="px-3 py-1 bg-white/20 rounded-lg hover:bg-white/30 transition-colors text-sm"
                >
                  {previewMode ? 'Edit' : 'Preview'}
                </button>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          <div className="flex w-full mt-16">
            {/* Command Palette */}
            <div className="w-80 bg-gray-50 p-4 border-r border-gray-200 overflow-y-auto">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
                <Zap className="w-5 h-5 mr-2 text-yellow-500" />
                Command Palette
              </h3>
              
              <div className="space-y-2">
                {commandTypes.map((cmd, index) => (
                  <motion.div
                    key={cmd.type}
                    draggable
                    onDragStart={(e) => handleDragStart(e, cmd)}
                    className={`p-3 rounded-lg cursor-move transition-all duration-200 ${cmd.color} hover:shadow-md transform hover:-translate-y-0.5 border-2 border-dashed border-transparent hover:border-white`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div className="flex items-center space-x-2">
                      <cmd.icon className="w-5 h-5" />
                      <span className="font-medium text-sm">{cmd.label}</span>
                    </div>
                    <p className="text-xs mt-1 opacity-80">
                      Drag to workflow area →
                    </p>
                  </motion.div>
                ))}
              </div>

              {/* Quick Actions */}
              <div className="mt-6">
                <h4 className="font-medium text-gray-700 mb-2">Quick Actions</h4>
                <div className="space-y-2">
                  <button
                    onClick={executeWorkflow}
                    disabled={workflow.steps.length === 0}
                    className="w-full flex items-center justify-center space-x-2 bg-green-500 text-white py-2 px-3 rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <Play className="w-4 h-4" />
                    <span>Execute</span>
                  </button>
                  
                  <button
                    onClick={saveWorkflow}
                    disabled={workflow.steps.length === 0 || !workflow.name}
                    className="w-full flex items-center justify-center space-x-2 bg-blue-500 text-white py-2 px-3 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <Save className="w-4 h-4" />
                    <span>Save</span>
                  </button>
                  
                  <button
                    onClick={copyWorkflow}
                    disabled={workflow.steps.length === 0}
                    className="w-full flex items-center justify-center space-x-2 bg-gray-500 text-white py-2 px-3 rounded-lg hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <Copy className="w-4 h-4" />
                    <span>Copy</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Workflow Builder */}
            <div className="flex-1 p-6 overflow-y-auto">
              {/* Workflow Info */}
              <div className="mb-6">
                <input
                  type="text"
                  placeholder="Workflow Name"
                  value={workflow.name}
                  onChange={(e) => setWorkflow(prev => ({ ...prev, name: e.target.value }))}
                  className="text-xl font-bold w-full p-2 border-b-2 border-gray-200 focus:border-green-500 outline-none bg-transparent"
                />
                <textarea
                  placeholder="Describe what this workflow does..."
                  value={workflow.description}
                  onChange={(e) => setWorkflow(prev => ({ ...prev, description: e.target.value }))}
                  className="w-full mt-2 p-2 border border-gray-200 rounded-lg focus:border-green-500 outline-none resize-none"
                  rows={2}
                />
              </div>

              {/* Workflow Steps */}
              <div className="space-y-4">
                {workflow.steps.length === 0 ? (
                  <div
                    onDragOver={(e) => handleDragOver(e, 0)}
                    onDrop={(e) => handleDrop(e, 0)}
                    className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center text-gray-500"
                  >
                    <Zap className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                    <p className="text-lg font-medium">Start Building Your Workflow</p>
                    <p className="text-sm mt-2">Drag commands from the palette to create your automation sequence</p>
                  </div>
                ) : (
                  <>
                    {workflow.steps.map((step, index) => (
                      <div key={step.id}>
                        {/* Drop Zone Before Step */}
                        <div
                          onDragOver={(e) => handleDragOver(e, index)}
                          onDrop={(e) => handleDrop(e, index)}
                          className="h-2 bg-transparent hover:bg-green-100 rounded transition-colors"
                        />
                        
                        {/* Step Card */}
                        <motion.div
                          draggable
                          onDragStart={(e) => handleDragStart(e, step, index)}
                          className={`p-4 rounded-lg border-2 border-gray-200 hover:border-green-300 transition-all duration-200 ${step.color.replace('text-', 'bg-').replace('-700', '-50')} cursor-move`}
                          whileHover={{ scale: 1.01 }}
                        >
                          <div className="flex items-start justify-between">
                            <div className="flex items-center space-x-3">
                              <div className={`p-2 rounded-lg ${step.color}`}>
                                <step.icon className="w-5 h-5" />
                              </div>
                              <div>
                                <h4 className="font-medium text-gray-800">{step.label}</h4>
                                <p className="text-sm text-gray-500">Step {index + 1}</p>
                              </div>
                            </div>
                            <button
                              onClick={() => removeStep(step.id)}
                              className="p-1 text-red-500 hover:bg-red-100 rounded transition-colors"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                          
                          {/* Step Parameters */}
                          <div className="mt-4 space-y-3">
                            {Object.entries(step.params).map(([paramName, paramValue]) => (
                              <div key={paramName}>
                                <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">
                                  {paramName}:
                                </label>
                                <input
                                  type="text"
                                  value={paramValue}
                                  onChange={(e) => updateStepParam(step.id, paramName, e.target.value)}
                                  placeholder={`Enter ${paramName}...`}
                                  className="w-full p-2 border border-gray-300 rounded-lg focus:border-green-500 outline-none"
                                />
                              </div>
                            ))}
                          </div>
                        </motion.div>
                        
                        {/* Flow Arrow */}
                        {index < workflow.steps.length - 1 && (
                          <div className="flex justify-center my-2">
                            <ArrowDown className="w-5 h-5 text-gray-400" />
                          </div>
                        )}
                      </div>
                    ))}
                    
                    {/* Drop Zone After Last Step */}
                    <div
                      onDragOver={(e) => handleDragOver(e, workflow.steps.length)}
                      onDrop={(e) => handleDrop(e, workflow.steps.length)}
                      className="h-8 bg-transparent hover:bg-green-100 rounded transition-colors border-2 border-dashed border-transparent hover:border-green-300 flex items-center justify-center"
                    >
                      <Plus className="w-4 h-4 text-gray-400" />
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default CommandBuilder;