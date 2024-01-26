import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import SignInPage from "./pages/sign-in/SignIn";

// Create blank components for each route

const SignUp = () => <div>Sign Up</div>;
const Dashboard = () => <div>Dashboard</div>;

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/sign-in" element={<SignInPage />} />
                    <Route path="/sign-up" element={<SignUp />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
