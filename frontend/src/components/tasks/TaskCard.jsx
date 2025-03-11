import React from "react";
import { format } from "date-fns";

const TaskCard = ({ task, onEdit, onDelete }) => {
    const { id, title, description, status, priority, due_date, created_at } =
        task;

    // Format dates
    const formattedDueDate = due_date
        ? format(new Date(due_date), "MMM dd, yyyy")
        : "No due date";
    const formattedCreatedDate = format(new Date(created_at), "MMM dd, yyyy");

    // Status badge styling
    const statusClass = `status-${status} text-xs font-medium px-2.5 py-0.5 rounded-full`;

    return (
        <div
            className={`task-card priority-${priority} bg-white rounded-md shadow p-4 mb-4`}
        >
            <div className="flex justify-between items-start">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                    {title}
                </h3>
                <div className="flex space-x-2">
                    <button
                        onClick={() => onEdit(task)}
                        className="text-blue-600 hover:text-blue-800"
                    >
                        <svg
                            className="w-5 h-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                            />
                        </svg>
                    </button>
                    <button
                        onClick={() => onDelete(id)}
                        className="text-red-600 hover:text-red-800"
                    >
                        <svg
                            className="w-5 h-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                            />
                        </svg>
                    </button>
                </div>
            </div>

            {description && (
                <p className="text-gray-600 text-sm mb-3">{description}</p>
            )}

            <div className="flex flex-wrap items-center gap-2 mt-2">
                <span className={statusClass}>{status.replace("_", " ")}</span>
                <span className="text-xs text-gray-500">
                    Priority:{" "}
                    <span className="font-medium capitalize">{priority}</span>
                </span>
                <span className="text-xs text-gray-500">
                    Due: <span className="font-medium">{formattedDueDate}</span>
                </span>
            </div>

            <div className="text-xs text-gray-400 mt-3">
                Created: {formattedCreatedDate}
            </div>
        </div>
    );
};

export default TaskCard;
