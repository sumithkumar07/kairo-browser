import React, { useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MousePointer, 
  Navigation, 
  Type, 
  Search, 
  Download, 
  Eye, 
  Pause, 
  Play, 
  Save, 
  Trash2, 
  Plus, 
  ArrowRight,
  Settings,
  Code,
  Workflow,
  Zap,
  Clock,
  CheckCircle,
  XCircle,
  RotateCw
} from 'lucide-react';

const VisualWorkflowBuilder = ({ onExecuteWorkflow, shadowTasks, builtWorkflows, setBuiltWorkflows }) => {
  const [workflowSteps, setWorkflowSteps] = useState([]);
  const [workflowName, setWorkflowName] = useState('');
  const [draggedCommand, setDraggedCommand] = useState(null);
  const [selectedStep, setSelectedStep] = useState(null);
  const [showStepConfig, setShowStepConfig] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);

  const dropZoneRef = useRef(null);

  // Available commands that can be dragged
  const availableCommands = [
    { id: 'navigate', icon: Navigation, label: 'Navigate', color: 'bg-blue-100 text-blue-600', description: 'Go to a website' },
    { id: 'click', icon: MousePointer, label: 'Click', color: 'bg-green-100 text-green-600', description: 'Click an element' },
    { id: 'type', icon: Type, label: 'Type', color: 'bg-purple-100 text-purple-600', description: 'Enter text' },
    { id: 'search', icon: Search, label: 'Search', color: 'bg-orange-100 text-orange-600', description: 'Search for content' },
    { id: 'extract', icon: Download, label: 'Extract', color: 'bg-pink-100 text-pink-600', description: 'Extract data' },
    { id: 'wait', icon: Pause, label: 'Wait', color: 'bg-gray-100 text-gray-600', description: 'Pause execution' },
    { id: 'screenshot', icon: Eye, label: 'Screenshot', color: 'bg-indigo-100 text-indigo-600', description: 'Take screenshot' }
  ];

  // Drag and drop handlers
  const handleDragStart = (command) => {
    setDraggedCommand(command);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (draggedCommand) {
      const newStep = {
        id: `step_${Date.now()}`,
        ...draggedCommand,
        params: getDefaultParams(draggedCommand.id),
        order: workflowSteps.length
      };
      
      setWorkflowSteps(prev => [...prev, newStep]);
      setDraggedCommand(null);
    }
  };

  const getDefaultParams = (commandType) => {
    const defaults = {
      navigate: { url: 'https://example.com' },
      click: { selector: 'button', description: 'Click button' },
      type: { selector: 'input', text: 'Sample text' },
      search: { query: 'Search term', engine: 'google' },
      extract: { selector: '.content', attribute: 'text' },
      wait: { duration: 2000 },
      screenshot: { fullPage: false, quality: 80 }
    };
    return defaults[commandType] || {};
  };

  const updateStepParams = (stepId, newParams) => {
    setWorkflowSteps(prev => prev.map(step => 
      step.id === stepId ? { ...step, params: { ...step.params, ...newParams } } : step
    ));
  };

  const removeStep = (stepId) => {
    setWorkflowSteps(prev => prev.filter(step => step.id !== stepId));
    setSelectedStep(null);
    setShowStepConfig(false);
  };

  const moveStep = (stepId, direction) => {
    setWorkflowSteps(prev => {
      const steps = [...prev];
      const index = steps.findIndex(s => s.id === stepId);
      if (index === -1) return steps;
      
      const newIndex = direction === 'up' ? index - 1 : index + 1;
      if (newIndex < 0 || newIndex >= steps.length) return steps;
      
      [steps[index], steps[newIndex]] = [steps[newIndex], steps[index]];
      return steps;
    });
  };

  const executeWorkflow = async () => {
    if (workflowSteps.length === 0) return;
    
    setIsExecuting(true);
    
    const workflow = {
      id: `workflow_${Date.now()}`,
      name: workflowName || 'Untitled Workflow',
      steps: workflowSteps,
      createdAt: new Date()
    };
    
    // Save to built workflows
    setBuiltWorkflows(prev => [...prev, workflow]);
    
    // Execute the workflow
    await onExecuteWorkflow(workflow);
    
    setIsExecuting(false);
  };

  const saveWorkflow = () => {
    if (workflowSteps.length === 0) return;
    
    const workflow = {
      id: `workflow_${Date.now()}`,
      name: workflowName || 'Untitled Workflow',
      steps: workflowSteps,
      createdAt: new Date(),
      saved: true
    };
    
    setBuiltWorkflows(prev => [...prev, workflow]);
    
    // Reset builder
    setWorkflowSteps([]);
    setWorkflowName('');
  };

  const loadWorkflow = (workflow) => {
    setWorkflowName(workflow.name);
    setWorkflowSteps(workflow.steps);
  };

  const clearWorkflow = () => {
    setWorkflowSteps([]);
    setWorkflowName('');
    setSelectedStep(null);
    setShowStepConfig(false);
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Builder Header */}
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Workflow className="w-5 h-5 text-green-600" />
            <h3 className="font-semibold text-gray-800">Visual Workflow Builder</h3>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={clearWorkflow}
              className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Clear Workflow"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <input
          type="text"
          value={workflowName}
          onChange={(e) => setWorkflowName(e.target.value)}
          placeholder="Workflow name..."
          className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
        />
      </div>

      {/* Main Builder Area */}
      <div className="flex-1 flex">
        {/* Command Palette */}
        <div className="w-1/3 p-3 border-r border-gray-200 bg-white">
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Available Commands
          </h4>
          <div className="space-y-2">
            {availableCommands.map((command) => (
              <motion.div
                key={command.id}
                draggable
                onDragStart={() => handleDragStart(command)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`p-3 rounded-lg border-2 border-dashed border-gray-200 ${command.color} cursor-grab active:cursor-grabbing transition-all hover:border-gray-300`}
              >
                <div className="flex items-center space-x-2">
                  <command.icon className="w-4 h-4" />
                  <div>
                    <div className="font-medium text-sm">{command.label}</div>
                    <div className="text-xs opacity-75">{command.description}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Workflow Canvas */}
        <div className="flex-1 p-4">
          <div className="h-full flex flex-col">
            <h4 className="text-sm font-medium text-gray-700 mb-3">
              Workflow Steps ({workflowSteps.length})
            </h4>
            
            <div
              ref={dropZoneRef}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className={`flex-1 border-2 border-dashed rounded-lg p-4 transition-colors ${
                workflowSteps.length === 0 
                  ? 'border-gray-300 bg-gray-50' 
                  : 'border-green-300 bg-green-50/30'
              }`}
            >
              {workflowSteps.length === 0 ? (
                <div className="h-full flex items-center justify-center text-center">
                  <div>
                    <Workflow className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                    <p className="text-sm text-gray-500 mb-1">Drop commands here to build your workflow</p>
                    <p className="text-xs text-gray-400">Drag from the command palette on the left</p>
                  </div>
                </div>
              ) : (
                <div className="space-y-3">
                  {workflowSteps.map((step, index) => (
                    <motion.div
                      key={step.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`flex items-center p-3 bg-white rounded-lg border shadow-sm hover:shadow-md transition-all cursor-pointer ${
                        selectedStep?.id === step.id ? 'ring-2 ring-green-500 border-green-200' : 'border-gray-200'
                      }`}
                      onClick={() => {
                        setSelectedStep(step);
                        setShowStepConfig(true);
                      }}
                    >
                      <div className="flex items-center space-x-3 flex-1">
                        <div className="flex items-center justify-center w-8 h-8 bg-gray-100 rounded-full text-sm font-medium text-gray-600">
                          {index + 1}
                        </div>
                        <step.icon className="w-5 h-5 text-gray-600" />
                        <div className="flex-1">
                          <div className="font-medium text-sm">{step.label}</div>
                          <div className="text-xs text-gray-500">
                            {step.id === 'navigate' ? step.params.url : 
                             step.id === 'click' ? step.params.selector :
                             step.id === 'type' ? `"${step.params.text}"` :
                             step.id === 'search' ? step.params.query :
                             step.id === 'wait' ? `${step.params.duration}ms` :
                             'Configured'}
                          </div>
                        </div>
                        {index < workflowSteps.length - 1 && (
                          <ArrowRight className="w-4 h-4 text-gray-400" />
                        )}
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          removeStep(step.id);
                        }}
                        className="p-1 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </motion.div>
                  ))}
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center space-x-2">
                <button
                  onClick={saveWorkflow}
                  disabled={workflowSteps.length === 0}
                  className="flex items-center space-x-2 px-3 py-2 text-sm bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Save className="w-4 h-4" />
                  <span>Save</span>
                </button>
              </div>
              
              <button
                onClick={executeWorkflow}
                disabled={workflowSteps.length === 0 || isExecuting}
                className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm hover:shadow-md"
              >
                {isExecuting ? (
                  <>
                    <RotateCw className="w-4 h-4 animate-spin" />
                    <span>Executing...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    <span>Execute</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Built Workflows & Shadow Tasks */}
      <div className="border-t border-gray-200 bg-white p-3">
        <div className="flex space-x-6">
          {/* Built Workflows */}
          {builtWorkflows.length > 0 && (
            <div className="flex-1">
              <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                Saved Workflows ({builtWorkflows.length})
              </h5>
              <div className="flex space-x-2 overflow-x-auto">
                {builtWorkflows.slice(-3).map((workflow) => (
                  <button
                    key={workflow.id}
                    onClick={() => loadWorkflow(workflow)}
                    className="flex items-center space-x-2 px-3 py-1.5 bg-purple-50 text-purple-600 rounded-lg hover:bg-purple-100 transition-colors whitespace-nowrap text-sm"
                  >
                    <Workflow className="w-3 h-3" />
                    <span>{workflow.name}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Shadow Tasks Status */}
          {shadowTasks.length > 0 && (
            <div className="flex-1">
              <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                Background Tasks ({shadowTasks.length})
              </h5>
              <div className="flex space-x-2 overflow-x-auto">
                {shadowTasks.slice(-3).map((task) => (
                  <div
                    key={task.id}
                    className="flex items-center space-x-2 px-3 py-1.5 bg-gray-50 rounded-lg text-sm"
                  >
                    {task.status === 'running' ? (
                      <Clock className="w-3 h-3 text-yellow-500" />
                    ) : task.status === 'completed' ? (
                      <CheckCircle className="w-3 h-3 text-green-500" />
                    ) : (
                      <XCircle className="w-3 h-3 text-red-500" />
                    )}
                    <span className="text-gray-600 truncate max-w-24">{task.name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Step Configuration Modal */}
      <AnimatePresence>
        {showStepConfig && selectedStep && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
            onClick={() => setShowStepConfig(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-lg shadow-xl p-6 w-96 max-w-full mx-4"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold flex items-center space-x-2">
                  <selectedStep.icon className="w-5 h-5" />
                  <span>Configure {selectedStep.label}</span>
                </h3>
                <button
                  onClick={() => setShowStepConfig(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>

              {/* Dynamic configuration based on step type */}
              <div className="space-y-4">
                {selectedStep.id === 'navigate' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">URL</label>
                    <input
                      type="url"
                      value={selectedStep.params.url || ''}
                      onChange={(e) => updateStepParams(selectedStep.id, { url: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="https://example.com"
                    />
                  </div>
                )}

                {selectedStep.id === 'click' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">CSS Selector</label>
                      <input
                        type="text"
                        value={selectedStep.params.selector || ''}
                        onChange={(e) => updateStepParams(selectedStep.id, { selector: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                        placeholder="button, .class, #id"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                      <input
                        type="text"
                        value={selectedStep.params.description || ''}
                        onChange={(e) => updateStepParams(selectedStep.id, { description: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                        placeholder="Click the submit button"
                      />
                    </div>
                  </>
                )}

                {selectedStep.id === 'type' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">CSS Selector</label>
                      <input
                        type="text"
                        value={selectedStep.params.selector || ''}
                        onChange={(e) => updateStepParams(selectedStep.id, { selector: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                        placeholder="input, textarea, [contenteditable]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Text to Type</label>
                      <textarea
                        value={selectedStep.params.text || ''}
                        onChange={(e) => updateStepParams(selectedStep.id, { text: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                        rows="3"
                        placeholder="Text to enter"
                      />
                    </div>
                  </>
                )}

                {selectedStep.id === 'wait' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Duration (milliseconds)</label>
                    <input
                      type="number"
                      value={selectedStep.params.duration || 2000}
                      onChange={(e) => updateStepParams(selectedStep.id, { duration: parseInt(e.target.value) })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                      min="100"
                      step="100"
                    />
                  </div>
                )}
              </div>

              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => setShowStepConfig(false)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  Close
                </button>
                <button
                  onClick={() => setShowStepConfig(false)}
                  className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                >
                  Save
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default VisualWorkflowBuilder;