import logo from "../assets/logo.png";

export default function Header() {
    return (
        <div className="w-full flex my-3 place-items-center mx-5">
            <img className="h-7 w-8 m-1" src={logo} alt="chef-hat" />
            <span className="font-bold text-logo-red text-2xl">Taste Buds</span>
            <div className="absolute right-5 mx-10 flex place-items-center">
                <input className="h-full rounded mx-1 border-logo-red"></input>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} className="w-6 h-6 mx-1 stroke-logo-red">
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                    />
                </svg>
            </div>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                className="absolute right-5 m-1 w-6 h-6 stroke-logo-red"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                />
            </svg>
        </div>
    );
}
