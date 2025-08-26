import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Monitor, 
  Zap, 
  Shield, 
  Wifi, 
  CheckCircle, 
  XCircle,
  Loader2,
  Trash2,
  Archive,
  Download
} from 'lucide-react';

const LocalFirstDetector = () => {
  const [electronInfo, setElectronInfo] = useState(null);
  const [isLocalFirst, setIsLocalFirst] = useState(false);
  const [loading, setLoading] = useState(true);
  const [migrationStatus, setMigrationStatus] = useState(null);

  useEffect(() => {
    const detectEnvironment = async () => {
      setLoading(true);
      
      // Check migration status
      const serverBackendExists = await checkServerBackendExists();
      
      // Check if we're running in Electron
      if (window.kairoAPI) {
        try {
          const appInfo = await window.kairoAPI.system.getInfo();
          setElectronInfo(appInfo.system);
          setIsLocalFirst(true);
          setMigrationStatus({
            phase: serverBackendExists ? 'hybrid' : 'complete',
            serverRemoved: !serverBackendExists
          });
        } catch (error) {
          console.error('Failed to get app info:', error);
        }
      } else {
        // We're running in regular browser (server-first mode)
        setIsLocalFirst(false);
        setMigrationStatus({
          phase: serverBackendExists ? 'server-first' : 'migration-needed',
          serverRemoved: !serverBackendExists
        });
      }
      
      setLoading(false);
    };

    detectEnvironment();
  }, []);

  const checkServerBackendExists = async () => {
    try {
      const response = await fetch('/api/health');
      return response.ok;
    } catch (error) {
      return false;
    }
  };

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
          <span>Architecture Status</span>
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

      {/* Migration Status Banner */}
      {migrationStatus && (
        <div className="mb-4">
          {migrationStatus.phase === 'complete' && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="text-sm font-semibold text-green-800">Migration Complete!</span>
              </div>
              <p className="text-xs text-green-700">
                ✨ Successfully migrated to pure local-first architecture. Server components removed.
              </p>
            </div>
          )}
          
          {migrationStatus.phase === 'hybrid' && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <Archive className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-semibold text-blue-800">Hybrid Mode Active</span>
              </div>
              <p className="text-xs text-blue-700">
                🔄 Both architectures available. Server components preserved for comparison.
              </p>
            </div>
          )}

          {migrationStatus.serverRemoved && (
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 mt-3">
              <div className="flex items-center space-x-2 mb-1">
                <Trash2 className="w-4 h-4 text-purple-600" />
                <span className="text-xs font-medium text-purple-800">Server Components Removed</span>
              </div>
              <p className="text-xs text-purple-700">
                📦 Backend archived to /app/archive/server-first-backup/
              </p>
            </div>
          )}
        </div>
      )}

      {isLocalFirst && electronInfo ? (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <div className="flex items-center space-x-2 mb-2">
                <Zap className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-800">Native Runtime</span>
              </div>
              <p className="text-xs text-green-700">
                Desktop app with embedded Chromium engine
              </p>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <div className="flex items-center space-x-2 mb-2">
                <Wifi className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">Direct Internet</span>
              </div>
              <p className="text-xs text-blue-700">
                No proxy - full website access
              </p>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-gray-700 mb-2">System Information:</h4>
            <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
              <div>Platform: {electronInfo.platform}</div>
              <div>Version: {electronInfo.version}</div>
              <div>Electron: {electronInfo.electron}</div>
              <div>Chrome: {electronInfo.chrome}</div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg border border-green-200">
            <div className="flex items-center space-x-2 mb-2">
              <Shield className="w-4 h-4 text-green-600" />
              <span className="text-sm font-medium text-green-800">Local-First Benefits Active</span>
            </div>
            <ul className="text-xs text-green-700 space-y-1">
              <li>✅ Native YouTube/Netflix access</li>
              <li>✅ Maximum performance (no server bottleneck)</li>
              <li>✅ Complete privacy (data stays local)</li>
              <li>✅ Offline operation capability</li>
              <li>✅ Direct file system access</li>
              <li>✅ System integration features</li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
            <div className="flex items-center space-x-2 mb-2">
              <XCircle className="w-4 h-4 text-orange-600" />
              <span className="text-sm font-medium text-orange-800">Running in Browser</span>
            </div>
            <p className="text-xs text-orange-700 mb-3">
              {migrationStatus?.serverRemoved 
                ? 'Server components removed. For full functionality, use the desktop app.'
                : 'You\'re using the web version. For local-first benefits, use the desktop app.'
              }
            </p>
            
            <div className="bg-white p-3 rounded border border-orange-200">
              <h5 className="text-xs font-medium text-gray-700 mb-2">Current Limitations:</h5>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>⚠️ {migrationStatus?.serverRemoved ? 'Limited functionality (no backend)' : 'Some websites may have restrictions'}</li>
                <li>⚠️ {migrationStatus?.serverRemoved ? 'No AI processing available' : 'Slower performance through proxy'}</li>
                <li>⚠️ No offline capabilities</li>
              </ul>
            </div>

            {!migrationStatus?.serverRemoved && (
              <div className="mt-3 bg-blue-50 p-3 rounded border border-blue-200">
                <div className="flex items-center space-x-2 mb-1">
                  <Download className="w-4 h-4 text-blue-600" />
                  <span className="text-xs font-medium text-blue-800">Get Desktop App</span>
                </div>
                <p className="text-xs text-blue-700">
                  Download the desktop version for full local-first architecture benefits.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default LocalFirstDetector;