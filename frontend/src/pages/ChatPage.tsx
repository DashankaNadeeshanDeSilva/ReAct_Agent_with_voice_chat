import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, RefreshCw } from 'lucide-react';
import { sendChatMessage, type ChatMessage } from '../utils/api';

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      text: 'Hello! I\'m your document assistant. Upload documents in the Upload section, then ask me questions about them here.',
      sender: 'assistant',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (inputValue.trim() === '' || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage(inputValue.trim());
      
      if (response.error) {
        throw new Error(response.error);
      }

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: response.data?.message || 'Sorry, I encountered an error processing your request.',
        sender: 'assistant',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to get response');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-13rem)] flex flex-col">
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Chat with Your Documents</h1>
        <p className="text-gray-600">
          Ask questions about your uploaded documents to get instant insights.
        </p>
      </div>

      <div className="flex-1 overflow-hidden flex flex-col bg-white border border-gray-200 rounded-lg shadow-sm">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map(message => (
            <div 
              key={message.id} 
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex max-w-[80%] ${message.sender === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
                  message.sender === 'user' ? 'bg-blue-100 ml-2' : 'bg-gray-100 mr-2'
                }`}>
                  {message.sender === 'user' 
                    ? <User className="h-4 w-4 text-blue-600" /> 
                    : <Bot className="h-4 w-4 text-gray-600" />
                  }
                </div>
                <div>
                  <div className={`rounded-lg px-4 py-2 mb-1 ${
                    message.sender === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                  </div>
                  <p className={`text-xs ${
                    message.sender === 'user' ? 'text-right text-gray-500' : 'text-gray-500'
                  }`}>
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex max-w-[80%]">
                <div className="flex-shrink-0 h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center mr-2">
                  <Bot className="h-4 w-4 text-gray-600" />
                </div>
                <div className="bg-gray-100 rounded-lg px-4 py-2 text-gray-800">
                  <div className="flex items-center space-x-2">
                    <RefreshCw className="h-4 w-4 text-gray-500 animate-spin" />
                    <p className="text-sm">Thinking...</p>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {error && (
            <div className="flex justify-center">
              <div className="bg-red-100 text-red-600 px-4 py-2 rounded-lg text-sm">
                {error}
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="border-t border-gray-200 p-4">
          <div className="flex items-end space-x-2">
            <div className="flex-1 min-h-[3rem]">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask something about your documents..."
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[3rem] max-h-[12rem]"
                rows={1}
                style={{ height: 'auto', minHeight: '3rem' }}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={inputValue.trim() === '' || isLoading}
              className={`p-2 rounded-full ${
                inputValue.trim() === '' || isLoading
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              } transition-colors duration-200`}
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;