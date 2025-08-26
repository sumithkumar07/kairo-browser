# 🗑️ COMPONENTS TO REMOVE FOR LOCAL-FIRST MIGRATION

## 🚫 COMPLETE REMOVAL LIST

### **Backend Directory - REMOVE ENTIRELY**
```
❌ /app/backend/
├── ❌ server.py                 # FastAPI server (2,500+ lines)
├── ❌ requirements.txt          # Python dependencies
└── ❌ .env                      # Server environment variables
```

**Reason:** All server-side processing moves to local machine

---

### **Specific Backend Components to Remove**

#### 1. **FastAPI Server Infrastructure**
```python
❌ app = FastAPI()                # Main server app
❌ CORSMiddleware                 # No longer needed - local access
❌ MongoDB client/connections     # Replace with local SQLite
❌ All @app.post() endpoints      # Replace with IPC handlers
```

#### 2. **Proxy System (Lines 531-1400+ in server.py)**
```python
❌ @app.post("/api/proxy")                    # Basic proxy
❌ @app.post("/api/proxy/enhanced")           # Enhanced proxy  
❌ @app.post("/api/proxy/browser")            # Browser proxy
❌ async def proxy_with_browser()             # Playwright proxy
❌ async def enhanced_http_proxy()            # HTTP proxy
❌ async def proxy_request_internal()         # Internal proxy
```
**Reason:** Direct browser access - no proxy needed

#### 3. **Server-side Browser Automation**
```python
❌ from playwright.async_api import async_playwright
❌ async def execute_workflow_background()
❌ async def execute_workflow_step()
❌ All Playwright browser launching code
❌ Browser context creation and management
```
**Reason:** Local browser engine handles this

#### 4. **Server API Endpoints - ALL**
```python
❌ @app.get("/api/health")
❌ @app.post("/api/ai/query") 
❌ @app.post("/api/ai/multimodal-query")
❌ @app.post("/api/browser/execute")
❌ @app.post("/api/workflow/execute")
❌ @app.get("/api/workflow/{workflow_id}")
❌ @app.get("/api/sessions")
❌ @app.post("/api/navigate")
❌ @app.post("/api/ultimate/proxy")
❌ @app.post("/api/system/analytics")
❌ @app.post("/api/stealth/test/{domain}")
❌ @app.post("/api/interaction/execute")
```
**Reason:** Replace with Electron IPC handlers

#### 5. **MongoDB Dependencies**
```python
❌ from pymongo import MongoClient
❌ client = MongoClient(MONGO_URL)
❌ db = client.kairo_browser
❌ All db.collection.insert_one() calls
❌ All database aggregation queries
```
**Reason:** Replace with local SQLite database

#### 6. **Server-side HTTP Client**
```python
❌ import httpx
❌ async with httpx.AsyncClient() as client:
❌ All external HTTP requests from server
❌ Custom headers and proxy logic
```
**Reason:** Direct browser navigation

---

### **Frontend Components to MODIFY (Not Remove)**

#### 1. **API Calls - REPLACE with IPC**
```javascript
// ❌ REMOVE these patterns:
fetch(`${backendUrl}/api/ai/query`, {...})
fetch(`${backendUrl}/api/browser/execute`, {...})
fetch(`${backendUrl}/api/proxy`, {...})

// ✅ REPLACE with:
window.electronAPI.processAIQuery(...)
window.electronAPI.executeBrowserCommand(...)
window.electronAPI.navigateToUrl(...)
```

#### 2. **Session Context - MODIFY**
```javascript
❌ REMOVE: axios calls to backend
❌ REMOVE: HTTP error handling
❌ REMOVE: API_BASE URL configuration

✅ KEEP: Session state management
✅ KEEP: Local storage concepts
✅ MODIFY: Replace HTTP with IPC calls
```

---

### **Configuration Files to Update**

#### 1. **package.json Changes**
```json
❌ REMOVE: "proxy": "http://localhost:8001"
❌ REMOVE: Backend-related scripts

✅ ADD: Electron dependencies
✅ ADD: Electron build scripts
```

#### 2. **Environment Variables**
```javascript
❌ REMOVE: REACT_APP_BACKEND_URL (no backend server)
❌ REMOVE: Server port configurations

✅ KEEP: GROQ_API_KEY (for local AI processing)
✅ ADD: Local app configuration
```

---

### **Dependencies to Remove**

#### 1. **Backend Python Dependencies**
```txt
❌ fastapi
❌ uvicorn
❌ pymongo  
❌ playwright
❌ httpx
❌ beautifulsoup4
❌ python-multipart
```

#### 2. **Frontend Dependencies - Some Removals**
```json
❌ "axios": "^1.6.0"     # Replace with Electron IPC
✅ KEEP: All React dependencies
✅ KEEP: UI libraries (framer-motion, lucide-react)
```

---

### **Build/Deployment Files to Remove**

```
❌ Backend supervisord configuration
❌ Backend server startup scripts
❌ Backend environment setup
❌ Any Docker/container configurations for backend
❌ Backend testing files
```

---

## 📊 REMOVAL IMPACT SUMMARY

### **Files to Delete Completely:**
- 🗑️ `/app/backend/` (entire directory)
- 🗑️ Any backend-related configuration files
- 🗑️ Server deployment scripts

### **Files to Heavily Modify:**
- 🔄 `/app/frontend/src/contexts/SessionContext.js` → Replace with local IPC
- 🔄 `/app/frontend/src/components/*.js` → Replace API calls with IPC
- 🔄 `/app/package.json` → Add Electron, remove proxy

### **Files to Keep Unchanged:**
- ✅ All UI components (visual design)
- ✅ React component structure  
- ✅ CSS/styling files
- ✅ Static assets

---

## 🎯 WHAT STAYS vs WHAT GOES

### **✅ KEEP (Transform to Local)**
```
React UI Components     → Wrap in Electron
Browser Interface      → Keep design, change backend
AI Chat Functionality  → Direct API calls instead of server
Tab Management         → Keep UI, local browser engine
Session Management     → Local SQLite instead of MongoDB
Bookmarks System       → Local storage
```

### **❌ REMOVE (Server Dependencies)**
```
FastAPI Backend        → Replace with Electron main process  
Proxy System          → Direct browser navigation
MongoDB               → SQLite local database
Server API Endpoints  → IPC handlers
CORS/HTTP Middleware  → Not needed for local app
Server-side Playwright → Local browser engine
```

This removal strategy eliminates ~3,000+ lines of server code and transforms the app into a true local-first architecture!