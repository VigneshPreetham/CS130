import logo from '../assets/logo.png';
import { useParams } from "react-router-dom";
import React, { useEffect, useState } from 'react';
import { addRecipeToUser, dbRecipe, getImage, getRecipe, removeRecipeFromUser } from '../api/api';
import { useUser } from '../hooks/useUser';


let pizzaPocket: dbRecipe = {
    name: "Pizza Pocket",
    id: "",
    recipe: "",
    created_by: "",
    created_on: "",
    users_added: []
};

export default function PicAndRecipe() {
    let { id } = useParams()
    const [recipe, setRecipe] = useState<dbRecipe>(pizzaPocket)
    const [recipeId, setRecipeId] = useState<string>("")
    const [pic, setPic] = useState<any>()
    const user = useUser();
    const [reload, setReload] = useState<boolean>(false)



    useEffect(() =>{
        const rI = id == undefined ? "" : id
        setRecipeId(rI)
        getImage(rI).then((r) => {
            setPic(URL.createObjectURL(r))
        })
        getRecipe(rI).then((r) => {
            setRecipe(r)
        })
    }, [reload])

    return (
        <div className="h-screen w-screen flex justify-center bg-gray-50">
            <div className="relative bg-slate-200 border-2 items-center rounded-lg border-black w-3/4 h-fit h-rounded-lg flex flex-col m-5 lg:px-8">
                <div className="m-2 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900"> {recipe.name} </div>
                <div className='absolute top-3 right-0 m-w'>
                {(recipe.users_added.indexOf(user.userId) > -1) ? 
                        (<button onClick={() => {
                            removeRecipeFromUser(user.userId, recipeId).then(()=>{setReload(!reload)})
                        }} className="absolute border-black rounded-md right-5 m-1 w-6 h-6 hover:bg-logo-red">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        </button>) 
                        :
                        (<button onClick={() => {
                            addRecipeToUser(user.userId, recipeId).then(()=>{setReload(!reload)})}} className="absolute border-black rounded-md right-5 m-1 w-6 h-6 hover:bg-logo-red">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                            </svg>
                        </button>)
                    }
                </div>
                <img src={pic} alt="pic" className="m-4 w-[400px]" />
                <div className="list-decimal m-2">
                    {recipe.recipe}
                </div>
            </div>
        </div>
    );
}
