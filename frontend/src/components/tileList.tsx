import React from 'react';
import { Tile } from './tile';

export interface SingleObject {
    name: string,
    id: string,
    usersAdded: string[],
}


interface TileListProps {
    toList: SingleObject[],
    isUser: boolean,
}


export function TileList({toList, isUser}: TileListProps){
    return (
        <div>
            {toList.map((recipe, i) => 
                <Tile usersAdded={recipe.usersAdded} isUser={isUser} index={i+1} name={recipe.name} id={recipe.id}/>
            )}
        </div>
    )
}