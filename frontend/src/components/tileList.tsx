import React from 'react';
import { Tile } from './tile';

export interface SingleObject {
    name: string,
    id: string,
    pic: any,
}


interface TileListProps {
    toList: SingleObject[],
    isUser: boolean,
}


export function TileList({toList, isUser}: TileListProps){
    return (
        <div>
            {toList.map((recipe, i) => 
                <Tile isUser={isUser} index={i+1} name={recipe.name} id={recipe.id} pic={recipe.pic}/>
            )}
        </div>
    )
}