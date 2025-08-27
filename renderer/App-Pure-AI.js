import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Send, Loader } from 'lucide-react';
import './App.css';

function PureAIApp() {
  // Pure AI State - Minimal UI
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [aiStatus, setAiStatus] = useState('initializing');
  const [capabilities, setCapabilities] = useState([]);
  const messagesEndRef = useRef(null);

  // Initialize AI System
  useEffect(() => {
    initializeAI();
  }, []);

  // Auto-scroll to latest message
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const initializeAI = async () => {
    try {
      setAiStatus('initializing');
      
      // Initialize Pure NLP Interface
      if (window.kairoAPI && window.kairoAPI.ai) {
        const result = await window.kairoAPI.ai.initialize();
        
        if (result.success) {
          setAiStatus('ready');
          setCapabilities(result.capabilities || []);
          
          // Add welcome message
          addMessage({
            role: 'assistant',
            content: result.message,
            type: 'welcome',
            timestamp: new Date()
          });
        } else {
          setAiStatus('error');
          addMessage({
            role: 'assistant',
            content: 'I encountered an issue starting up. Let me try again...',
            type: 'error',
            timestamp: new Date()
          });
        }
      } else {
        // Fallback mode
        setAiStatus('fallback');
        addMessage({
          role: 'assistant',
          content: "Hello! I'm your AI assistant. I can help you browse the web, search for information, analyze data, and much more. Just tell me what you want to do in natural language!",
          type: 'welcome',
          timestamp: new Date()
        });
      }
    } catch (error) {
      console.error('AI initialization error:', error);
      setAiStatus('error');
    }
  };

  const addMessage = (message) => {
    setMessages(prev => [...prev, { ...message, id: Date.now() }]);
  };

  const handleUserInput = async (input) => {
    if (!input.trim() || isProcessing) return;

    // Add user message
    addMessage({
      role: 'user',
      content: input,
      timestamp: new Date()
    });

    setInputValue('');
    setIsProcessing(true);

    try {
      // Send to AI for processing
      if (window.kairoAPI && window.kairoAPI.ai) {
        const response = await window.kairoAPI.ai.processInput(input, {
          timestamp: new Date().toISOString(),
          conversationHistory: messages.slice(-10) // Last 10 messages for context
        });

        if (response.success) {
          // Add AI response
          addMessage({
            role: 'assistant',
            content: response.message,
            data: response.data,
            proactiveActions: response.proactiveActions,
            tasksSummary: response.tasksSummary,
            browserResults: response.browserResults,
            timestamp: new Date()
          });

          // Add proactive suggestions if available
          if (response.proactiveActions && response.proactiveActions.length > 0) {
            setTimeout(() => {
              addMessage({
                role: 'assistant',
                content: 'Here are some suggestions for what you might want to do next:',
                type: 'suggestions',
                suggestions: response.proactiveActions,
                timestamp: new Date()
              });
            }, 1000);
          }
        } else {
          addMessage({
            role: 'assistant',
            content: response.message || "I'm having trouble processing that request. Could you try rephrasing it?",
            type: 'error',
            timestamp: new Date()
          });
        }
      } else {
        // Fallback response
        addMessage({
          role: 'assistant',
          content: `I understand you want: "${input}". In full mode, I would execute this automatically across websites. Currently running in demo mode.`,
          timestamp: new Date()
        });
      }
    } catch (error) {
      console.error('Error processing input:', error);
      addMessage({
        role: 'assistant',
        content: "I encountered an unexpected error. Let me try to help you differently - what specifically would you like me to do?",
        type: 'error',
        timestamp: new Date()
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleUserInput(inputValue);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleUserInput(suggestion);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="pure-ai-app min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white flex flex-col">
      {/* Minimal Header */}
      <div className="header bg-black/50 backdrop-blur-sm px-6 py-4 border-b border-gray-700/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Bot className="w-8 h-8 text-blue-400" />
              <div className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full ${
                aiStatus === 'ready' ? 'bg-green-400' : 
                aiStatus === 'initializing' ? 'bg-yellow-400 animate-pulse' : 
                'bg-red-400'
              }`}></div>
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Kairo AI Assistant
              </h1>
              <p className="text-sm text-gray-400">
                {aiStatus === 'ready' && 'AI Ready - Just tell me what you want to do'}
                {aiStatus === 'initializing' && 'Starting up...'}
                {aiStatus === 'error' && 'Having issues - trying to reconnect'}
                {aiStatus === 'fallback' && 'Demo mode - limited functionality'}
              </p>
            </div>
          </div>
          
          {/* Status Indicator */}
          <div className="text-right">
            <div className="text-xs text-gray-400">
              {messages.length > 0 && `${messages.length} messages`}
            </div>
            {isProcessing && (
              <div className="flex items-center space-x-2 text-blue-400">
                <Loader className="w-4 h-4 animate-spin" />
                <span className="text-xs">AI working...</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Pure Conversation Interface */}
      <div className="flex-1 flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
          {messages.length === 0 && aiStatus !== 'initializing' && (
            <div className="text-center py-12">
              <Bot className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <h2 className="text-2xl font-semibold mb-2 text-gray-300">
                Ready to help!
              </h2>
              <p className="text-gray-400 mb-6 max-w-md mx-auto">
                Tell me anything you want to do. I can browse websites, search for information, 
                analyze data, create reports, and much more - all through natural conversation.
              </p>
              
              {/* Quick Examples */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                {[
                  "Find iPhone prices on 3 different websites",
                  "Search for AI news on YouTube and Google",
                  "Compare laptop specs and create a report", 
                  "Monitor a website for price changes"
                ].map((example, index) => (
                  <button
                    key={index}
                    onClick={() => handleUserInput(example)}
                    className="p-3 bg-gray-800/50 hover:bg-gray-700/50 rounded-lg border border-gray-700 text-sm text-left transition-colors"
                  >
                    💡 {example}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Message List */}
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-4xl ${message.role === 'user' ? 'ml-12' : 'mr-12'}`}>
                  {/* Message Bubble */}
                  <div
                    className={`p-4 rounded-2xl ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white ml-auto'
                        : message.type === 'error'
                        ? 'bg-red-900/50 border border-red-500/50 text-red-100'
                        : message.type === 'welcome'
                        ? 'bg-gradient-to-r from-purple-900/50 to-blue-900/50 border border-purple-500/50'
                        : 'bg-gray-800/80 backdrop-blur border border-gray-700/50'
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      {message.role === 'assistant' && (
                        <Bot className="w-6 h-6 text-blue-400 flex-shrink-0 mt-0.5" />
                      )}
                      
                      <div className="flex-1">
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">
                          {message.content}
                        </p>
                        
                        {/* Task Summary */}
                        {message.tasksSummary && (
                          <div className="mt-3 p-3 bg-black/30 rounded-lg border border-gray-600/50">
                            <div className="text-xs text-gray-400 mb-1">Task Execution Summary:</div>
                            <div className="flex items-center space-x-4 text-sm">
                              <span className="text-green-400">
                                ✅ {message.tasksSummary.successful} completed
                              </span>
                              <span className="text-blue-400">
                                ⏱ {message.tasksSummary.duration}ms
                              </span>
                              <span className="text-gray-400">
                                📋 {message.tasksSummary.completed} total tasks
                              </span>
                            </div>
                          </div>
                        )}

                        {/* Browser Results */}
                        {message.browserResults && message.browserResults.length > 0 && (
                          <div className="mt-3 space-y-2">
                            <div className="text-xs text-gray-400">Browser Operations:</div>
                            {message.browserResults.slice(0, 3).map(([taskId, result], index) => (
                              <div key={index} className="p-2 bg-black/30 rounded border border-gray-600/30 text-xs">
                                <div className="flex items-center space-x-2">
                                  <span className={result.success ? 'text-green-400' : 'text-red-400'}>
                                    {result.success ? '✅' : '❌'}
                                  </span>
                                  <span className="text-gray-300">{result.action || taskId}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}

                        {/* Suggestions */}
                        {message.type === 'suggestions' && message.suggestions && (
                          <div className="mt-3 space-y-2">
                            {message.suggestions.map((suggestion, index) => (
                              <button
                                key={index}
                                onClick={() => handleSuggestionClick(suggestion)}
                                className="block w-full p-2 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 rounded-lg text-left text-sm transition-colors"
                              >
                                💡 {suggestion}
                              </button>
                            ))}
                          </div>
                        )}
                        
                        {/* Timestamp */}
                        <div className="mt-2 text-xs text-gray-500">
                          {formatTimestamp(message.timestamp)}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Processing Indicator */}
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start mr-12"
            >
              <div className="max-w-xs">
                <div className="bg-gray-800/80 backdrop-blur border border-gray-700/50 p-4 rounded-2xl">
                  <div className="flex items-center space-x-3">
                    <Bot className="w-6 h-6 text-blue-400" />
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-sm text-gray-400">AI is working...</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-700/50 bg-black/30 backdrop-blur-sm p-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-end space-x-4">
              <div className="flex-1">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Tell me what you want me to do... (e.g., 'Find and compare iPhone prices on Amazon and Best Buy')"
                  className="w-full bg-gray-800/50 border border-gray-600/50 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 resize-none"
                  rows={inputValue.split('\n').length}
                  disabled={isProcessing}
                />
                <div className="flex items-center justify-between mt-2">
                  <div className="text-xs text-gray-500">
                    Press Enter to send, Shift+Enter for new line
                  </div>
                  <div className="text-xs text-gray-500">
                    {inputValue.length} characters
                  </div>
                </div>
              </div>
              
              <button
                onClick={() => handleUserInput(inputValue)}
                disabled={!inputValue.trim() || isProcessing}
                className="p-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-xl transition-colors"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PureAIApp;