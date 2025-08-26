/**
 * Workflow Engine - Local-First Implementation
 * Executes workflows locally with native browser automation
 */

const { v4: uuidv4 } = require('uuid');

class WorkflowEngine {
  constructor() {
    this.activeWorkflows = new Map();
    this.workflowHistory = [];
  }

  /**
   * Execute a workflow locally
   */
  async execute(workflow, context = {}) {
    const executionId = uuidv4();
    const execution = {
      id: executionId,
      workflowId: workflow.id || uuidv4(),
      name: workflow.name,
      steps: workflow.steps || [],
      status: 'running',
      startTime: new Date(),
      results: [],
      context: context
    };

    this.activeWorkflows.set(executionId, execution);

    try {
      console.log(`🔄 Starting workflow execution: ${workflow.name} (${executionId})`);

      const { page, browserAutomation, aiIntegration } = context;
      
      if (!page) {
        throw new Error('Browser page context required for workflow execution');
      }

      // Execute steps sequentially
      for (let i = 0; i < execution.steps.length; i++) {
        const step = execution.steps[i];
        const stepResult = await this.executeStep(step, {
          page,
          browserAutomation,
          aiIntegration,
          workflowContext: execution,
          stepIndex: i
        });

        execution.results.push(stepResult);

        // Update workflow status
        execution.status = stepResult.success ? 'running' : 'failed';
        
        if (!stepResult.success) {
          console.error(`❌ Workflow step ${i + 1} failed:`, stepResult.error);
          break;
        }

        console.log(`✅ Workflow step ${i + 1} completed:`, stepResult.action);

        // Add delay between steps if specified
        if (step.delay) {
          await new Promise(resolve => setTimeout(resolve, step.delay));
        }
      }

      // Mark as completed if all steps succeeded
      if (execution.status === 'running') {
        execution.status = 'completed';
      }

      execution.endTime = new Date();
      execution.duration = execution.endTime - execution.startTime;

      console.log(`🎉 Workflow execution ${execution.status}: ${workflow.name}`);

      // Move to history
      this.workflowHistory.push(execution);
      this.activeWorkflows.delete(executionId);

      return execution;

    } catch (error) {
      console.error(`❌ Workflow execution failed:`, error);
      
      execution.status = 'failed';
      execution.error = error.message;
      execution.endTime = new Date();
      execution.duration = execution.endTime - execution.startTime;

      this.workflowHistory.push(execution);
      this.activeWorkflows.delete(executionId);

      throw error;
    }
  }

  /**
   * Execute a single workflow step
   */
  async executeStep(step, context) {
    const { page, browserAutomation, aiIntegration, stepIndex } = context;
    
    try {
      console.log(`⚡ Executing step ${stepIndex + 1}: ${step.type}`);

      switch (step.type) {
        case 'navigate':
          return await browserAutomation.executeCommand(page, 'navigate', {
            url: step.url || step.params?.url
          });

        case 'click':
          return await browserAutomation.executeCommand(page, 'click', {
            selector: step.selector || step.params?.selector
          });

        case 'type':
          return await browserAutomation.executeCommand(page, 'type', {
            selector: step.selector || step.params?.selector,
            text: step.text || step.params?.text
          });

        case 'wait':
          return await browserAutomation.executeCommand(page, 'wait', {
            duration: step.duration || step.params?.duration || 1000
          });

        case 'wait_for':
          return await browserAutomation.executeCommand(page, 'waitForSelector', {
            selector: step.selector || step.params?.selector,
            timeout: step.timeout || step.params?.timeout || 10000
          });

        case 'extract':
          return await browserAutomation.executeCommand(page, 'extract', {
            selector: step.selector || step.params?.selector,
            attribute: step.attribute || step.params?.attribute || 'textContent'
          });

        case 'screenshot':
          return await browserAutomation.executeCommand(page, 'screenshot', {
            options: step.options || step.params || {}
          });

        case 'search':
          return await browserAutomation.executeCommand(page, 'search', {
            query: step.query || step.params?.query
          });

        case 'ai_process':
          if (!aiIntegration) {
            throw new Error('AI integration not available');
          }
          
          const aiResult = await aiIntegration.processQuery(
            step.query || step.params?.query,
            {
              currentUrl: page.url(),
              pageTitle: await page.title(),
              workflowContext: true
            }
          );
          
          return {
            action: 'ai_processed',
            success: true,
            result: aiResult
          };

        case 'condition':
          return await this.evaluateCondition(step, { page, browserAutomation });

        case 'loop':
          return await this.executeLoop(step, context);

        case 'script':
          const scriptResult = await page.evaluate(step.script || step.params?.script);
          return {
            action: 'script_executed',
            success: true,
            result: scriptResult
          };

        default:
          throw new Error(`Unknown step type: ${step.type}`);
      }

    } catch (error) {
      return {
        action: step.type,
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Evaluate a condition step
   */
  async evaluateCondition(step, context) {
    const { page, browserAutomation } = context;
    
    try {
      const { condition, onTrue, onFalse } = step.params || step;
      
      let conditionResult = false;
      
      if (condition.type === 'element_exists') {
        const element = await page.$(condition.selector);
        conditionResult = !!element;
      } else if (condition.type === 'url_contains') {
        conditionResult = page.url().includes(condition.value);
      } else if (condition.type === 'text_contains') {
        const text = await page.textContent('body');
        conditionResult = text.includes(condition.value);
      } else if (condition.type === 'script') {
        conditionResult = await page.evaluate(condition.script);
      }
      
      // Execute appropriate branch
      const branchSteps = conditionResult ? onTrue : onFalse;
      if (branchSteps && branchSteps.length > 0) {
        const branchResults = [];
        for (const branchStep of branchSteps) {
          const result = await this.executeStep(branchStep, context);
          branchResults.push(result);
          if (!result.success) break;
        }
        
        return {
          action: 'condition_evaluated',
          success: true,
          conditionResult: conditionResult,
          branchResults: branchResults
        };
      }
      
      return {
        action: 'condition_evaluated',
        success: true,
        conditionResult: conditionResult
      };
      
    } catch (error) {
      return {
        action: 'condition_evaluated',
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Execute a loop step
   */
  async executeLoop(step, context) {
    const { iterations, steps: loopSteps } = step.params || step;
    const results = [];
    
    try {
      for (let i = 0; i < iterations; i++) {
        console.log(`🔄 Loop iteration ${i + 1}/${iterations}`);
        
        for (const loopStep of loopSteps) {
          const result = await this.executeStep(loopStep, {
            ...context,
            loopIteration: i
          });
          
          results.push(result);
          
          if (!result.success) {
            throw new Error(`Loop failed at iteration ${i + 1}: ${result.error}`);
          }
        }
      }
      
      return {
        action: 'loop_executed',
        success: true,
        iterations: iterations,
        results: results
      };
      
    } catch (error) {
      return {
        action: 'loop_executed',
        success: false,
        error: error.message,
        completedIterations: results.length / loopSteps.length,
        results: results
      };
    }
  }

  /**
   * Get workflow execution status
   */
  getExecutionStatus(executionId) {
    const activeExecution = this.activeWorkflows.get(executionId);
    if (activeExecution) {
      return {
        ...activeExecution,
        isActive: true
      };
    }

    const historyExecution = this.workflowHistory.find(w => w.id === executionId);
    if (historyExecution) {
      return {
        ...historyExecution,
        isActive: false
      };
    }

    return null;
  }

  /**
   * Get all active workflows
   */
  getActiveWorkflows() {
    return Array.from(this.activeWorkflows.values());
  }

  /**
   * Get workflow history
   */
  getWorkflowHistory(limit = 50) {
    return this.workflowHistory.slice(-limit);
  }

  /**
   * Cancel a running workflow
   */
  cancelWorkflow(executionId) {
    const execution = this.activeWorkflows.get(executionId);
    if (execution) {
      execution.status = 'cancelled';
      execution.endTime = new Date();
      execution.duration = execution.endTime - execution.startTime;
      
      this.workflowHistory.push(execution);
      this.activeWorkflows.delete(executionId);
      
      return true;
    }
    return false;
  }

  /**
   * Create a workflow from AI conversation
   */
  createWorkflowFromAI(aiResponse, userQuery) {
    if (!aiResponse.commands || aiResponse.commands.length === 0) {
      return null;
    }

    const workflow = {
      id: uuidv4(),
      name: `AI Generated: ${userQuery.slice(0, 50)}...`,
      description: aiResponse.explanation || 'Workflow generated from AI conversation',
      steps: aiResponse.commands.map((command, index) => ({
        id: `step_${index + 1}`,
        type: command.type,
        params: command.params || {},
        description: command.description || `${command.type} action`
      })),
      created: new Date(),
      source: 'ai_conversation',
      originalQuery: userQuery
    };

    return workflow;
  }
}

module.exports = WorkflowEngine;