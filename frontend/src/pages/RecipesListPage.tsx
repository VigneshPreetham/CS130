import logo from '../assets/logo.png'
import { Link } from "react-router-dom";


interface SingleRecipeProps {
    index: Number,
    name: string,
    id: string,
}

interface SingleRecipe {
    name: string,
    id: string,
}


const navigateToRecipe = (id: string) => {

}

export function SingleRecipe({index, name, id}: SingleRecipeProps){
    return (
        <div>
            <div className="flex w-full justify-center my-3">
                <div className="flex place-items-center w-1/2 h-20 bg-slate-200 rounded-md border-2 border-black" >
                    <div className='p-5 text-lg font-bold'>{index.toString()}.</div>
                    <img src={logo} alt="test" className='h-full p-5'/>
                    <Link to={'/recipe/'+id} className='p-5 font-bold'> {name} </Link>
                </div>
            </div>
        </div>
    )
}

let recipes: SingleRecipe[] = [
    {id: "1", name: "Pizza"},
    {id: "2", name: "Pasta"},
    {id: "3", name: "Gourmet Salad"},
    {id: "4", name: "Human Flesh"},
    
]


export default function RecipesListPage() {
    return (
        <div>
            <div className="m-4 font-bold text-center text-logo-red text-2xl">USERNAME's Recipes</div>
            <div>
                {recipes.map((recipe, i) => 
                    <SingleRecipe index={i+1} name={recipe.name} id={recipe.id}/>
                )}
            </div>
        </div>
    )
}