import { Route, Routes } from "react-router-dom";
import Main from "@pages/Main/Main";
import Report from "@pages/Report/Report";
import Settings from "@pages/Settings/Settings";
import NotFound from "@pages/NotFound/NotFound";

function App() {
  if (window?.Telegram?.WebApp) {
    window.Telegram.WebApp.ready();
    window.Telegram.WebApp.expand();
  }
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/report" element={<Report />} />
      <Route path="/setting" element={<Settings />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;
