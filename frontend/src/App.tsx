import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ChatPage from './pages/ChatPage';
import UploadPage from './pages/UploadPage';
import Layout from './components/Layout';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<LandingPage />} />
          <Route path="chat" element={<ChatPage />} />
          <Route path="upload" element={<UploadPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;