import React from "react";
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import TaskList from "./components/tasks/TaskList";
import TaskFilter from "./components/tasks/TaskFilter";
import TaskForm from "./components/tasks/TaskForm";
import { useState } from "react";

function App() {
    const [showTaskForm, setShowTaskForm] = useState(false);
    const [editingTask, setEditingTask] = useState(null);
    const [filter, setFilter] = useState({ status: "all", priority: "all" });

    const handleAddTask = () => {
        setEditingTask(null);
        setShowTaskForm(true);
    };

    const handleEditTask = (task) => {
        setEditingTask(task);
        setShowTaskForm(true);
    };

    const handleCloseForm = () => {
        setShowTaskForm(false);
        setEditingTask(null);
    };

    return (
        <div className="min-h-screen flex flex-col bg-gray-50">
            <Header />
            <main className="flex-grow container mx-auto px-4 py-8">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-bold text-gray-800">
                        Task Management
                    </h1>
                    <button
                        onClick={handleAddTask}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
                    >
                        Add New Task
                    </button>
                </div>

                <TaskFilter filter={filter} setFilter={setFilter} />

                <TaskList filter={filter} onEditTask={handleEditTask} />

                {showTaskForm && (
                    <TaskForm task={editingTask} onClose={handleCloseForm} />
                )}
            </main>
            <Footer />
        </div>
    );
}

export default App;
