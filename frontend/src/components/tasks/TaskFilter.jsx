import React from "react";

const TaskFilter = ({ filter, setFilter }) => {
    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilter((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    return (
        <div className="bg-white rounded-md shadow p-4 mb-6">
            <h2 className="text-lg font-medium text-gray-800 mb-3">
                Filter Tasks
            </h2>
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
                        value={filter.status}
                        onChange={handleFilterChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="all">All Statuses</option>
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
                        value={filter.priority}
                        onChange={handleFilterChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="all">All Priorities</option>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
            </div>
        </div>
    );
};

export default TaskFilter;
