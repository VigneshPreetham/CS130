import { Link } from "react-router-dom";
import React from 'react';


export interface RecipeTileProps {
    index: Number,
    name: string,
    id: string,
    pic: any,
}


export function RecipeTile({index, name, id, pic}: RecipeTileProps){
    const globalUser = '2';

    return (
        <div className="flex w-full justify-center my-3">
            <div className="relative flex place-items-center w-1/2 h-20 bg-slate-200 rounded-md border-2 border-black" >
                <div className='p-5 text-lg font-bold'>{index.toString()}.</div>
                <img src={pic} alt="test" className='h-full p-5'/>
                <Link to={'/recipe/'+id} className='p-5 font-bold'> {name} </Link>
                {(globalUser == id) ? 
                    (<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="absolute right-5 m-1 w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                    </svg>) 
                    :
                    (<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="absolute right-5 m-1 w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                    </svg>)}
            </div>
        </div>
    )
}