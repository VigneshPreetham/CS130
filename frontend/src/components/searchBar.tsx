import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
  

export default function SearchBar() {

    const [searchVal, setSearchVal] = useState<string>('');
    const navigate = useNavigate()

    function search(event: any, searchText: string){
        event.preventDefault()
        navigate({
            pathname: '/results',
            search: '?searchText=' + searchText
        })
    }

  return (<>
  <form onSubmit={(e) => {search(e, searchVal)}}>
        <input 
            className="h-full rounded mx-1 border-logo-red"
            onChange={e => setSearchVal(e.target.value)}
        />
    </form>
    <button onClick={(e) => {search(e, searchVal)}}>
        <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            strokeWidth={1.5} 
            className="w-6 h-6 mx-1 stroke-logo-red">
            <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
            />
        </svg>
    </button>
</>)
}
  