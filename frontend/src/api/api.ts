import axios from "axios";

console.log(process.env.REACT_APP_SERVER_URL);

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

export async function signUp(email: string, userName: string, password: string): Promise<string> {
    const response = await api.post<{ message: string }>("/signup", {
        email,
        userName,
        password,
    });

    if (response.status !== 200) {
        throw new Error(response.data.message);
    }

    return response.data.message;
}

export async function signIn(
    email: string,
    password: string
): Promise<{
    email: string;
    username: string;
}> {
    const response = await api.post<{ email: string; username: string; error: string }>("/login", {
        email,
        password,
    });

    if (response.status !== 200) {
        throw new Error(response.data.error);
    }

    return {
        email: response.data.email,
        username: response.data.username,
    };
}
