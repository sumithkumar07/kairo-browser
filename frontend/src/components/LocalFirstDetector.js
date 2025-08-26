import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Monitor, 
  Zap, 
  Shield, 
  Wifi, 
  CheckCircle, 
  XCircle,
  Loader2
} from 'lucide-react';

const LocalFirstDetector = () => {
  const [electronInfo, setElectronInfo] = useState(null);
  const [isLocalFirst, setIsLocalFirst] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const detectEnvironment = async () => {
      setLoading(true);
      
      // Check if we're running in Electron
      if (window.electronAPI) {
        try {
          const appInfo = await window.electronAPI.getAppInfo();
          setElectronInfo(appInfo);
          setIsLocalFirst(appInfo.isLocalFirst);
        } catch (error) {
          console.error('Failed to get app info:', error);
        }
      } else {
        // We're running in regular browser (server-first mode)
        setIsLocalFirst(false);
      }
      
      setLoading(false);
    };

    detectEnvironment();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        <span className="ml-3 text-gray-600">Detecting environment...</span>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6 mb-6"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
          <Monitor className="w-5 h-5 text-blue-600" />
          <span>Architecture Detection</span>
        </h3>
        
        {isLocalFirst ? (
          <div className="flex items-center space-x-2 bg-green-100 text-green-800 px-3 py-1 rounded-full">
            <CheckCircle className="w-4 h-4" />
            <span className="text-sm font-medium">Local-First</span>
          </div>
        ) : (
          <div className="flex items-center space-x-2 bg-orange-100 text-orange-800 px-3 py-1 rounded-full">
            <XCircle className="w-4 h-4" />
            <span className="text-sm font-medium">Server-First</span>
          </div>
        )}
      </div>

      {isLocalFirst && electronInfo ? (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <div className="flex items-center space-x-2 mb-2">
                <Zap className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-800">Local Runtime</span>
              </div>
              <p className="text-xs text-green-700">
                All processing happens on your machine
              </p>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <div className="flex items-center space-x-2 mb-2">
                <Wifi className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">Direct Internet</span>
              </div>
              <p className="text-xs text-blue-700">
                No proxy restrictions - full website access
              </p>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-gray-700 mb-2">System Information:</h4>
            <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
              <div>App: {electronInfo.appName}</div>
              <div>Version: {electronInfo.version}</div>
              <div>Platform: {electronInfo.platform}</div>
              <div>Architecture: {electronInfo.arch}</div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg border border-green-200">
            <div className="flex items-center space-x-2 mb-2">
              <Shield className="w-4 h-4 text-green-600" />
              <span className="text-sm font-medium text-green-800">Local-First Benefits Active</span>
            </div>
            <ul className="text-xs text-green-700 space-y-1">
              <li>✅ Direct YouTube access (no restrictions)</li>
              <li>✅ Faster performance (no server bottleneck)</li>
              <li>✅ Better privacy (data stays local)</li>
              <li>✅ Full website functionality</li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
            <div className="flex items-center space-x-2 mb-2">
              <XCircle className="w-4 h-4 text-orange-600" />
              <span className="text-sm font-medium text-orange-800">Running in Browser (Server-First)</span>
            </div>
            <p className="text-xs text-orange-700 mb-3">
              You're currently using the web version. For full local-first benefits, use the desktop app.
            </p>
            
            <div className="bg-white p-3 rounded border border-orange-200">
              <h5 className="text-xs font-medium text-gray-700 mb-2">Current Limitations:</h5>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>⚠️ Some websites may have restrictions</li>
                <li>⚠️ Slower performance through proxy</li>
                <li>⚠️ Limited offline capabilities</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default LocalFirstDetector;