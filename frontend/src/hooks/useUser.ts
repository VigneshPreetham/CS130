import { create } from "zustand";

interface UserStore {
    userName: string;
    email: string;
    userId: string;
    loggedIn: boolean;
    login: (userName: string, email: string, userId: string) => void;
    logout: () => void;
}

export const useUser = create<UserStore>((set) => ({
    userName: "",
    email: "",
    userId: "",
    loggedIn: false,
    login: (userName: string, email: string, userId: string) => set({ loggedIn: true, userName, email, userId }),
    logout: () => set({ loggedIn: false, userName: "" }),
}));
