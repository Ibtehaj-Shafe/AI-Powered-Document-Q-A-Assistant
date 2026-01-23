# Document Q&A System - Frontend

A modern React + TypeScript frontend application for a Document Q&A system. This application allows users to upload documents (PDF/DOCX) and ask questions based on the uploaded content. It includes authentication, document management, and an admin dashboard.

## 🚀 Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API calls
- **JWT** - Authentication tokens

## 📁 Project Structure

```
Frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # Reusable components
│   │   └── ProtectedRoute.tsx
│   ├── contexts/          # React contexts
│   │   └── AuthContext.tsx
│   ├── pages/             # Page components
│   │   ├── Login.tsx
│   │   ├── Signup.tsx
│   │   ├── ForgotPassword.tsx
│   │   ├── ResetPassword.tsx
│   │   ├── Dashboard.tsx
│   │   ├── AdminDashboard.tsx
│   │   ├── Auth.css
│   │   ├── Dashboard.css
│   │   └── AdminDashboard.css
│   ├── services/          # API service layer
│   │   ├── api.ts         # Axios instance with interceptors
│   │   ├── authService.ts
│   │   ├── documentService.ts
│   │   ├── askService.ts
│   │   └── adminService.ts
│   ├── App.tsx            # Main app component with routing
│   ├── App.css
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 📄 Pages and Components

### Authentication Pages

1. **Login** (`/login`)
   - User login with email and password
   - Redirects to dashboard on success
   - Links to signup and forgot password

2. **Signup** (`/signup`)
   - User registration with name, email, and password
   - Password confirmation validation
   - Automatically logs in after successful signup

3. **Forgot Password** (`/forgot-password`)
   - Request OTP via email
   - Sends OTP to user's email address

4. **Reset Password** (`/reset-password`)
   - Reset password using email, OTP, and new password
   - Validates password match and minimum length

### Main Application Pages

5. **Dashboard** (`/dashboard`)
   - **Document Upload Section**
     - Upload PDF or DOCX files
     - File validation (only PDF and DOCX allowed)
     - Success/error messages
   - **Question & Answer Section**
     - Ask questions about uploaded documents
     - Displays AI-generated answers
     - Loading states during processing
   - **Header**
     - User name display
     - Admin dashboard link (for admin users)
     - Logout button

6. **Admin Dashboard** (`/admin`)
   - **Statistics Cards**
     - Total users count
     - Total files uploaded
     - Total questions asked
   - **User Statistics Table**
     - Displays all users with their stats
     - Shows files uploaded and questions asked per user
     - Responsive table design
   - Protected route (admin only)

### Components

- **ProtectedRoute**: Wraps protected pages and redirects unauthenticated users to login
- **AuthContext**: Manages authentication state, user data, and auth methods

## 🔌 API Integration

### Base Configuration

The API client is configured in `src/services/api.ts`:
- Base URL: `http://localhost:8000` (configurable via `VITE_API_BASE_URL` env variable)
- Automatic JWT token injection in request headers
- Automatic token refresh on 401 errors
- Error handling and token cleanup

### API Endpoints Used

#### Authentication (`/auth`)
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login (returns access_token and refresh_token)
- `POST /auth/refresh` - Refresh access token
- `POST /auth/forgot-password` - Request password reset OTP
- `POST /auth/reset-password` - Reset password with OTP

#### Documents (`/upload`)
- `POST /upload/` - Upload document (requires authentication)
  - Accepts: multipart/form-data with file
  - Returns: Document metadata

#### Questions (`/ask`)
- `POST /ask/` - Ask question about documents (requires authentication)
  - Accepts: `{ query: string }`
  - Returns: `{ answer: string }`

#### Admin (`/admin`)
- `GET /admin/dashboard` - Get admin statistics (requires admin role)
  - Returns: Total users, files, questions, and user_stats array

### Service Layer

All API calls are abstracted into service modules:
- `authService.ts` - Authentication operations
- `documentService.ts` - Document upload operations
- `askService.ts` - Question/answer operations
- `adminService.ts` - Admin dashboard operations

## 🔐 Authentication Flow

### JWT Token Management

1. **Login Flow**:
   - User submits credentials
   - Backend returns `access_token` and `refresh_token`
   - Tokens stored in `localStorage`
   - User data stored in AuthContext

2. **Token Refresh**:
   - Axios interceptor catches 401 errors
   - Automatically attempts token refresh using `refresh_token`
   - Updates tokens in localStorage
   - Retries original request

3. **Logout**:
   - Clears tokens from localStorage
   - Resets user state in AuthContext
   - Redirects to login page

### Protected Routes

- Routes are protected using `ProtectedRoute` component
- Unauthenticated users are redirected to `/login`
- Admin-only routes check user role before allowing access

### Route Protection

```typescript
// Regular protected route
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>

// Admin-only route
<ProtectedRoute requireAdmin={true}>
  <AdminDashboard />
</ProtectedRoute>
```

## 🎨 Styling

- **Global Styles**: `src/index.css` - Base styles and CSS reset
- **Component Styles**: Each page has its own CSS file
- **Responsive Design**: Mobile-friendly with media queries
- **Modern UI**: Gradient backgrounds, card-based layouts, smooth transitions

## 🛠️ Development

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Navigate to the Frontend directory:
```bash
cd Frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional):
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### Running Locally

1. Start the development server:
```bash
npm run dev
```

2. Open your browser and navigate to:
```
http://localhost:3000
```

### Building for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the Frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If not set, defaults to `http://localhost:8000`.

### Vite Configuration

The `vite.config.ts` includes:
- React plugin configuration
- Development server on port 3000
- Proxy configuration for API calls (optional, if using `/api` prefix)

## 📱 Features

### User Features
- ✅ User registration and login
- ✅ Password reset via OTP
- ✅ Document upload (PDF/DOCX)
- ✅ Ask questions about uploaded documents
- ✅ View AI-generated answers
- ✅ Responsive design for mobile and desktop

### Admin Features
- ✅ Admin dashboard with statistics
- ✅ View all users and their statistics
- ✅ Total files and questions metrics
- ✅ User statistics table

## 🚦 Usage Flow

1. **New User**:
   - Sign up at `/signup`
   - Automatically logged in
   - Redirected to dashboard

2. **Existing User**:
   - Login at `/login`
   - Redirected to dashboard

3. **Using the Application**:
   - Upload documents (PDF or DOCX)
   - Ask questions about uploaded content
   - View answers generated by AI

4. **Admin Access**:
   - Login with admin account
   - Access admin dashboard from main dashboard
   - View system-wide statistics

## 🔍 Error Handling

- Form validation on client side
- API error messages displayed to users
- Token expiration handled automatically
- Network errors shown with user-friendly messages

## 📝 Notes

- JWT tokens are stored in `localStorage`
- Access tokens expire after 30 minutes (backend config)
- Refresh tokens expire after 7 days (backend config)
- File uploads are limited to PDF and DOCX formats
- All API calls include authentication headers automatically

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**:
   - Ensure backend is running on `http://localhost:8000`
   - Check `VITE_API_BASE_URL` in `.env` file

2. **Authentication Issues**:
   - Clear localStorage and try logging in again
   - Check browser console for errors

3. **CORS Errors**:
   - Ensure backend has CORS configured to allow requests from `http://localhost:3000`

4. **Build Errors**:
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Vite Documentation](https://vite.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [Axios Documentation](https://axios-http.com/)

## 📄 License

This project is part of an Intern Technical Assessment.
