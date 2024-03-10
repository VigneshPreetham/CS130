import { useEffect, useState } from 'react';
import logo from '../assets/logo.png'
import { RecipeTileList, SingleRecipe } from '../components/recipeTileList';
import { getRecipes } from '../api/api';

const userId = '1';

let recipesData: SingleRecipe[] = [
    {id: "1", name: "Pizza", pic: logo},
    {id: "2", name: "Pasta", pic: logo},
    {id: "3", name: "Gourmet Salad", pic: logo},
    {id: "4", name: "Human Flesh", pic: logo},
    
]


export default function UserRecipesPage() {

    const [recipes, setRecipes] = useState<SingleRecipe[]>(recipesData);

    useEffect(() =>{
        getRecipes(userId).then(result => {
                setRecipes(result)
            }
        );
    })

    


    return (
        <div>
            <div className="m-4 font-bold text-center text-logo-red text-2xl">USERNAME's Recipes</div>
            <RecipeTileList recipes={recipes}></RecipeTileList>
        </div>
    )
}