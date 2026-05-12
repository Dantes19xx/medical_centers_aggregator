import axios from 'axios';
import type { ChatMessage, ChatResponse } from '../types';

const aiClient = axios.create({
  baseURL: import.meta.env.VITE_AI_API_BASE_URL || 'http://localhost:3002/api/ai',
  headers: { 'Content-Type': 'application/json' },
});

type AiChatResponse = {
  success: boolean;
  data?: {
    response: string;
    toolCalls?: unknown[];
  };
  error?: string;
};

export const sendChatMessage = async (
  message: string,
  sessionId: string,
  history: ChatMessage[]
): Promise<ChatResponse> => {
  const { data } = await aiClient.post<AiChatResponse>('/chat', {
    userId: sessionId,
    message,
    history,
  });

  if (!data.success || !data.data) {
    throw new Error(data.error || 'AI chat request failed');
  }

  return {
    response: data.data.response,
    session_id: sessionId,
    suggestions: [],
    cards: [],
  };
};
