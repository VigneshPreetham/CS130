import { create } from "zustand";

interface UserStore {
    userName: string;
    loggedIn: boolean;
    login: (userName: string) => void;
    logout: () => void;
}

export const useUser = create<UserStore>((set) => ({
    userName: "",
    loggedIn: false,
    login: (userName: string) => set({ loggedIn: true, userName: userName }),
    logout: () => set({ loggedIn: false, userName: "" }),
}));
