import axios from "axios";

export const api = axios.create({
    baseURL: process.env.REACT_APP_SERVER_URL + "/api",
});

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
