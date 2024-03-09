import React from 'react';
import { RecipeTile } from './recipeTile';

export interface SingleRecipe {
    name: string,
    id: string,
    pic: any,
}


interface RecipeTileListProps {
    recipes: SingleRecipe[],
}


export function RecipeTileList({recipes}: RecipeTileListProps){
    return (
        <div>
            {recipes.map((recipe, i) => 
                <RecipeTile index={i+1} name={recipe.name} id={recipe.id} pic={recipe.pic}/>
            )}
        </div>
    )
}