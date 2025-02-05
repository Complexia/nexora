"use client";

import { ChatMessage } from '@/components/chat-page';

interface ChatMessagesProps {
  messages: ChatMessage[];
}

export default function ChatMessages({ messages }: ChatMessagesProps) {
  return (
    <div className="space-y-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`chat ${
            message.role === 'user' ? 'chat-end' : 'chat-start'
          }`}
        >
          <div className="chat-bubble">
            {message.content}
          </div>
        </div>
      ))}
    </div>
  );
} 