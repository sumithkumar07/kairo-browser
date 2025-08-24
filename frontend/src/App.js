import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WelcomePage from './components/WelcomePage';
import BrowserInterface from './components/BrowserInterface';
import { SessionProvider } from './contexts/SessionContext';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('welcome');

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
                <BrowserInterface onBackToWelcome={() => setCurrentView('welcome')} />
              } 
            />
            <Route 
              path="/browser" 
              element={<BrowserInterface onBackToWelcome={() => setCurrentView('welcome')} />} 
            />
          </Routes>
        </div>
      </Router>
    </SessionProvider>
  );
}

export default App;