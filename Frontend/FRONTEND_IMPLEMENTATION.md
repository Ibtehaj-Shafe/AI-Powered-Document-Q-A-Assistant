# Frontend Implementation Guide

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Concepts](#core-concepts)
4. [File-by-File Breakdown](#file-by-file-breakdown)
5. [Data Flow](#data-flow)
6. [Authentication Flow](#authentication-flow)
7. [Component Relationships](#component-relationships)
8. [API Integration](#api-integration)
9. [State Management](#state-management)
10. [Routing Logic](#routing-logic)

---

## 🏗️ Architecture Overview

The frontend is built using **React 18** with **TypeScript** and **Vite** as the build tool. The architecture follows a **component-based, service-oriented** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         React Application                │
├─────────────────────────────────────────┤
│  Pages (UI Components)                    │
│  ├── Authentication Pages                │
│  ├── Dashboard (Main App)                │
│  └── Admin Dashboard                    │
├─────────────────────────────────────────┤
│  Contexts (State Management)             │
│  └── AuthContext (Global Auth State)     │
├─────────────────────────────────────────┤
│  Services (API Layer)                    │
│  ├── api.ts (Axios Instance)            │
│  ├── authService.ts                     │
│  ├── documentService.ts                 │
│  ├── askService.ts                      │
│  └── adminService.ts                    │
├─────────────────────────────────────────┤
│  Components (Reusable)                  │
│  └── ProtectedRoute                    │
├─────────────────────────────────────────┤
│  Utils (Helpers)                        │
│  └── jwt.ts (Token Decoding)            │
└─────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Frontend/
├── public/                    # Static assets
├── src/
│   ├── components/           # Reusable components
│   │   └── ProtectedRoute.tsx
│   ├── contexts/             # React Context providers
│   │   └── AuthContext.tsx
│   ├── pages/               # Page components
│   │   ├── Login.tsx
│   │   ├── Signup.tsx
│   │   ├── ForgotPassword.tsx
│   │   ├── ResetPassword.tsx
│   │   ├── Dashboard.tsx
│   │   ├── AdminDashboard.tsx
│   │   ├── Auth.css
│   │   ├── Dashboard.css
│   │   └── AdminDashboard.css
│   ├── services/            # API service layer
│   │   ├── api.ts
│   │   ├── authService.ts
│   │   ├── documentService.ts
│   │   ├── askService.ts
│   │   └── adminService.ts
│   ├── utils/               # Utility functions
│   │   └── jwt.ts
│   ├── App.tsx              # Main app component
│   ├── App.css
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles
├── index.html
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript configuration
├── package.json
└── README.md
```

---

## 🧠 Core Concepts

### 1. **Service Layer Pattern**
All API calls are abstracted into service modules. This provides:
- Single source of truth for API endpoints
- Type safety with TypeScript interfaces
- Easy error handling
- Reusability across components

### 2. **Context API for State Management**
- `AuthContext` manages global authentication state
- Provides user data, login/logout functions
- Eliminates prop drilling
- Centralized auth logic

### 3. **Protected Routes**
- `ProtectedRoute` component wraps sensitive pages
- Checks authentication status
- Handles role-based access (user/admin)
- Redirects unauthenticated users

### 4. **JWT Token Management**
- Tokens stored in `localStorage`
- Automatic token refresh on 401 errors
- Token expiration checking
- Secure token decoding (frontend only)

### 5. **Vite Proxy for CORS**
- All API calls go through `/api` proxy
- Vite forwards to `http://localhost:8000`
- Avoids CORS issues without backend changes

---

## 📄 File-by-File Breakdown

### **Entry Point Files**

#### `main.tsx`
**Purpose:** Application entry point that renders the React app.

**Key Logic:**
- Creates React root
- Wraps app in `BrowserRouter` for routing
- Renders `App` component
- Applies global styles

**Code Flow:**
```typescript
ReactDOM.createRoot(document.getElementById('root')!)
  .render(
    <React.StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </React.StrictMode>
  )
```

#### `index.html`
**Purpose:** HTML template that serves as the container for the React app.

**Key Elements:**
- Root `<div id="root">` where React mounts
- Script tag loading `main.tsx`
- Meta tags for responsive design

---

### **Core Application Files**

#### `App.tsx`
**Purpose:** Main application component that sets up routing.

**Key Logic:**
- Wraps entire app in `AuthProvider` for global auth state
- Defines all routes using React Router
- Uses `ProtectedRoute` for authenticated pages
- Handles navigation and route protection

**Route Structure:**
```typescript
- /login → Login page (public)
- /signup → Signup page (public)
- /forgot-password → Forgot password (public)
- /reset-password → Reset password (public)
- /dashboard → Main app (protected)
- /admin → Admin dashboard (protected, admin only)
- / → Redirects to /dashboard
```

**Component Relationships:**
- Imports `AuthProvider` from `contexts/AuthContext.tsx`
- Imports `ProtectedRoute` from `components/ProtectedRoute.tsx`
- Imports all page components from `pages/`

---

### **Context Files**

#### `contexts/AuthContext.tsx`
**Purpose:** Global authentication state management.

**Key Logic:**

1. **State Management:**
   - `user`: Current user object (id, name, email, role)
   - `loading`: Initialization loading state
   - `isAuthenticated`: Computed from user and token presence
   - `isAdmin`: Computed from user role

2. **Initialization (`useEffect`):**
   - Checks for existing access token in localStorage
   - Validates token expiration
   - Decodes JWT to extract user info
   - Sets user state if token is valid

3. **Login Function:**
   - Calls `authService.login()`
   - Stores tokens in localStorage
   - Decodes JWT to get user info
   - Updates user state

4. **Signup Function:**
   - Calls `authService.signup()`
   - Automatically logs in after signup
   - Stores tokens
   - Sets user state from signup response

5. **Logout Function:**
   - Clears tokens from localStorage
   - Resets user state to null

**Dependencies:**
- `services/authService.ts` - For API calls
- `utils/jwt.ts` - For token decoding

**Exports:**
- `AuthProvider` - Context provider component
- `useAuth` - Hook to access auth context

---

### **Service Layer Files**

#### `services/api.ts`
**Purpose:** Axios instance with interceptors for all API calls.

**Key Logic:**

1. **Base Configuration:**
   - Base URL: `/api` (uses Vite proxy)
   - Default headers: `Content-Type: application/json`

2. **Request Interceptor:**
   - Runs before every API request
   - Retrieves access token from localStorage
   - Adds `Authorization: Bearer <token>` header
   - Ensures all authenticated requests include token

3. **Response Interceptor:**
   - Handles 401 (Unauthorized) errors
   - Attempts automatic token refresh
   - Retries original request with new token
   - Redirects to login if refresh fails

**Code Flow:**
```
Request → Add Token Header → Backend
Response ← Check Status ← Backend
  ├─ 200-299: Return response
  ├─ 401: Try refresh token
  │   ├─ Success: Retry request
  │   └─ Fail: Redirect to login
  └─ Other: Return error
```

**Dependencies:**
- `axios` - HTTP client library

---

#### `services/authService.ts`
**Purpose:** Authentication-related API calls.

**Exported Interfaces:**
- `UserCreate` - Signup data structure
- `UserLogin` - Login credentials
- `TokenResponse` - JWT tokens response
- `UserResponse` - User data structure

**Functions:**

1. **`signup(userData)`**
   - POST to `/auth/signup`
   - Returns `UserResponse`
   - Creates new user account

2. **`login(credentials)`**
   - POST to `/auth/login`
   - Returns `TokenResponse` (access_token, refresh_token)
   - Authenticates user

3. **`forgotPassword(email)`**
   - POST to `/auth/forgot-password`
   - Sends OTP to email
   - Returns success message

4. **`resetPassword(email, otp, newPassword)`**
   - POST to `/auth/reset-password`
   - Resets password with OTP
   - Returns success message

5. **`refreshToken(refreshToken)`**
   - POST to `/auth/refresh`
   - Gets new access token
   - Returns new `TokenResponse`

**Dependencies:**
- `services/api.ts` - Axios instance

---

#### `services/documentService.ts`
**Purpose:** Document upload API calls.

**Exported Interfaces:**
- `DocumentResponse` - Uploaded document metadata

**Functions:**

1. **`uploadFile(file)`**
   - POST to `/upload/` with FormData
   - Content-Type: `multipart/form-data`
   - Returns document metadata
   - Requires authentication

**Dependencies:**
- `services/api.ts` - Axios instance

---

#### `services/askService.ts`
**Purpose:** Question-answer API calls.

**Exported Interfaces:**
- `AskRequest` - Question payload
- `AskResponse` - Answer response

**Functions:**

1. **`askQuestion(query)`**
   - POST to `/ask/` with query
   - Returns AI-generated answer
   - Requires authentication
   - Uses user's uploaded documents

**Dependencies:**
- `services/api.ts` - Axios instance

---

#### `services/adminService.ts`
**Purpose:** Admin dashboard API calls.

**Exported Interfaces:**
- `UserStat` - Individual user statistics
- `AdminDashboardResponse` - Complete dashboard data

**Functions:**

1. **`getDashboard()`**
   - GET to `/admin/dashboard`
   - Returns statistics and user stats
   - Requires admin role
   - Includes: total_users, total_files, total_questions, user_stats array

**Dependencies:**
- `services/api.ts` - Axios instance

---

### **Component Files**

#### `components/ProtectedRoute.tsx`
**Purpose:** Route protection wrapper component.

**Key Logic:**

1. **Props:**
   - `children`: Component to render if authorized
   - `requireAdmin`: Boolean for admin-only routes

2. **Protection Logic:**
   ```
   Check loading state
     ├─ Loading: Show loading indicator
     ├─ Not authenticated: Redirect to /login
     ├─ Admin required but not admin: Redirect to /dashboard
     └─ Authorized: Render children
   ```

3. **Uses:**
   - `useAuth()` hook to get auth state
   - `Navigate` component for redirects

**Dependencies:**
- `contexts/AuthContext.tsx` - For auth state
- `react-router-dom` - For navigation

**Usage:**
```typescript
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>

<ProtectedRoute requireAdmin={true}>
  <AdminDashboard />
</ProtectedRoute>
```

---

### **Page Components**

#### `pages/Login.tsx`
**Purpose:** User login page.

**State Management:**
- `email`: User email input
- `password`: User password input
- `error`: Error message display
- `loading`: Loading state during login

**Key Logic:**

1. **Form Submission:**
   - Validates inputs
   - Calls `login()` from `useAuth()`
   - Handles errors
   - Redirects to dashboard on success

2. **Navigation:**
   - Link to `/signup`
   - Link to `/forgot-password`

**Dependencies:**
- `contexts/AuthContext.tsx` - For login function
- `react-router-dom` - For navigation
- `pages/Auth.css` - Styling

---

#### `pages/Signup.tsx`
**Purpose:** User registration page.

**State Management:**
- `name`: User name input
- `email`: User email input
- `password`: Password input
- `confirmPassword`: Password confirmation
- `error`: Validation/API errors
- `loading`: Loading state

**Key Logic:**

1. **Validation:**
   - Password match check
   - Minimum password length (6 characters)
   - Email format (handled by input type)

2. **Form Submission:**
   - Calls `signup()` from `useAuth()`
   - Automatically logs in after signup
   - Redirects to dashboard

**Dependencies:**
- `contexts/AuthContext.tsx` - For signup function
- `react-router-dom` - For navigation
- `pages/Auth.css` - Styling

---

#### `pages/ForgotPassword.tsx`
**Purpose:** Password reset request page.

**State Management:**
- `email`: User email input
- `error`: Error message
- `loading`: Loading state

**Key Logic:**

1. **Form Submission:**
   - Calls `authService.forgotPassword()`
   - **Automatically navigates to `/reset-password?email=<email>` after OTP is sent successfully**
   - Passes email as URL parameter for seamless flow
   - Handles errors if OTP sending fails

2. **User Flow:**
   - User enters email
   - Clicks "Send OTP"
   - Backend verifies email exists in database
   - OTP is sent to email
   - User is automatically redirected to reset password page

**Dependencies:**
- `services/authService.ts` - For API call
- `react-router-dom` - For navigation (useNavigate)
- `pages/Auth.css` - Styling

---

#### `pages/ResetPassword.tsx`
**Purpose:** Password reset with OTP page.

**State Management:**
- `email`: User email (pre-filled from URL params if coming from forgot password)
- `otp`: OTP code input
- `newPassword`: New password input
- `confirmPassword`: Password confirmation
- `error`: Validation/API errors
- `message`: Success message
- `loading`: Loading state

**Key Logic:**

1. **Email Handling:**
   - Reads email from URL search params (`?email=<email>`)
   - If email exists in URL: Shows as read-only field (pre-filled)
   - If no email in URL: Allows manual email entry
   - Ensures email is always available for password reset

2. **Validation:**
   - Password match check
   - Minimum password length (6 characters)

3. **Form Submission:**
   - Calls `authService.resetPassword(email, otp, newPassword)`
   - Shows success message
   - Redirects to login after 2 seconds

4. **Complete Password Reset Flow:**
   ```
   Forgot Password Page
     ↓ (User enters email)
   OTP Sent to Email
     ↓ (Automatic navigation)
   Reset Password Page
     ↓ (User enters OTP + new password)
   Password Reset Success
     ↓ (Automatic redirect)
   Login Page
   ```

**Dependencies:**
- `services/authService.ts` - For API call
- `react-router-dom` - For navigation and URL params (useSearchParams, useNavigate)
- `pages/Auth.css` - Styling

---

#### `pages/Dashboard.tsx`
**Purpose:** Main application page for document upload and Q&A.

**State Management:**
- `file`: Selected file for upload
- `uploading`: Upload progress state
- `uploadMessage`: Success message
- `query`: Question input
- `answer`: AI-generated answer
- `asking`: Question processing state
- `error`: Error messages

**Key Logic:**

1. **File Upload:**
   - File selection handler validates PDF/DOCX
   - Form submission calls `documentService.uploadFile()`
   - Shows success/error messages
   - Resets file input on success

2. **Question & Answer:**
   - Form submission calls `askService.askQuestion()`
   - Displays answer in formatted container
   - Handles loading states
   - Shows error messages

3. **Navigation:**
   - Logout button calls `logout()` from `useAuth()`
   - Admin dashboard link (if admin)
   - User name display

**Dependencies:**
- `contexts/AuthContext.tsx` - For user data and logout
- `services/documentService.ts` - For file upload
- `services/askService.ts` - For questions
- `react-router-dom` - For navigation
- `pages/Dashboard.css` - Styling

---

#### `pages/AdminDashboard.tsx`
**Purpose:** Admin-only dashboard with statistics.

**State Management:**
- `data`: Dashboard statistics data
- `loading`: Data fetching state
- `error`: Error message

**Key Logic:**

1. **Data Fetching (`useEffect`):**
   - Calls `adminService.getDashboard()` on mount
   - Updates state with response
   - Handles errors

2. **Display:**
   - Statistics cards (total users, files, questions)
   - User statistics table
   - Loading and error states

3. **Navigation:**
   - Back to dashboard button
   - Logout button

**Dependencies:**
- `contexts/AuthContext.tsx` - For logout function
- `services/adminService.ts` - For API call
- `react-router-dom` - For navigation
- `pages/AdminDashboard.css` - Styling

---

### **Utility Files**

#### `utils/jwt.ts`
**Purpose:** JWT token decoding utilities.

**Key Functions:**

1. **`decodeJWT(token)`**
   - Decodes JWT payload (frontend only, no verification)
   - Returns payload object with user_id, role, exp, etc.
   - Handles base64 decoding
   - Returns null on error

2. **`isTokenExpired(token)`**
   - Checks token expiration
   - Uses 5-second buffer for safety
   - Returns boolean

**Usage:**
- Used in `AuthContext` to extract user info from tokens
- Used to check token validity before making requests

**Note:** This is frontend-only decoding. Token verification is done by the backend.

---

### **Configuration Files**

#### `vite.config.ts`
**Purpose:** Vite build tool configuration.

**Key Settings:**
- React plugin enabled
- Development server on port 3000
- Proxy configuration:
  - `/api/*` → `http://localhost:8000/*`
  - Handles CORS by proxying requests

**Why Proxy?**
- Backend doesn't have CORS configured
- Proxy makes requests appear same-origin
- No backend modifications needed

---

#### `tsconfig.json`
**Purpose:** TypeScript compiler configuration.

**Key Settings:**
- Strict mode enabled
- JSX: `react-jsx`
- Module: ESNext
- Target: ES2022
- `verbatimModuleSyntax`: Requires type-only imports for types

---

## 🔄 Data Flow

### **Authentication Flow**

```
User enters credentials
    ↓
Login.tsx calls useAuth().login()
    ↓
AuthContext.login() calls authService.login()
    ↓
api.ts adds token to request header
    ↓
Backend validates and returns tokens
    ↓
Tokens stored in localStorage
    ↓
JWT decoded to extract user info
    ↓
User state updated in AuthContext
    ↓
ProtectedRoute checks isAuthenticated
    ↓
User redirected to /dashboard
```

### **Document Upload Flow**

```
User selects file
    ↓
Dashboard.tsx validates file type
    ↓
Form submission calls documentService.uploadFile()
    ↓
api.ts adds Authorization header
    ↓
Backend processes file (extracts text, chunks, embeds)
    ↓
Response with document metadata
    ↓
Success message displayed
```

### **Question & Answer Flow**

```
User enters question
    ↓
Dashboard.tsx calls askService.askQuestion()
    ↓
api.ts adds Authorization header
    ↓
Backend:
  - Embeds question
  - Searches Pinecone (user's documents)
  - Builds context
  - Calls Groq LLM
  - Returns answer
    ↓
Answer displayed in UI
```

### **Admin Dashboard Flow**

```
Admin navigates to /admin
    ↓
ProtectedRoute checks isAdmin
    ↓
AdminDashboard.tsx mounts
    ↓
useEffect calls adminService.getDashboard()
    ↓
api.ts adds Authorization header
    ↓
Backend:
  - Validates admin role
  - Queries database for stats
  - Returns aggregated data
    ↓
Statistics displayed in cards and table
```

### **Password Reset Flow**

```
User navigates to /forgot-password
    ↓
User enters email and submits
    ↓
ForgotPassword.tsx calls authService.forgotPassword()
    ↓
Backend verifies email exists in database
    ↓
OTP sent to user's email
    ↓
Automatic navigation to /reset-password?email=<email>
    ↓
ResetPassword.tsx pre-fills email (read-only)
    ↓
User enters OTP, new password, and confirm password
    ↓
ResetPassword.tsx calls authService.resetPassword()
    ↓
Backend validates OTP and updates password
    ↓
Success message displayed
    ↓
Automatic redirect to /login after 2 seconds
```

---

## 🔐 Authentication Flow (Detailed)

### **Initial Load**

1. **App.tsx renders** → Wraps in `AuthProvider`
2. **AuthContext initializes:**
   - `useEffect` runs
   - Checks `localStorage` for `access_token`
   - If found:
     - Checks expiration using `isTokenExpired()`
     - If valid: Decodes JWT to get user info
     - Sets user state
   - Sets `loading` to false

3. **ProtectedRoute checks:**
   - If loading: Shows loading indicator
   - If not authenticated: Redirects to `/login`
   - If authenticated: Renders protected component

### **Login Process**

1. User submits login form
2. `Login.tsx` calls `useAuth().login(email, password)`
3. `AuthContext.login()`:
   - Calls `authService.login(credentials)`
   - Receives `{ access_token, refresh_token }`
   - Stores in `localStorage`
   - Decodes `access_token` to get user info
   - Updates `user` state
4. `ProtectedRoute` detects authentication
5. User redirected to `/dashboard`

### **Token Refresh**

1. API request returns 401
2. `api.ts` response interceptor catches it
3. Retrieves `refresh_token` from `localStorage`
4. Calls `/auth/refresh` endpoint
5. Receives new tokens
6. Updates `localStorage`
7. Retries original request with new token
8. If refresh fails: Clears tokens and redirects to login

---

## 🔗 Component Relationships

### **Dependency Graph**

```
App.tsx
├── AuthProvider (contexts/AuthContext.tsx)
│   ├── authService (services/authService.ts)
│   │   └── api (services/api.ts)
│   └── jwt utils (utils/jwt.ts)
├── ProtectedRoute (components/ProtectedRoute.tsx)
│   └── useAuth (from AuthContext)
└── Pages
    ├── Login.tsx
    │   └── useAuth (from AuthContext)
    ├── Signup.tsx
    │   └── useAuth (from AuthContext)
    ├── ForgotPassword.tsx
    │   └── authService
    ├── ResetPassword.tsx
    │   └── authService
    ├── Dashboard.tsx
    │   ├── useAuth (from AuthContext)
    │   ├── documentService
    │   └── askService
    └── AdminDashboard.tsx
        ├── useAuth (from AuthContext)
        └── adminService
```

### **Data Flow Between Components**

```
AuthContext (Global State)
    ↑
    │ provides
    │
    ├──→ Login.tsx (uses login function)
    ├──→ Signup.tsx (uses signup function)
    ├──→ Dashboard.tsx (uses user, logout)
    ├──→ AdminDashboard.tsx (uses logout)
    └──→ ProtectedRoute (uses isAuthenticated, isAdmin)
```

---

## 🌐 API Integration

### **Request Flow**

```
Component
    ↓
Service Function (authService, documentService, etc.)
    ↓
api.ts (Axios instance)
    ↓
Request Interceptor (adds token)
    ↓
Vite Proxy (/api → http://localhost:8000)
    ↓
Backend API
```

### **Response Flow**

```
Backend API
    ↓
Vite Proxy
    ↓
Response Interceptor (handles 401, token refresh)
    ↓
api.ts
    ↓
Service Function
    ↓
Component (updates state)
```

### **Error Handling**

1. **Network Errors:**
   - Caught in service functions
   - Displayed in component error state
   - User-friendly messages shown

2. **401 Unauthorized:**
   - Caught by response interceptor
   - Automatic token refresh attempted
   - If refresh fails: Redirect to login

3. **Validation Errors:**
   - Client-side validation in forms
   - Backend validation errors displayed
   - Clear error messages

---

## 📊 State Management

### **Global State (AuthContext)**

- **Location:** `contexts/AuthContext.tsx`
- **Scope:** Entire application
- **State:**
  - `user`: User object (id, name, email, role)
  - `loading`: Initialization state
  - `isAuthenticated`: Computed boolean
  - `isAdmin`: Computed boolean

### **Local State (Components)**

Each component manages its own local state:
- Form inputs
- Loading states
- Error messages
- API responses

### **Persistent State (localStorage)**

- `access_token`: JWT access token
- `refresh_token`: JWT refresh token

---

## 🛣️ Routing Logic

### **Route Configuration**

```typescript
Routes:
  /login → Login (public)
  /signup → Signup (public)
  /forgot-password → ForgotPassword (public)
  /reset-password → ResetPassword (public)
  /dashboard → Dashboard (protected)
  /admin → AdminDashboard (protected, admin only)
  / → Redirect to /dashboard
```

### **Route Protection**

1. **Public Routes:**
   - No protection
   - Accessible to all users
   - Examples: Login, Signup

2. **Protected Routes:**
   - Wrapped in `ProtectedRoute`
   - Requires authentication
   - Redirects to `/login` if not authenticated
   - Example: Dashboard

3. **Admin Routes:**
   - Wrapped in `ProtectedRoute` with `requireAdmin={true}`
   - Requires authentication AND admin role
   - Redirects to `/dashboard` if not admin
   - Example: AdminDashboard

### **Navigation Guards**

- `ProtectedRoute` acts as navigation guard
- Checks authentication before rendering
- Handles redirects automatically
- Shows loading state during checks

---

## 🎨 Styling Approach

### **CSS Organization**

1. **Global Styles** (`index.css`):
   - CSS reset
   - Base typography
   - Global variables

2. **Component Styles:**
   - Each page has its own CSS file
   - Scoped to component
   - Modular approach

3. **Shared Styles:**
   - `Auth.css` shared by all auth pages
   - Consistent styling across auth flow

### **Design Principles**

- **Minimal:** Clean, assessment-level design
- **Responsive:** Mobile-first approach
- **Modern:** Gradient backgrounds, card layouts
- **Accessible:** Proper form labels, error messages

---

## 🔧 Key Implementation Details

### **Type Safety**

- All API responses typed with TypeScript interfaces
- Props and state fully typed
- Compile-time error checking

### **Error Handling**

- Try-catch blocks in async functions
- Error states in components
- User-friendly error messages
- Automatic retry for token refresh

### **Performance**

- Lazy loading not needed (small app)
- Efficient re-renders with React hooks
- Minimal API calls
- Token caching in localStorage

### **Security**

- Tokens stored in localStorage (not cookies)
- Automatic token refresh
- Token expiration checking
- Role-based access control

---

## 🚀 How Everything Works Together

1. **User opens app** → `main.tsx` renders `App.tsx`
2. **App.tsx** wraps in `AuthProvider` and sets up routes
3. **AuthContext** initializes and checks for existing tokens
4. **ProtectedRoute** checks authentication status
5. **User navigates** → React Router handles routing
6. **User interacts** → Component calls service function
7. **Service function** → Uses `api.ts` to make HTTP request
8. **api.ts** → Adds token, sends request through proxy
9. **Backend responds** → Response interceptor handles errors
10. **Component updates** → State changes trigger re-render
11. **UI updates** → User sees new data

---

## 📝 Summary

The frontend is built with a **clean, maintainable architecture** that separates concerns:

- **Pages** handle UI and user interaction
- **Services** handle API communication
- **Context** manages global state
- **Components** provide reusable functionality
- **Utils** provide helper functions

All components work together through:
- React Context for state sharing
- Service layer for API calls
- React Router for navigation
- TypeScript for type safety

This architecture makes the codebase:
- ✅ Easy to understand
- ✅ Easy to maintain
- ✅ Easy to test
- ✅ Easy to extend
