import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Clock, 
  Search, 
  Filter, 
  Calendar,
  Globe,
  Bot,
  Zap,
  BarChart3,
  FileText,
  Settings,
  Star,
  ArrowRight,
  Play,
  Pause,
  RotateCcw,
  X,
  ChevronDown,
  ChevronUp,
  BookOpen,
  Target,
  TrendingUp
} from 'lucide-react';
import { useSession } from '../contexts/SessionContext';

const IntelligentTimeline = ({ isOpen, onClose }) => {
  const { sessionId } = useSession();
  const [timelineData, setTimelineData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [selectedDate, setSelectedDate] = useState('today');
  const [isLoading, setIsLoading] = useState(false);
  const [expandedItems, setExpandedItems] = useState(new Set());
  const [workspaces, setWorkspaces] = useState([]);
  const [selectedWorkspace, setSelectedWorkspace] = useState('default');
  
  const timelineRef = useRef(null);

  // Sample timeline data structure
  const sampleData = [
    {
      id: '1',
      timestamp: new Date('2025-01-15T10:30:00'),
      type: 'navigation',
      icon: Globe,
      title: 'Navigated to YouTube',
      description: 'AI assistant opened YouTube for video research',
      details: {
        url: 'https://youtube.com',
        command: 'Open YouTube',
        duration: 2.3,
        success: true
      },
      workspace: 'research',
      tags: ['youtube', 'video', 'research']
    },
    {
      id: '2',
      timestamp: new Date('2025-01-15T10:45:00'),
      type: 'search',
      icon: Search,
      title: 'Deep Search: AI Tutorials',
      description: 'Conducted parallel search across 5 sources',
      details: {
        query: 'AI machine learning tutorials',
        sources: ['Google', 'YouTube', 'Reddit', 'GitHub', 'StackOverflow'],
        results: 47,
        duration: 8.2
      },
      workspace: 'research',
      tags: ['ai', 'tutorials', 'learning']
    },
    {
      id: '3',
      timestamp: new Date('2025-01-15T11:15:00'),
      type: 'automation',
      icon: Zap,
      title: 'Workflow Executed: Data Collection',
      description: 'Automated data scraping from 3 websites',
      details: {
        workflow: 'Research Data Collection',
        sites: ['site1.com', 'site2.com', 'site3.com'],
        dataPoints: 127,
        success: true
      },
      workspace: 'work',
      tags: ['automation', 'scraping', 'data']
    },
    {
      id: '4',
      timestamp: new Date('2025-01-15T11:30:00'),
      type: 'report',
      icon: FileText,
      title: 'Generated Research Report',
      description: 'AI composed comprehensive analysis report',
      details: {
        reportType: 'Research Analysis',
        pages: 12,
        sections: 5,
        visualizations: 3
      },
      workspace: 'research',
      tags: ['report', 'analysis', 'documentation']
    },
    {
      id: '5',
      timestamp: new Date('2025-01-15T12:00:00'),
      type: 'ai_interaction',
      icon: Bot,
      title: 'AI Context Suggestion',
      description: 'Proactive intelligence suggested next actions',
      details: {
        suggestions: ['Check emails', 'Review calendar', 'Update project status'],
        confidence: 0.87,
        context: 'work productivity'
      },
      workspace: 'work',
      tags: ['ai', 'suggestions', 'productivity']
    }
  ];

  useEffect(() => {
    if (isOpen) {
      loadTimelineData();
    }
  }, [isOpen, selectedDate, sessionId]);

  useEffect(() => {
    filterTimelineData();
  }, [timelineData, searchTerm, selectedFilter, selectedWorkspace]);

  const loadTimelineData = async () => {
    setIsLoading(true);
    try {
      // In real implementation, this would fetch from backend
      // const response = await fetch(`/api/timeline?session=${sessionId}&date=${selectedDate}`);
      // const data = await response.json();
      
      // For demo, use sample data
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      setTimelineData(sampleData);
      
      // Extract workspaces
      const uniqueWorkspaces = [...new Set(sampleData.map(item => item.workspace))];
      setWorkspaces([
        { id: 'all', name: 'All Workspaces' },
        ...uniqueWorkspaces.map(ws => ({ id: ws, name: ws.charAt(0).toUpperCase() + ws.slice(1) }))
      ]);
    } catch (error) {
      console.error('Failed to load timeline data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filterTimelineData = () => {
    let filtered = timelineData;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(item => 
        item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter by type
    if (selectedFilter !== 'all') {
      filtered = filtered.filter(item => item.type === selectedFilter);
    }

    // Filter by workspace
    if (selectedWorkspace !== 'all') {
      filtered = filtered.filter(item => item.workspace === selectedWorkspace);
    }

    setFilteredData(filtered);
  };

  const toggleItemExpansion = (itemId) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(itemId)) {
      newExpanded.delete(itemId);
    } else {
      newExpanded.add(itemId);
    }
    setExpandedItems(newExpanded);
  };

  const replayAction = async (item) => {
    // Implementation for replaying actions
    console.log('Replaying action:', item);
  };

  const createWorkspace = () => {
    const name = prompt('Enter workspace name:');
    if (name) {
      setWorkspaces(prev => [...prev, { id: name.toLowerCase(), name }]);
    }
  };

  const getTypeIcon = (type) => {
    const icons = {
      navigation: Globe,
      search: Search,
      automation: Zap,
      report: FileText,
      ai_interaction: Bot,
      analytics: BarChart3
    };
    return icons[type] || Target;
  };

  const getTypeColor = (type) => {
    const colors = {
      navigation: 'bg-blue-100 text-blue-600',
      search: 'bg-green-100 text-green-600',
      automation: 'bg-purple-100 text-purple-600',
      report: 'bg-orange-100 text-orange-600',
      ai_interaction: 'bg-pink-100 text-pink-600',
      analytics: 'bg-indigo-100 text-indigo-600'
    };
    return colors[type] || 'bg-gray-100 text-gray-600';
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatDuration = (seconds) => {
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds.toFixed(0)}s`;
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
          className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl h-[85vh] flex flex-col overflow-hidden"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold flex items-center">
                  <Clock className="w-6 h-6 mr-3" />
                  Intelligent Timeline
                </h2>
                <p className="text-indigo-100 mt-1">Your AI-powered activity history and workspace management</p>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-white/20 rounded-lg transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Controls */}
            <div className="mt-4 flex flex-wrap items-center gap-4">
              {/* Search */}
              <div className="relative flex-1 min-w-64">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-indigo-300" />
                <input
                  type="text"
                  placeholder="Search activities..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white placeholder-indigo-200 focus:outline-none focus:ring-2 focus:ring-white/50"
                />
              </div>

              {/* Date Filter */}
              <select
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-white/50"
              >
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="all">All Time</option>
              </select>

              {/* Type Filter */}
              <select
                value={selectedFilter}
                onChange={(e) => setSelectedFilter(e.target.value)}
                className="px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-white/50"
              >
                <option value="all">All Types</option>
                <option value="navigation">Navigation</option>
                <option value="search">Search</option>
                <option value="automation">Automation</option>
                <option value="report">Reports</option>
                <option value="ai_interaction">AI Interaction</option>
              </select>

              {/* Workspace Filter */}
              <select
                value={selectedWorkspace}
                onChange={(e) => setSelectedWorkspace(e.target.value)}
                className="px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-white/50"
              >
                {workspaces.map(workspace => (
                  <option key={workspace.id} value={workspace.id}>{workspace.name}</option>
                ))}
              </select>

              <button
                onClick={createWorkspace}
                className="px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white hover:bg-white/30 transition-colors"
              >
                + Workspace
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-hidden flex">
            {/* Timeline */}
            <div className="flex-1 overflow-y-auto p-6" ref={timelineRef}>
              {isLoading ? (
                <div className="flex items-center justify-center h-64">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                </div>
              ) : (
                <div className="space-y-6">
                  {filteredData.map((item, index) => {
                    const Icon = getTypeIcon(item.type);
                    const isExpanded = expandedItems.has(item.id);
                    
                    return (
                      <motion.div
                        key={item.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className="relative"
                      >
                        {/* Timeline line */}
                        {index < filteredData.length - 1 && (
                          <div className="absolute left-6 top-12 w-0.5 h-16 bg-gray-200"></div>
                        )}
                        
                        <div className="flex items-start space-x-4">
                          {/* Icon */}
                          <div className={`flex-shrink-0 w-12 h-12 rounded-full ${getTypeColor(item.type)} flex items-center justify-center`}>
                            <Icon className="w-5 h-5" />
                          </div>
                          
                          {/* Content */}
                          <div className="flex-1 bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <div className="flex items-center space-x-2">
                                  <h3 className="font-semibold text-gray-900">{item.title}</h3>
                                  <span className="text-xs text-gray-500">{formatTime(item.timestamp)}</span>
                                  <span className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded-full">
                                    {item.workspace}
                                  </span>
                                </div>
                                <p className="text-gray-600 text-sm mt-1">{item.description}</p>
                                
                                {/* Tags */}
                                <div className="flex flex-wrap gap-1 mt-2">
                                  {item.tags.map(tag => (
                                    <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">
                                      #{tag}
                                    </span>
                                  ))}
                                </div>
                              </div>
                              
                              <div className="flex items-center space-x-2 ml-4">
                                <button
                                  onClick={() => replayAction(item)}
                                  className="p-2 text-gray-500 hover:text-green-600 hover:bg-green-100 rounded transition-colors"
                                  title="Replay Action"
                                >
                                  <Play className="w-4 h-4" />
                                </button>
                                
                                <button
                                  onClick={() => toggleItemExpansion(item.id)}
                                  className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-200 rounded transition-colors"
                                >
                                  {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                                </button>
                              </div>
                            </div>
                            
                            {/* Expanded Details */}
                            <AnimatePresence>
                              {isExpanded && (
                                <motion.div
                                  initial={{ opacity: 0, height: 0 }}
                                  animate={{ opacity: 1, height: 'auto' }}
                                  exit={{ opacity: 0, height: 0 }}
                                  className="mt-4 p-4 bg-white rounded-lg border border-gray-200"
                                >
                                  <div className="grid grid-cols-2 gap-4 text-sm">
                                    {Object.entries(item.details).map(([key, value]) => (
                                      <div key={key}>
                                        <span className="font-medium text-gray-700 capitalize">
                                          {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                                        </span>
                                        <div className="text-gray-600 mt-1">
                                          {Array.isArray(value) ? (
                                            <ul className="list-disc list-inside">
                                              {value.map((item, idx) => (
                                                <li key={idx}>{item}</li>
                                              ))}
                                            </ul>
                                          ) : typeof value === 'boolean' ? (
                                            <span className={value ? 'text-green-600' : 'text-red-600'}>
                                              {value ? 'Yes' : 'No'}
                                            </span>
                                          ) : typeof value === 'number' && key.includes('duration') ? (
                                            formatDuration(value)
                                          ) : (
                                            String(value)
                                          )}
                                        </div>
                                      </div>
                                    ))}
                                  </div>
                                </motion.div>
                              )}
                            </AnimatePresence>
                          </div>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              )}

              {!isLoading && filteredData.length === 0 && (
                <div className="text-center py-16">
                  <Clock className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-600 mb-2">No Activities Found</h3>
                  <p className="text-gray-500">Try adjusting your search filters or date range</p>
                </div>
              )}
            </div>

            {/* Sidebar - Analytics */}
            <div className="w-80 bg-gray-50 border-l border-gray-200 p-6 overflow-y-auto">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2" />
                Activity Analytics
              </h3>
              
              {/* Stats */}
              <div className="space-y-4 mb-6">
                <div className="bg-white p-4 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Total Activities</span>
                    <span className="text-2xl font-bold text-gray-900">{filteredData.length}</span>
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Active Workspaces</span>
                    <span className="text-2xl font-bold text-indigo-600">{workspaces.length - 1}</span>
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Most Active</span>
                    <span className="text-lg font-semibold text-green-600">Research</span>
                  </div>
                </div>
              </div>

              {/* Activity Types */}
              <div className="mb-6">
                <h4 className="font-medium text-gray-800 mb-3">Activity Breakdown</h4>
                <div className="space-y-2">
                  {['navigation', 'search', 'automation', 'report', 'ai_interaction'].map(type => {
                    const count = filteredData.filter(item => item.type === type).length;
                    const percentage = filteredData.length > 0 ? (count / filteredData.length * 100) : 0;
                    
                    return (
                      <div key={type} className="flex items-center justify-between text-sm">
                        <span className="capitalize text-gray-600">{type.replace('_', ' ')}</span>
                        <div className="flex items-center space-x-2">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                          <span className="w-8 text-right text-gray-700">{count}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Quick Actions */}
              <div>
                <h4 className="font-medium text-gray-800 mb-3">Quick Actions</h4>
                <div className="space-y-2">
                  <button className="w-full text-left p-3 bg-white rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex items-center space-x-2">
                      <BookOpen className="w-4 h-4 text-blue-600" />
                      <span className="text-sm">Export Timeline</span>
                    </div>
                  </button>
                  
                  <button className="w-full text-left p-3 bg-white rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex items-center space-x-2">
                      <TrendingUp className="w-4 h-4 text-green-600" />
                      <span className="text-sm">Generate Report</span>
                    </div>
                  </button>
                  
                  <button className="w-full text-left p-3 bg-white rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex items-center space-x-2">
                      <Settings className="w-4 h-4 text-gray-600" />
                      <span className="text-sm">Timeline Settings</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default IntelligentTimeline;