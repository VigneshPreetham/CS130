import logo from '../assets/logo.png'
import { useEffect, useState } from 'react';
import { TileList, SingleObject } from '../components/tileList';
import { useSearchParams } from 'react-router-dom';
import { searchRecipes } from '../api/api';

 interface User {
    name: string,
    id: string,
}


let recipes: SingleObject[] = [
    {id: "1", name: "Pizza", pic: logo},
    {id: "2", name: "Pasta", pic: logo},
    {id: "3", name: "Gourmet Salad", pic: logo},
    {id: "4", name: "Human Flesh", pic: logo},
    
]

let users: SingleObject[] = [
    {id: "1", name: "Zack", pic: logo},
    {id: "2", name: "Sam", pic: logo},
    {id: "3", name: "Luca", pic: logo},

]


export default function SearchResultsPage() {
    const [showUsers, setShowUser] = useState<boolean>(false)
    //const [users, setUsers] = useState<SingleObject[]>([])
    //const [recipes, setRecipes] = useState<SingleObject[]>()
    const [searchParams, setSearchParams] = useSearchParams()


    useEffect(() =>{
        searchRecipes(searchParams.get("searchText")).then(result => {
                
            }
        );
    })



    return (
        <div>
            <div className='w-full flex justify-center'>
                <div className='rounded-md border-2 border-black'>

                    <button 
                        className={showUsers ? 'rounded-md m-1 p-3' : 'font-bold bg-logo-red rounded-md m-1 p-3'}
                        onClick={()=>{setShowUser(false)}}
                        >
                        Recipes
                    </button>
                    <button 
                        className={showUsers ? 'font-bold bg-logo-red rounded-md m-1 p-3' : 'rounded-md m-1 p-3'}
                        onClick={()=>{setShowUser(true)}}
                    >
                        Users
                    </button>
                </div>

            </div>
            <TileList isUser={showUsers} toList={showUsers ? users : recipes}/>
        </div>
    )
}