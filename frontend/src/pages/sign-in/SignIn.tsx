import { useState } from "react";
import React from 'react';
import { signIn } from "../../api/api";

export default function SignInPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();

        try {
            const user = await signIn(email, password);
        } catch (error) {
            if (error instanceof Error) {
                setErrorMessage(error.message);
            } else {
                setErrorMessage("An error occurred. Please try again later.");
            }
        }
    }

    return (
        <div className="flex items-center justify-center w-screen h-screen bg-gray-50">
            <div className="bg-white w-[500px] rounded-lg flex flex-col px-6 py-20 lg:px-8 shadow-standard">
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                    <h2 className="text-2xl font-bold leading-9 tracking-tight text-center text-gray-900">Sign in to your account</h2>
                </div>
                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    id="email"
                                    name="email"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-logo-red sm:text-sm sm:leading-6"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                                    Password
                                </label>
                            </div>
                            <div className="mt-2">
                                <input
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="current-password"
                                    required
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-logo-red sm:text-sm sm:leading-6"
                                />
                            </div>
                        </div>

                        <div className="flex flex-col items-center gap-2">
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-logo-red px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-logo-red"
                            >
                                Sign in
                            </button>
                            {errorMessage !== "" && <span className="self-center text-red-500">{errorMessage}</span>}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
