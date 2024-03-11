import { Link } from "react-router-dom";
import profilePic from "../assets/profile.webp"
import React, { useEffect, useState } from 'react';
import { addRecipeToUser, dbRecipe, getImage, getRecipe, removeRecipeFromUser } from "../api/api";
import { useUser } from "../hooks/useUser";


export interface TileProps {
    index: Number,
    name: string,
    id: string,
    isUser: boolean,
    usersAdded: string[]
}

let pizzaPocket: dbRecipe = {
    name: "Pizza Pocket",
    id: "",
    recipe: "",
    created_by: "",
    created_on: "",
    users_added: []
};



export function Tile({index, id, isUser, name}: TileProps){
    const [pic, setPic] = useState<any>()
    const [recipe, setRecipe] = useState<dbRecipe>(pizzaPocket)
    const [reload, setReload] = useState<boolean>(false)
    const user = useUser();

    useEffect(() =>{
        if (isUser){
            setPic(profilePic);
        } else {
            getImage(id).then((r) => setPic(URL.createObjectURL(r)))
            getRecipe(id).then((r) => {
                setRecipe(r)
            })
        }
    }, [reload])

    return (
        <div className="flex w-full justify-center my-3">
            <div className="relative flex place-items-center w-1/2 h-20 bg-slate-200 rounded-md border-2 border-black" >
                <div className='p-5 text-lg font-bold'>{index.toString()}.</div>
                <img src={pic} alt="test" className='h-full p-5'/>
                {isUser ? 
                    (<Link to={'/user/'+id + '/recipes'} className='p-5 font-bold'> {name} </Link>)
                    :
                    (<>
                        <Link to={'/recipe/'+id} className='p-5 font-bold'> {name} </Link>
                        {(recipe.users_added.indexOf(user.userId) > -1) ? 
                            (<button onClick={() => {removeRecipeFromUser(user.userId, id).then(()=>{setReload(!reload)})}} className="absolute border-black rounded-md right-5 m-1 w-6 h-6 hover:bg-logo-red">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                </svg>
                            </button>) 
                            :
                            (<button onClick={() => {addRecipeToUser(user.userId, id).then(()=>{setReload(!reload)})}} className="absolute border-black rounded-md right-5 m-1 w-6 h-6 hover:bg-logo-red">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                </svg>
                            </button>)
                        }
                    </>)
                }
            </div>
        </div>
    )
}