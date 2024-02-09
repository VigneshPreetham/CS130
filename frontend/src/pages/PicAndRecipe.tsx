import logo from '../assets/logo.png'
import { useParams } from 'react-router-dom';

interface PicAndRecipePrps {
    exampleParam: string
}

interface PicAndRecipe {
    name: string,
    picture: string,
    recipe: string[]
}

let pizzaPocket: PicAndRecipe = {
    name: "Pizza Pocket",
    picture: "idk",
    recipe: ["Take out of box", "Microwave"]
}

export default function PicAndRecipe({exampleParam}: PicAndRecipePrps) {

    let { id } = useParams();

    return (
        <div className="h-screen w-screen flex justify-center bg-gray-50">
            <div className="bg-slate-200 border-2 items-center rounded-lg border-black w-3/4 h-fit h-rounded-lg flex flex-col m-5 lg:px-8">
                <div className = "m-2 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900"> {pizzaPocket.name} </div>
                <img src={logo} alt="test" className="m-4 w-[400px]"/>
                <div className="list-decimal m-2">
                    {pizzaPocket.recipe.map(line => <li> {line} </li>)}
                </div>
            </div>
        </div>
    )
}