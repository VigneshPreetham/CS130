import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./pages/Header";
import SignInPage from "./pages/sign-in/SignIn";
import PicAndRecipe from "./pages/PicAndRecipe";
import RecipesListPage from "./pages/RecipesListPage";
import SignUpPage from "./pages/sign-up/SignUp";
import UploadImagePage from "./pages/upload-image/UploadImagePage";

function App() {
    return (
        <Router>
            <div className="App">
                <Header></Header>
                <Routes>
                    <Route path="/sign-in" element={<SignInPage />} />
                    <Route path="/sign-up" element={<SignUpPage />} />
                    <Route path="/upload" element={<UploadImagePage />} />
                    <Route path="/recipe/:id" element={<PicAndRecipe exampleParam={"2"} />} />
                    <Route path="/user/:id/recipes" element={<RecipesListPage></RecipesListPage>} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
