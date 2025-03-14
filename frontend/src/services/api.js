import axios from "axios";

// Create axios instance
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api/v1",
});

// Error handling interceptor
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error("API Error:", error.response || error);
        return Promise.reject(error);
    }
);

// Task API calls
export const getTasks = async () => {
    const response = await apiClient.get("/tasks");
    return response.data;
};

export const getTask = async (id) => {
    const response = await apiClient.get(`/tasks/${id}`);
    return response.data;
};

export const createTask = async (taskData) => {
    const response = await apiClient.post("/tasks", taskData, {
        headers: {
            "Content-Type": "application/json",
        },
    });
    return response.data;
};

export const updateTask = async (id, taskData) => {
    const response = await apiClient.put(`/tasks/${id}`, taskData, {
        headers: {
            "Content-Type": "application/json",
        },
    });
    return response.data;
};

export const deleteTask = async (id) => {
    const response = await apiClient.delete(`/tasks/${id}`);
    return response.data;
};
