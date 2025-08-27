/**
 * Advanced Workflow Engine
 * Handles complex multi-step browser automation workflows
 */

const { v4: uuidv4 } = require('uuid');

class WorkflowEngine {
  constructor() {
    this.workflows = new Map();
    this.activeExecutions = new Map();
    this.workflowTemplates = new Map();
    this.executionHistory = [];
  }

  /**
   * Create a new workflow from AI-generated tasks
   */
  async createWorkflow(name, description, tasks, options = {}) {
    const workflowId = uuidv4();
    
    const workflow = {
      id: workflowId,
      name: name,
      description: description,
      tasks: this.processTasks(tasks),
      options: {
        parallel: options.parallel || false,
        maxRetries: options.maxRetries || 3,
        timeout: options.timeout || 60000,
        ...options
      },
      created: new Date().toISOString(),
      version: '1.0.0'
    };
    
    this.workflows.set(workflowId, workflow);
    console.log(`📋 Workflow created: ${name} (${workflowId})`);
    
    return workflow;
  }

  /**
   * Execute a workflow with enhanced monitoring
   */
  async execute(workflow, context = {}) {
    // Handle both new workflow format and legacy test format
    if (!workflow.id && !workflow.name) {
      // This is a legacy test workflow, convert it
      workflow = {
        id: workflow.id || 'legacy_workflow',
        name: workflow.name || 'Legacy Workflow',
        tasks: workflow.steps || workflow.tasks || [],
        options: workflow.options || {}
      };
    }

    const executionId = uuidv4();
    
    console.log(`🚀 Executing workflow: ${workflow.name}`);
    
    const execution = {
      id: executionId,
      workflowId: workflow.id,
      status: 'running',
      startTime: Date.now(),
      context: context,
      results: new Map(),
      errors: [],
      progress: 0
    };
    
    this.activeExecutions.set(executionId, execution);
    
    try {
      const results = await this.executeWorkflowTasks(workflow, execution);
      
      execution.status = 'completed';
      execution.endTime = Date.now();
      execution.duration = execution.endTime - execution.startTime;
      execution.progress = 100;
      
      console.log(`✅ Workflow completed: ${workflow.name} (${execution.duration}ms)`);
      
      // Store in history
      this.executionHistory.push({
        ...execution,
        summary: this.generateExecutionSummary(execution, results)
      });
      
      return {
        id: executionId,
        status: 'completed', // Add status for legacy compatibility
        success: true,
        results: Array.from(results.values()), // Convert Map to Array for compatibility
        duration: execution.duration,
        summary: this.generateExecutionSummary(execution, results)
      };
      
    } catch (error) {
      execution.status = 'failed';
      execution.error = error.message;
      execution.endTime = Date.now();
      execution.duration = execution.endTime - execution.startTime;
      
      console.error(`❌ Workflow failed: ${workflow.name}`, error);
      
      return {
        id: executionId,
        status: 'failed',
        success: false,
        error: error.message,
        results: Array.from(execution.results.values()),
        duration: execution.duration
      };
    } finally {
      this.activeExecutions.delete(executionId);
    }
  }

  /**
   * Execute workflow tasks with proper dependency management
   */
  async executeWorkflowTasks(workflow, execution) {
    const tasks = workflow.tasks || workflow.steps; // Support both tasks and steps
    const results = new Map();
    
    // Ensure workflow has options
    const options = workflow.options || {};
    
    if (options.parallel) {
      // Execute tasks in parallel where possible
      return await this.executeParallelTasks(tasks, execution, results);
    } else {
      // Execute tasks sequentially
      return await this.executeSequentialTasks(tasks, execution, results);
    }
  }

  /**
   * Execute tasks in parallel with dependency resolution
   */
  async executeParallelTasks(tasks, execution, results) {
    const taskGroups = this.groupTasksByDependencies(tasks);
    
    for (const group of taskGroups) {
      const promises = group.map(task => this.executeTask(task, execution, results));
      const groupResults = await Promise.allSettled(promises);
      
      // Process results
      groupResults.forEach((result, index) => {
        const task = group[index];
        if (result.status === 'fulfilled') {
          results.set(task.id, result.value);
        } else {
          execution.errors.push({
            taskId: task.id,
            error: result.reason.message,
            timestamp: Date.now()
          });
        }
      });
      
      // Update progress
      execution.progress = (results.size / tasks.length) * 100;
    }
    
    return results;
  }

  /**
   * Execute tasks sequentially
   */
  async executeSequentialTasks(tasks, execution, results) {
    for (const task of tasks) {
      try {
        const result = await this.executeTask(task, execution, results);
        results.set(task.id, result);
        
        // Update progress
        execution.progress = (results.size / tasks.length) * 100;
        
      } catch (error) {
        execution.errors.push({
          taskId: task.id,
          error: error.message,
          timestamp: Date.now()
        });
        
        if (!task.optional) {
          throw error; // Stop execution on critical task failure
        }
      }
    }
    
    return results;
  }

  /**
   * Execute individual task with context and retries
   */
  async executeTask(task, execution, previousResults) {
    const maxRetries = task.retries || execution.context.maxRetries || 3;
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        console.log(`⚡ Executing task: ${task.name} (attempt ${attempt})`);
        
        // Build task context
        const taskContext = {
          ...execution.context,
          previousResults: Object.fromEntries(previousResults),
          attempt: attempt,
          workflowId: execution.workflowId
        };
        
        // Execute based on task type
        const result = await this.executeTaskByType(task, taskContext);
        
        console.log(`✅ Task completed: ${task.name}`);
        return {
          success: true,
          data: result,
          attempts: attempt,
          duration: Date.now() - execution.startTime
        };
        
      } catch (error) {
        lastError = error;
        console.warn(`⚠️ Task attempt ${attempt} failed: ${task.name}`, error.message);
        
        if (attempt < maxRetries) {
          // Wait before retry (exponential backoff)
          await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
        }
      }
    }
    
    // All attempts failed
    throw new Error(`Task failed after ${maxRetries} attempts: ${lastError.message}`);
  }

  /**
   * Execute task based on its type
   */
  async executeTaskByType(task, context) {
    const { page, browserAutomation, aiIntegration } = context;
    
    switch (task.type) {
      case 'navigate':
        if (page && task.params.url) {
          await page.goto(task.params.url, { waitUntil: 'networkidle' });
          return {
            action: 'navigated',
            url: page.url(),
            title: await page.title()
          };
        }
        break;
        
      case 'click':
        if (page && task.params.selector) {
          await page.waitForSelector(task.params.selector, { timeout: 10000 });
          await page.click(task.params.selector);
          return {
            action: 'clicked',
            selector: task.params.selector
          };
        }
        break;
        
      case 'type':
        if (page && task.params.selector && task.params.text) {
          await page.waitForSelector(task.params.selector);
          await page.fill(task.params.selector, task.params.text);
          return {
            action: 'typed',
            selector: task.params.selector,
            text: task.params.text
          };
        }
        break;
        
      case 'extract':
        if (page && task.params.selector) {
          const data = await page.$$eval(task.params.selector, els => 
            els.map(el => el.textContent?.trim()).filter(text => text)
          );
          return {
            action: 'extracted',
            selector: task.params.selector,
            data: data,
            count: data.length
          };
        }
        break;
        
      case 'wait':
        const duration = task.params.duration || 1000;
        await new Promise(resolve => setTimeout(resolve, duration));
        return {
          action: 'waited',
          duration: duration
        };
        
      case 'screenshot':
        if (page) {
          const screenshot = await page.screenshot({
            fullPage: task.params.fullPage || false,
            quality: task.params.quality || 90
          });
          return {
            action: 'screenshot',
            screenshot: screenshot.toString('base64')
          };
        }
        break;
        
      case 'ai_analyze':
        if (aiIntegration && task.params.content) {
          // This would integrate with your AI system for content analysis
          return {
            action: 'ai_analyzed',
            content: task.params.content,
            analysis: 'AI analysis placeholder'
          };
        }
        break;
        
      default:
        throw new Error(`Unknown task type: ${task.type}`);
    }
    
    throw new Error(`Failed to execute task: ${task.type} - missing parameters or context`);
  }

  /**
   * Process and validate tasks
   */
  processTasks(tasks) {
    return tasks.map((task, index) => ({
      id: task.id || `task_${index + 1}`,
      name: task.name || `Task ${index + 1}`,
      type: task.type,
      description: task.description || '',
      params: task.params || {},
      dependencies: task.dependencies || [],
      optional: task.optional || false,
      retries: task.retries || 3,
      timeout: task.timeout || 30000
    }));
  }

  /**
   * Group tasks by their dependencies for parallel execution
   */
  groupTasksByDependencies(tasks) {
    const groups = [];
    const processed = new Set();
    const taskMap = new Map(tasks.map(t => [t.id, t]));
    
    while (processed.size < tasks.length) {
      const currentGroup = [];
      
      for (const task of tasks) {
        if (processed.has(task.id)) continue;
        
        // Check if all dependencies are satisfied
        const dependenciesMet = task.dependencies.every(dep => processed.has(dep));
        
        if (dependenciesMet) {
          currentGroup.push(task);
        }
      }
      
      if (currentGroup.length === 0) {
        // Circular dependency or unresolvable dependencies
        const remaining = tasks.filter(t => !processed.has(t.id));
        console.warn('⚠️ Circular dependencies detected, adding remaining tasks');
        currentGroup.push(...remaining);
      }
      
      groups.push(currentGroup);
      currentGroup.forEach(task => processed.add(task.id));
    }
    
    return groups;
  }

  /**
   * Generate execution summary
   */
  generateExecutionSummary(execution, results) {
    const successful = Array.from(results.values()).filter(r => r.success).length;
    const failed = execution.errors.length;
    
    return {
      totalTasks: results.size + failed,
      successful: successful,
      failed: failed,
      duration: execution.duration,
      status: execution.status,
      efficiency: successful / (successful + failed) * 100
    };
  }

  /**
   * Get workflow execution status
   */
  getExecutionStatus(executionId) {
    return this.activeExecutions.get(executionId);
  }

  /**
   * Get workflow history
   */
  getExecutionHistory(limit = 10) {
    return this.executionHistory.slice(-limit);
  }

  /**
   * Create workflow template
   */
  createTemplate(name, description, taskTemplates) {
    const templateId = uuidv4();
    
    const template = {
      id: templateId,
      name: name,
      description: description,
      taskTemplates: taskTemplates,
      created: new Date().toISOString()
    };
    
    this.workflowTemplates.set(templateId, template);
    return template;
  }

  /**
   * Generate workflow from template
   */
  generateFromTemplate(templateId, parameters = {}) {
    const template = this.workflowTemplates.get(templateId);
    if (!template) {
      throw new Error(`Template not found: ${templateId}`);
    }
    
    // Process template with parameters
    const tasks = template.taskTemplates.map(taskTemplate => {
      const task = { ...taskTemplate };
      
      // Replace parameter placeholders
      if (task.params) {
        task.params = this.replaceParameters(task.params, parameters);
      }
      
      return task;
    });
    
    return this.createWorkflow(
      template.name,
      template.description,
      tasks
    );
  }

  /**
   * Replace parameter placeholders in task parameters
   */
  replaceParameters(params, parameters) {
    const processed = { ...params };
    
    for (const [key, value] of Object.entries(processed)) {
      if (typeof value === 'string' && value.includes('{{')) {
        processed[key] = value.replace(/\{\{(\w+)\}\}/g, (match, paramName) => {
          return parameters[paramName] || match;
        });
      }
    }
    
    return processed;
  }
}

module.exports = WorkflowEngine;