/**
 * JWT Authentication Utilities
 * Handles token storage, retrieval, and API requests with authentication
 */

interface User {
  id: number;
  name: string;
  email: string;
  state?: string;
  role: 'volunteer' | 'admin';
  skills?: string[];
}

interface AuthResponse {
  message: string;
  token: string;
  user: User;
}

const TOKEN_KEY = 'jwt_token';
const USER_KEY = 'user_data';

/**
 * Store JWT token and user data in localStorage
 */
export const setAuthData = (token: string, user: User): void => {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

/**
 * Get stored JWT token
 */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Get stored user data
 */
export const getUser = (): User | null => {
  const userData = localStorage.getItem(USER_KEY);
  if (!userData) return null;
  
  try {
    return JSON.parse(userData);
  } catch {
    return null;
  }
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  return !!getToken();
};

/**
 * Check if user is an admin
 */
export const isAdmin = (): boolean => {
  const user = getUser();
  return user?.role === 'admin';
};

/**
 * Clear authentication data (logout)
 */
export const clearAuth = (): void => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

/**
 * Get authorization headers for API requests
 */
export const getAuthHeaders = (): HeadersInit => {
  const token = getToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
};

/**
 * Make an authenticated API request
 */
export const authenticatedFetch = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  const headers = getAuthHeaders();
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...headers,
      ...(options.headers || {}),
    },
  });

  // Handle token expiration
  if (response.status === 401) {
    // Token expired or invalid
    clearAuth();
    // Optionally redirect to login
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
  }

  return response;
};

/**
 * Login user
 */
export const login = async (email: string, password: string): Promise<AuthResponse> => {
  const response = await fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Login failed');
  }

  const data: AuthResponse = await response.json();
  setAuthData(data.token, data.user);
  return data;
};

/**
 * Signup new user
 */
export const signup = async (
  name: string,
  email: string,
  password: string,
  state: string,
  skills: string[]
): Promise<AuthResponse> => {
  const response = await fetch('http://localhost:5000/api/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, email, password, state, skills }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Signup failed');
  }

  const data: AuthResponse = await response.json();
  setAuthData(data.token, data.user);
  return data;
};

/**
 * Logout user
 */
export const logout = (): void => {
  clearAuth();
  window.location.href = '/login';
};

/**
 * Get current user profile (requires authentication)
 */
export const getProfile = async (): Promise<any> => {
  const response = await authenticatedFetch('http://localhost:5000/api/profile/profile');
  
  if (!response.ok) {
    throw new Error('Failed to fetch profile');
  }
  
  return response.json();
};

/**
 * Update user profile (requires authentication)
 */
export const updateProfile = async (data: any): Promise<any> => {
  const response = await authenticatedFetch('http://localhost:5000/api/profile/profile', {
    method: 'POST',
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error('Failed to update profile');
  }
  
  return response.json();
};
