'use client';

import { useState } from 'react';
import ChatInput from '@/components/ChatInput';
import ChatMessages from '@/components/ChatMessages';
import Navbar from '@/components/navbar';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

type ModelOption = 'gpt-3.5-turbo' | 'grok-2' | 'deepseek-r1' | 'claude-3.5-sonnet';

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState<ModelOption>('gpt-3.5-turbo');

  const models: { value: ModelOption; label: string }[] = [
    { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
    { value: 'grok-2', label: 'Grok 2' },
    { value: 'deepseek-r1', label: 'DeepSeek R1' },
    { value: 'claude-3.5-sonnet', label: 'Claude 3.5 Sonnet' },
  ];

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Add user message to chat
    const newMessages = [...messages, { role: 'user' as const, content: message }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const response = await fetch('/server/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          model: selectedModel
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      // Create a new message for the assistant's response
      const assistantMessage: ChatMessage = { role: 'assistant', content: '' };
      setMessages([...newMessages, assistantMessage]);

      // Read the streaming response
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // Decode the received chunk
        const chunk = new TextDecoder().decode(value);
        
        // Update the assistant's message with the new chunk
        assistantMessage.content += chunk;
        setMessages([...newMessages, { ...assistantMessage }]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <div className="container mx-auto max-w-4xl flex-1 flex flex-col">
        <div className="p-4">
          <select 
            className="select select-bordered w-full max-w-xs"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value as ModelOption)}
          >
            {models.map((model) => (
              <option key={model.value} value={model.value}>
                {model.label}
              </option>
            ))}
          </select>
        </div>
        <div className="flex-1 overflow-y-auto p-4">
          <ChatMessages messages={messages} />
        </div>
        <div className="p-4 mt-auto">
          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
} 