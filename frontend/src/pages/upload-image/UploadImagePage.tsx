import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { uploadImage, addRecipeToUser } from "../../api/api";
import { useUser } from "../../hooks/useUser";

export default function UploadImagePage() {
    const navigate = useNavigate();
    const { userId } = useUser();
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [foodName, setFoodName] = useState<string | null>(null);
    const [recipe, setRecipe] = useState<string>("");
    const [recipeId, setRecipeId] = useState<string>("");
    const [loading, setLoading] = useState(false);
    const [recipeOpacity, setRecipeOpacity] = useState(0);

    const [saveRecipeLoading, setSaveRecipeLoading] = useState(false);

    useEffect(() => {
        if (recipe) {
            setRecipeOpacity(1); // Make the recipe visible by fading in
        } else {
            setRecipeOpacity(0); // Hide the recipe
        }
    }, [recipe]);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            setUploadedFile(file);
            setRecipe(""); // Reset recipe when a new file is uploaded
        }
    };

    const handleDeleteFile = () => {
        setUploadedFile(null);
        setRecipe(""); // Reset recipe when the file is deleted
    };

    const handleGenerateRecipe = async () => {
        if (uploadedFile) {
            try {
                setLoading(true);
                const res = await uploadImage(uploadedFile, userId);
                setLoading(false);
                setFoodName(res.name);
                setRecipe(res.recipe);
                setRecipeId(res.id);
            } catch (error) {
                alert(error);
            }
        }
    };

    const handleSaveRecipe = async () => {
        if (foodName && recipe) {
            try {
                setSaveRecipeLoading(true);
                await addRecipeToUser(userId, recipeId);
                setSaveRecipeLoading(false);
                navigate(`/recipe/${recipeId}`);
            } catch (error) {
                alert(error);
            }
        }
    };

    return (
        <div className="flex flex-col min-h-screen">
            <main className="flex flex-col items-center justify-start mt-[200px] flex-1 gap-4">
                <div className="flex flex-col items-center gap-2">
                    <h1 className="text-3xl font-bold tracking-tight">Upload a food item to generate a recipe!</h1>
                    <div className="flex flex-col items-center w-full max-w-sm gap-2">
                        {!uploadedFile && (
                            <label className="flex items-center justify-center w-full max-w-sm p-8 text-gray-400 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer">
                                Upload Image
                                <input className="hidden" type="file" accept="image/*" onChange={handleFileChange} />
                            </label>
                        )}
                        {uploadedFile && (
                            <div className="flex flex-col gap-3 w-full items-center">
                                <div className="flex items-center justify-between w-full max-w-sm p-2 text-gray-700 border-2 border-gray-300 rounded-lg">
                                    {uploadedFile.name}
                                    <button onClick={handleDeleteFile}>X</button>
                                </div>
                                <img src={URL.createObjectURL(uploadedFile)} alt="Uploaded file" className="w-[300px] max-w-sm" />
                            </div>
                        )}
                        <button
                            className={`flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ${
                                uploadedFile && !loading ? "bg-logo-red hover:bg-red-500 focus-visible:outline-logo-red" : "bg-gray-300"
                            }`}
                            disabled={!uploadedFile || loading}
                            onClick={handleGenerateRecipe}
                        >
                            {loading ? "Loading..." : "Generate Recipe"}
                        </button>
                    </div>
                    <div
                        className="mt-8 w-full p-4 rounded-lg transition-opacity duration-700 flex flex-col items-center"
                        style={{ opacity: recipeOpacity } as React.CSSProperties}
                    >
                        <h2 className="mb-2 w-full text-3xl font-semibold text-center border border-x-0 border-t-0 pb-2">Recipe: {foodName}</h2>
                        {recipe.split("\n").map((line, index) => (
                            <React.Fragment key={index}>
                                {line}
                                <br />
                            </React.Fragment>
                        ))}
                        <button
                            className={`flex w-[200px] mt-8 justify-center rounded-md px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ${
                                uploadedFile && !loading ? "bg-logo-red hover:bg-red-500 focus-visible:outline-logo-red" : "bg-gray-300"
                            }`}
                            // disabled={saveRecipeLoading}
                            onClick={handleSaveRecipe}
                        >
                            {saveRecipeLoading ? "Saving..." : "Save Recipe"}
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
}
