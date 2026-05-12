import { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../../api/chatbot';
import type { ChatMessage } from '../../types';

const SESSION_KEY = 'chatbot_session_id';

function getSessionId() {
  let id = localStorage.getItem(SESSION_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: 'Здравствуйте! Я помогу найти клинику или врача. Чем могу помочь?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(['Найти клинику', 'Записаться к врачу', 'Узнать цены']);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    const userMsg: ChatMessage = { role: 'user', content: text };
    const newHistory = [...messages, userMsg];
    setMessages(newHistory);
    setInput('');
    setIsLoading(true);
    setSuggestions([]);

    try {
      const res = await sendChatMessage(text, getSessionId(), messages.slice(-10));
      setMessages([...newHistory, { role: 'assistant', content: res.response }]);
      if (res.suggestions?.length) setSuggestions(res.suggestions);
    } catch {
      setMessages([...newHistory, { role: 'assistant', content: 'Извините, произошла ошибка. Попробуйте позже.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen && (
        <div
          data-testid="chatbot-window"
          className="mb-4 w-80 sm:w-96 bg-white rounded-2xl shadow-xl border border-gray-200 flex flex-col overflow-hidden"
          style={{ height: '480px' }}
        >
          <div className="bg-blue-600 text-white px-4 py-3 flex items-center justify-between">
            <div>
              <p className="font-semibold text-sm">MedFind Ассистент</p>
              <p className="text-xs text-blue-200">Онлайн</p>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-white hover:text-blue-200 text-lg">✕</button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, i) => (
              <div
                key={i}
                data-testid={msg.role === 'user' ? 'user-message' : 'bot-message'}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-xs text-sm px-3 py-2 rounded-2xl ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-sm'
                    : 'bg-gray-100 text-gray-800 rounded-bl-sm'
                }`}>
                  {msg.content}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-500 text-sm px-3 py-2 rounded-2xl rounded-bl-sm">
                  <span className="animate-pulse">...</span>
                </div>
              </div>
            )}

            {suggestions.length > 0 && !isLoading && (
              <div className="flex flex-wrap gap-2 pt-1">
                {suggestions.map((s, i) => (
                  <button
                    key={i}
                    data-testid="suggestion-btn"
                    onClick={() => sendMessage(s)}
                    className="text-xs bg-blue-50 text-blue-600 border border-blue-200 px-3 py-1.5 rounded-full hover:bg-blue-100 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          <div className="border-t border-gray-200 p-3 flex gap-2">
            <input
              data-testid="chatbot-input"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage(input)}
              placeholder="Напишите сообщение..."
              className="flex-1 text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-400"
            />
            <button
              onClick={() => sendMessage(input)}
              disabled={!input.trim() || isLoading}
              className="bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors text-sm"
            >
              →
            </button>
          </div>
        </div>
      )}

      <button
        data-testid="chatbot-toggle"
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-colors flex items-center justify-center text-2xl"
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}
