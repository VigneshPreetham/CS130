import logo from '../assets/logo.png';
import { useParams } from "react-router-dom";
import React, { useEffect, useState } from 'react';
import { dbRecipe, getRecipe } from '../api/api';


let pizzaPocket: dbRecipe = {
    name: "Pizza Pocket",
    link: "",
    id: "",
    recipe: "",
    created_by: "",
    created_on: ""
};

export default function PicAndRecipe() {
    let { id } = useParams();
    const [recipe, setRecipe] = useState<dbRecipe>(pizzaPocket)

    useEffect(() =>{
        const recipeId = id == undefined ? "" : id
        getRecipe(recipeId).then((r) => setRecipe(r))
    }, [])

    return (
        <div className="h-screen w-screen flex justify-center bg-gray-50">
            <div className="bg-slate-200 border-2 items-center rounded-lg border-black w-3/4 h-fit h-rounded-lg flex flex-col m-5 lg:px-8">
                <div className="m-2 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900"> {recipe.name} </div>
                <img src={recipe.link} alt="test" className="m-4 w-[400px]" />
                <div className="list-decimal m-2">
                    {recipe.recipe}
                </div>
            </div>
        </div>
    );
}
