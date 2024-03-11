import { useEffect, useState } from 'react';
import { TileList, SingleObject } from '../components/tileList';
import { useSearchParams } from 'react-router-dom';
import { searchRecipes, searchUsers } from '../api/api';


export default function SearchResultsPage() {
    const [showUsers, setShowUser] = useState<boolean>(false)
    const [users, setUsers] = useState<SingleObject[]>([])
    const [recipes, setRecipes] = useState<SingleObject[]>([])
    const [searchParams, setSearchParams] = useSearchParams()


    useEffect(() =>{
        searchRecipes(searchParams.get("searchText")).then(result => {
                setRecipes(result.map((r) => {
                    return {
                        name: r.name,
                        id: r.id,
                        link: r.link
                    }}
                ))
            }
        );
        searchUsers(searchParams.get("searchText")).then(result => {
            setUsers(result.map((r) => {
                return {
                    name: r.username,
                    id: r.user_id,
                    link: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
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