import React, { useState, useEffect } from "react";
import Modal from "../common/Modal";
import { createTask, updateTask } from "../../services/api";
import toast from "react-hot-toast";

const TaskForm = ({ task, onClose }) => {
    const isEditing = !!task;

    const [formData, setFormData] = useState({
        title: "",
        description: "",
        status: "todo",
        priority: "medium",
        due_date: "",
    });

    const [isSubmitting, setIsSubmitting] = useState(false);

    // If editing, populate the form with task data
    useEffect(() => {
        if (task) {
            setFormData({
                title: task.title,
                description: task.description || "",
                status: task.status,
                priority: task.priority,
                due_date: task.due_date
                    ? new Date(task.due_date).toISOString().split("T")[0]
                    : "",
            });
        }
    }, [task]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validation
        if (!formData.title.trim()) {
            toast.error("Title is required");
            return;
        }

        try {
            setIsSubmitting(true);

            let formattedDueDate = null;
            if (formData.due_date) {
                const date = new Date(formData.due_date);
                formattedDueDate = new Date(
                    date.setHours(0, 0, 0, 0)
                ).toISOString();
            }

            const data = {
                ...formData,
                due_date: formattedDueDate,
            };

            if (isEditing) {
                await updateTask(task.id, data);
                toast.success("Task updated successfully");
            } else {
                await createTask(data);
                toast.success("Task created successfully");
            }

            // Close the form and refresh the task list
            onClose();
        } catch (error) {
            console.error("Error saving task:", error);
            toast.error(
                isEditing ? "Failed to update task" : "Failed to create task"
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Modal
            title={isEditing ? "Edit Task" : "Create New Task"}
            onClose={onClose}
        >
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label
                        htmlFor="title"
                        className="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Title <span className="text-red-500">*</span>
                    </label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>

                <div>
                    <label
                        htmlFor="description"
                        className="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Description
                    </label>
                    <textarea
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        rows="3"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    ></textarea>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label
                            htmlFor="status"
                            className="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Status
                        </label>
                        <select
                            id="status"
                            name="status"
                            value={formData.status}
                            onChange={handleChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="todo">To Do</option>
                            <option value="in_progress">In Progress</option>
                            <option value="done">Done</option>
                        </select>
                    </div>

                    <div>
                        <label
                            htmlFor="priority"
                            className="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Priority
                        </label>
                        <select
                            id="priority"
                            name="priority"
                            value={formData.priority}
                            onChange={handleChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label
                        htmlFor="due_date"
                        className="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Due Date
                    </label>
                    <input
                        type="date"
                        id="due_date"
                        name="due_date"
                        value={formData.due_date}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <div className="flex justify-end space-x-3 pt-2">
                    <button
                        type="button"
                        onClick={onClose}
                        className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                        disabled={isSubmitting}
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors disabled:opacity-50"
                        disabled={isSubmitting}
                    >
                        {isSubmitting
                            ? "Saving..."
                            : isEditing
                            ? "Update Task"
                            : "Create Task"}
                    </button>
                </div>
            </form>
        </Modal>
    );
};

export default TaskForm;
