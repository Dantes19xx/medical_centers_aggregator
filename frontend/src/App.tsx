import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/layout/Layout';
import ChatbotWidget from './components/chatbot/ChatbotWidget';
import HomePage from './pages/HomePage';
import ClinicsPage from './pages/ClinicsPage';
import DoctorsPage from './pages/DoctorsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 1000 * 60 * 5, retry: 1 },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/clinics" element={<ClinicsPage />} />
            <Route path="/doctors" element={<DoctorsPage />} />
            <Route path="*" element={
              <div className="text-center py-20 text-gray-400">
                <p className="text-6xl mb-4">404</p>
                <p>Страница не найдена</p>
              </div>
            } />
          </Route>
        </Routes>
        <ChatbotWidget />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
