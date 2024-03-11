import { useEffect, useState } from 'react';
import { TileList, SingleObject } from '../components/tileList';
import { useSearchParams } from 'react-router-dom';
import { searchRecipes, searchUsers } from '../api/api';
import { useUser } from '../hooks/useUser';


export default function SearchResultsPage() {

    const user = useUser();

    const [showUsers, setShowUser] = useState<boolean>(false)
    const [users, setUsers] = useState<SingleObject[]>([])
    const [recipes, setRecipes] = useState<SingleObject[]>([])
    const [searchParams, setSearchParams] = useSearchParams()


    useEffect(() =>{
        console.log(user)
        searchRecipes(searchParams.get("searchText")).then(result => {
                setRecipes(result.map((r) => {
                    return {
                        name: r.name,
                        id: r.id,
                        usersAdded: r.users_added,
                    }}
                ))
            }
        );
        searchUsers(searchParams.get("searchText")).then(result => {
            setUsers(result.map((r) => {
                return {
                    name: r.username,
                    id: r.user_id,
                    usersAdded: []
                }}
            ))
        });
    }, [searchParams])



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