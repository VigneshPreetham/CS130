import { useEffect, useState } from 'react';
import logo from '../assets/logo.png'
import { TileList, SingleObject } from '../components/tileList';
import { getRecipes } from '../api/api';

const userId = 'f650444e-1154-49f6-94aa-6a1acfdc0ae7';

let recipesData: SingleObject[] = [
    {id: "1", name: "Pizza", pic: logo},
    {id: "2", name: "Pasta", pic: logo},
    {id: "3", name: "Gourmet Salad", pic: logo},
    {id: "4", name: "Human Flesh", pic: logo},
    
]


export default function UserRecipesPage() {

    const [recipes, setRecipes] = useState<SingleObject[]>(recipesData);

    useEffect(() =>{
        getRecipes(userId).then(result => {
                setRecipes(result)
            }
        );
    })


    return (
        <div>
            <div className="m-4 font-bold text-center text-logo-red text-2xl">USERNAME's Recipes</div>
            <TileList isUser={false} toList={recipes}/>
        </div>
    )
}