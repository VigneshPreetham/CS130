import axios from "axios";
import { SingleObject } from "../components/tileList";

export const api = axios.create({
    baseURL: process.env.REACT_APP_SERVER_URL + "/api",
});

export interface dbRecipe {
    created_by : string,
    created_on : string,
    id : string,
    link: string,
    name: string,
    recipe : string
}

export interface dbUser {
    email: string,
    username: string,
    recipes: dbRecipe[],
    user_id: string
}

export async function getUserName(userId: string) : Promise<string> {
    const response = await api.get<{ recipes: dbRecipe[], username: string }>(
        "/user_info", 
        {params: {"user_id": userId}}
    )

    if (response.status !== 200) {
        throw new Error(response.statusText);
    }
    return response.data.username;
}

export async function getRecipes(userId: string) : Promise<dbRecipe[]> {
    const response = await api.get<{ recipes: dbRecipe[], username: string }>(
        "/user_info", 
        {params: {"user_id": userId}}
    )
    
    if (response.status !== 200) {
        throw new Error(response.statusText);
    }
    return response.data.recipes;
}

export async function getRecipe(recipeId: string) : Promise<dbRecipe> {
    const response = await api.get<{
        recipe_id: string,
        name: string,
        recipe: string,
        link: string,
        created_by: string
    }>(
        "/recipe_info", 
        {params: {"recipe_id": recipeId}}
    )
    
    if (response.status !== 200) {
        throw new Error(response.statusText);
    }

    return {
        created_by : response.data.created_by,
        created_on : "",
        id : response.data.recipe_id,
        link: response.data.link,
        name: response.data.name,
        recipe : response.data.recipe
    };
}

export async function addRecipeToUser(userId: string, recipeId: string) : Promise<string> {
    const response = await api.post<{ message: string }>(
        "/add_recipe", 
        {params: {
            "user_id": userId, 
            "recipe_id": recipeId
        }}
    )
    if (response.status !== 200) {
        throw new Error(response.data.message);
    }
    return response.data.message;
}

export async function searchRecipes(searchText: (string|null)) : Promise<dbRecipe[]>{
    const response = await api.get<{ recipes: dbRecipe[]}>(
        "/search_recipe", 
        {params: {"recipe": searchText}}
    )
    
    if (response.status !== 200) {
        throw new Error(response.statusText);
    }
    return response.data.recipes;
}

export async function searchUsers(searchText: (string|null)) : Promise<dbUser[]>{
    const response = await api.get<{ users: dbUser[]}>(
        "/search_username", 
        {params: {"username": searchText}}
    )
    
    if (response.status !== 200) {
        throw new Error(response.statusText);
    }
    return response.data.users;
}


export async function uploadImage(file: File): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post<{ message: string }>("/upload", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    if (response.status !== 200) {
        throw new Error(response.data.message);
    }

    return response.data.message;
}

type SignUpResponse = {
    email: string;
    user_id: string;
    username: string;
    recipes: string[];
    error: string;
};

export async function signUp(email: string, userName: string, password: string): Promise<SignUpResponse> {
    const response = await api
        .post<SignUpResponse>(
            "/signup",
            JSON.stringify({
                email,
                username: userName,
                password,
            }),
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
        .catch((error) => error.response);

    console.log(response);

    if (response.data.error) {
        throw new Error(response.data.error);
    }

    return response.data;
}

type SignInResponse = {
    email: string;
    user_id: string;
    username: string;
    recipes: string[];
    error: string;
};

export async function signIn(email: string, password: string): Promise<SignInResponse> {
    const response = await api
        .post<SignInResponse>(
            "/login",
            JSON.stringify({
                email,
                password,
            }),
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
        .catch((error) => error.response);

    if (response.data.error) {
        throw new Error(response.data.error);
    }

    return response.data;
}
