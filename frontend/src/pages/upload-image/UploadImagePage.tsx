import { useState } from "react";

import { uploadImage } from "../../api/api";

export default function UploadImagePage() {
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [recipe, setRecipe] = useState<string | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            setUploadedFile(file);
            setRecipe(null); // Reset recipe when a new file is uploaded
        }
    };

    const handleDeleteFile = () => {
        setUploadedFile(null);
        setRecipe(null); // Reset recipe when the file is deleted
    };

    const handleGenerateRecipe = async () => {
        if (uploadedFile) {
            try {
                await uploadImage(uploadedFile);
            } catch (error) {
                alert(error);
            }
        }

        // For now, we'll just set a static random recipe
        setRecipe("Random Recipe: 1 cup of flour, 2 eggs, 1/2 cup sugar, 1 tsp vanilla extract, bake for 20 minutes.");
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
                            <div className="flex items-center justify-between w-full max-w-sm p-2 text-gray-700 border-2 border-gray-300 rounded-lg">
                                {uploadedFile.name}
                                <button onClick={handleDeleteFile}>X</button>
                            </div>
                        )}
                        <button
                            className={`flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ${
                                uploadedFile ? "bg-logo-red hover:bg-red-500 focus-visible:outline-logo-red" : "bg-gray-300"
                            }`}
                            disabled={!uploadedFile}
                            onClick={handleGenerateRecipe}
                        >
                            Generate Recipe
                        </button>
                        {recipe && (
                            <div className="w-full max-w-sm p-4 border border-gray-300 rounded-lg dark:border-gray-700">
                                <h2 className="mb-2 text-xl font-semibold">Recipe</h2>
                                <p className="text-gray-600 dark:text-gray-400">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore
                                    magna aliqua.
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
