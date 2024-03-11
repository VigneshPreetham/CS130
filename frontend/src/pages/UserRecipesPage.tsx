import { useEffect, useState } from 'react';
import logo from '../assets/logo.png'
import { TileList, SingleObject } from '../components/tileList';
import { getRecipes, getUserName } from '../api/api';
import { useParams } from 'react-router-dom';

// 'f650444e-1154-49f6-94aa-6a1acfdc0ae7';


export default function UserRecipesPage() {

    const [recipes, setRecipes] = useState<SingleObject[]>([]);
    const [username, setUsername] = useState<string>("USERNAME")
    const { id } = useParams();

    useEffect(() =>{
        const userId = id == undefined ? "" : id
        getUserName(userId).then(r => setUsername(r))
        getRecipes(userId).then(result => {
                setRecipes(result.map((r) => {
                    return {
                        name: r.name,
                        id: r.id,
                        link: r.link
                    }}
                ))
            }
        );
    }, [])


    return (
        <div>
            <div className="m-4 font-bold text-center text-logo-red text-2xl">{username}'s Recipes</div>
            <TileList isUser={false} toList={recipes}/>
        </div>
    )
}