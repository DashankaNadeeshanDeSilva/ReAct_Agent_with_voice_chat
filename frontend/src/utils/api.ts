// API configuration
const API_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// Generic API call handler with error handling
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'API request failed');
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Unknown error occurred' };
  }
}

// Document upload service
export async function uploadDocument(file: File): Promise<ApiResponse<{ message: string }>> {
  const formData = new FormData();
  formData.append('file', file);

  return apiCall('/documents/upload', {
    method: 'POST',
    body: formData,
    headers: {
      // Remove Content-Type to let browser set it with boundary for FormData
      'Content-Type': undefined,
    },
  });
}

// Chat service
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

export interface ChatResponse {
  message: string;
  sources?: {
    document: string;
    relevance: number;
  }[];
}

export async function sendChatMessage(message: string): Promise<ApiResponse<ChatResponse>> {
  return apiCall('/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}