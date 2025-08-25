import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WelcomePage from './components/WelcomePage';
import BrowserInterface from './components/BrowserInterface';
import EnhancedBrowserInterface from './components/EnhancedBrowserInterface';
import { SessionProvider } from './contexts/SessionContext';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('welcome');
  const [useEnhancedUI, setUseEnhancedUI] = useState(true); // New enhanced UI by default

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
                useEnhancedUI ? 
                <EnhancedBrowserInterface onBackToWelcome={() => setCurrentView('welcome')} /> :
                <BrowserInterface onBackToWelcome={() => setCurrentView('welcome')} />
              } 
            />
            <Route 
              path="/browser" 
              element={
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