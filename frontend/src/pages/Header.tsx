import { useState } from "react";

import { useUser } from "../hooks/useUser";
import { Fragment } from "react";
import { Menu, Transition } from "@headlessui/react";

import logo from "../assets/logo.png";
import { Link } from "react-router-dom";

function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(" ");
}

function Dropdown() {
    const { userId, logout } = useUser();

    return (
        <Menu as="div" className="relative inline-block text-left">
            <div>
                <Menu.Button className="flex justify-center items-center">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        className="m-1 w-6 h-6 stroke-logo-red cursor-pointer"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                        />
                    </svg>
                </Menu.Button>
            </div>

            <Transition
                as={Fragment}
                enter="transition ease-out duration-100"
                enterFrom="transform opacity-0 scale-95"
                enterTo="transform opacity-100 scale-100"
                leave="transition ease-in duration-75"
                leaveFrom="transform opacity-100 scale-100"
                leaveTo="transform opacity-0 scale-95"
            >
                <Menu.Items className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div className="py-1">
                        <Menu.Item>
                            {({ active }) => (
                                <Link
                                    to={`/user/${userId}/recipes`}
                                    className={classNames(active ? "bg-gray-100 text-gray-900" : "text-gray-700", "block px-4 py-2 text-sm")}
                                >
                                    Profile
                                </Link>
                            )}
                        </Menu.Item>
                        <Menu.Item>
                            {({ active }) => (
                                <span
                                    className={classNames(
                                        active ? "bg-gray-100 text-gray-900" : "text-gray-700",
                                        "cursor-pointer block px-4 py-2 text-sm"
                                    )}
                                    onClick={logout}
                                >
                                    Log out
                                </span>
                            )}
                        </Menu.Item>
                    </div>
                </Menu.Items>
            </Transition>
        </Menu>
    );
}

export default function Header() {
    const { loggedIn } = useUser();

    const [showDropdown, setShowDropdown] = useState(false);

    return (
        <div className="w-full flex justify-between my-3 place-items-center px-5">
            <div className="LEFT flex">
                <img className="h-7 w-8 m-1" src={logo} alt="chef-hat" />
                <span className="font-bold text-logo-red text-2xl">Taste Buds</span>
            </div>
            {loggedIn && (
                <div className="RIGHT flex gap-5">
                    <div className="flex place-items-center">
                        <input className="h-full rounded mx-1 border-logo-red"></input>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={1.5}
                            className="w-6 h-6 mx-1 stroke-logo-red"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                            />
                        </svg>
                    </div>
                    <Dropdown />
                </div>
            )}
        </div>
    );
}
