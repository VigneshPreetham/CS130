import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import SignInPage from "./pages/sign-in/SignIn";
import SignUpPage from "./pages/sign-up/SignUp";
import UploadImagePage from "./pages/upload-image/UploadImagePage";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/sign-in" element={<SignInPage />} />
          <Route path="/sign-up" element={<SignUpPage />} />
          <Route path="/upload" element={<UploadImagePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
