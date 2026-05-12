import apiClient from './client';
import type { ChatMessage, ChatResponse } from '../types';

export const sendChatMessage = (message: string, sessionId: string, history: ChatMessage[]) =>
  apiClient.post<ChatResponse>('/chatbot/message', {
    message,
    session_id: sessionId,
    conversation_history: history,
  }).then(r => r.data);
