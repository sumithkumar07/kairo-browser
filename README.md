# 🌐 Kairo AI Browser

A revolutionary AI-powered browser with enhanced proxy capabilities and intelligent web automation.

## ✨ Features

- **🤖 AI Assistant Integration**: Natural language web navigation and automation
- **🚀 Enhanced Browser Engine**: Advanced proxy system with smart routing
- **🛡️ Anti-Detection Technology**: Bypass restrictions and access all websites
- **⚡ Real-time Content Loading**: Display actual website content within iframe
- **🔄 Smart Proxy Routing**: Automatic selection between HTTP proxy and browser engine
- **📱 Responsive Design**: Works seamlessly across all devices

## 🏗️ Architecture

### Backend (FastAPI)
- **AI Processing**: Groq integration for natural language understanding
- **Browser Automation**: Playwright-powered browser engine
- **Enhanced Proxy System**: Multi-method content loading with anti-detection
- **Database**: MongoDB for session and interaction storage

### Frontend (React)
- **Modern UI**: Built with Tailwind CSS and Framer Motion
- **AI Chat Interface**: Real-time communication with AI assistant
- **Browser Controls**: Full navigation and tab management
- **Session Management**: Persistent browsing sessions

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   # Backend
   cd backend && pip install -r requirements.txt
   
   # Frontend  
   cd frontend && yarn install
   ```

2. **Setup Environment**:
   - Backend: Configure `MONGO_URL` and `GROQ_API_KEY` in `.env`
   - Frontend: Set `REACT_APP_BACKEND_URL` in `.env`

3. **Start Services**:
   ```bash
   # Start all services
   sudo supervisorctl restart all
   ```

4. **Access Application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8001`

## 🎯 Usage

1. **Open the application** at `http://localhost:3000`
2. **Click "Start Browsing"** to enter the browser interface
3. **Open AI Assistant** (green button bottom-right)
4. **Try commands like**:
   - "Open YouTube"
   - "Search for AI news" 
   - "Navigate to Google"

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `POST /api/ai/query` - Process AI queries
- `POST /api/browser/execute` - Execute browser commands
- `POST /api/proxy/enhanced` - Enhanced proxy with smart routing
- `POST /api/proxy/browser` - Browser engine proxy
- `POST /api/proxy` - Basic HTTP proxy

## 🧪 Testing

The application includes comprehensive testing for all components:
- ✅ 13/13 backend test suites passing
- ✅ Complete integration testing verified
- ✅ Real content loading confirmed

## 📝 License

MIT License - see LICENSE file for details.