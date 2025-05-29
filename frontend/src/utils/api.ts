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
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
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

  return apiCall('/upload_document', {
    method: 'POST',
    body: formData,
  });
}

// Chat message service
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

export async function sendChatMessage(message: string): Promise<ApiResponse<{ response: string }>> {
  return apiCall('/chat_with_agent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      user_message: message,
      session_id: "123456" // Example session ID, replace with actual session management 
    }),
  });
}