import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WelcomePage from './components/WelcomePage';
import BrowserInterface from './components/BrowserInterface';
import EnhancedBrowserInterface from './components/EnhancedBrowserInterface';
import UltimateEnhancedBrowserInterface from './components/UltimateEnhancedBrowserInterface';
import { SessionProvider } from './contexts/SessionContext';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('welcome');
  const [useUltimateUI, setUseUltimateUI] = useState(true); // Ultimate enhanced UI by default
  const [useEnhancedUI, setUseEnhancedUI] = useState(true); // Fallback to enhanced UI

  return (
    <SessionProvider>
      <Router>
        <div className="App min-h-screen bg-gray-50">
          <Routes>
            <Route 
              path="/" 
              element={
                currentView === 'welcome' ? 
                <WelcomePage onStartBrowsing={() => setCurrentView('browser')} /> :
                useUltimateUI ? 
                <UltimateEnhancedBrowserInterface onBackToWelcome={() => setCurrentView('welcome')} /> :
                useEnhancedUI ? 
                <EnhancedBrowserInterface onBackToWelcome={() => setCurrentView('welcome')} /> :
                <BrowserInterface onBackToWelcome={() => setCurrentView('welcome')} />
              } 
            />
            <Route 
              path="/browser" 
              element={
                useUltimateUI ? 
                <UltimateEnhancedBrowserInterface onBackToWelcome={() => setCurrentView('welcome')} /> :
                useEnhancedUI ? 
                <EnhancedBrowserInterface onBackToWelcome={() => setCurrentView('welcome')} /> :
                <BrowserInterface onBackToWelcome={() => setCurrentView('welcome')} />
              } 
            />
          </Routes>
        </div>
      </Router>
    </SessionProvider>
  );
}

export default App;