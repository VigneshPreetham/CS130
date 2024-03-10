import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Header from "./pages/Header";
import SignInPage from "./pages/sign-in/SignIn";
import PicAndRecipe from "./pages/PicAndRecipe";
import RecipesListPage from "./pages/RecipesListPage";
import SignUpPage from "./pages/sign-up/SignUp";
import UploadImagePage from "./pages/upload-image/UploadImagePage";

import { useUser } from "./hooks/useUser";

function App() {
    const { loggedIn } = useUser();

    return (
        <Router>
            <div className="App">
                <Header />
                <Routes>
                    {loggedIn ? (
                        <>
                            <Route path="/upload" element={<UploadImagePage />} />
                            <Route path="/recipe/:id" element={<PicAndRecipe exampleParam={"2"} />} />
                            <Route path="/user/:id/recipes" element={<RecipesListPage />} />
                            <Route path="*" element={<Navigate replace to="/upload" />} />
                        </>
                    ) : (
                        <>
                            <Route path="/sign-in" element={<SignInPage />} />
                            <Route path="/sign-up" element={<SignUpPage />} />
                            <Route path="*" element={<Navigate replace to="/sign-in" />} />
                        </>
                    )}
                </Routes>
            </div>
        </Router>
    );
}

export default App;
