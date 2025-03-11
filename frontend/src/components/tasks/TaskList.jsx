import React, { useState, useEffect } from "react";
import TaskCard from "./TaskCard";
import Loader from "../common/Loader";
import { getTasks, deleteTask } from "../../services/api";
import toast from "react-hot-toast";

const TaskList = ({ filter, onEditTask }) => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);

    // Fetch tasks
    const fetchTasks = async () => {
        try {
            setLoading(true);
            const data = await getTasks();
            setTasks(data);
        } catch (error) {
            console.error("Error fetching tasks:", error);
            toast.error("Failed to load tasks");
        } finally {
            setLoading(false);
        }
    };

    // Load tasks on mount and when filter changes
    useEffect(() => {
        fetchTasks();
    }, []);

    // Handle task deletion
    const handleDeleteTask = async (id) => {
        if (window.confirm("Are you sure you want to delete this task?")) {
            try {
                await deleteTask(id);
                toast.success("Task deleted successfully");
                fetchTasks(); // Refresh the list
            } catch (error) {
                console.error("Error deleting task:", error);
                toast.error("Failed to delete task");
            }
        }
    };

    // Filter tasks based on current filter
    const filteredTasks = tasks.filter((task) => {
        // Filter by status
        if (filter.status !== "all" && task.status !== filter.status) {
            return false;
        }

        // Filter by priority
        if (filter.priority !== "all" && task.priority !== filter.priority) {
            return false;
        }

        return true;
    });

    if (loading) {
        return <Loader />;
    }

    if (filteredTasks.length === 0) {
        return (
            <div className="text-center py-10">
                <p className="text-gray-500">
                    No tasks found. Add a new task to get started.
                </p>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredTasks.map((task) => (
                <TaskCard
                    key={task.id}
                    task={task}
                    onEdit={onEditTask}
                    onDelete={handleDeleteTask}
                />
            ))}
        </div>
    );
};

export default TaskList;
