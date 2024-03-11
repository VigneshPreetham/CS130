import { create } from "zustand";
import { persist } from "zustand/middleware";

interface UserStore {
    userName: string;
    email: string;
    userId: string;
    loggedIn: boolean;
    login: (userName: string, email: string, userId: string) => void;
    logout: () => void;
}

export const useUser = create<UserStore>()(
    persist(
        (set) => ({
            userName: "",
            email: "",
            userId: "",
            loggedIn: false,
            login: (userName: string, email: string, userId: string) => set({ loggedIn: true, userName, email, userId }),
            logout: () => set({ loggedIn: false, userName: "" }),
        }),
        {
            name: "user-store", // unique name for localStorage key
        }
    )
);