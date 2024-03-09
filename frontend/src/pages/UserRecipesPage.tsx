import logo from '../assets/logo.png'
import React from 'react';
import { RecipeTileList, SingleRecipe } from '../components/recipeTileList';

const navigateToRecipe = (id: string) => {

}

let recipes: SingleRecipe[] = [
    {id: "1", name: "Pizza", pic: logo},
    {id: "2", name: "Pasta", pic: logo},
    {id: "3", name: "Gourmet Salad", pic: logo},
    {id: "4", name: "Human Flesh", pic: logo},
    
]


export default function RecipesListPage() {
    return (
        <div>
            <div className="m-4 font-bold text-center text-logo-red text-2xl">USERNAME's Recipes</div>
            <RecipeTileList recipes={recipes}></RecipeTileList>
        </div>
    )
}