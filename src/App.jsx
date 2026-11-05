import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import InspectionPage from './pages/InspectionPage.jsx';
import AboutPage from './pages/AboutPage.jsx';

/**
 * VEERA Application Root
 *
 * Sets up routing between the inspection workspace and methodology page.
 */
export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<InspectionPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}
