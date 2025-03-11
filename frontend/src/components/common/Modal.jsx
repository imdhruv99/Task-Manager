import React, { useEffect } from "react";

const Modal = ({ title, children, onClose }) => {
    // Close modal when Escape key is pressed
    useEffect(() => {
        const handleEscapeKey = (e) => {
            if (e.key === "Escape") {
                onClose();
            }
        };

        document.addEventListener("keydown", handleEscapeKey);

        // Prevent scrolling of background content
        document.body.style.overflow = "hidden";

        return () => {
            document.removeEventListener("keydown", handleEscapeKey);
            document.body.style.overflow = "auto";
        };
    }, [onClose]);

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
                {/* Background overlay */}
                <div
                    className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
                    onClick={onClose}
                ></div>

                {/* Modal panel */}
                <div className="inline-block w-full max-w-md px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-white rounded-lg shadow-xl sm:my-8 sm:align-middle sm:p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-medium leading-6 text-gray-900">
                            {title}
                        </h3>
                        <button
                            type="button"
                            className="text-gray-400 hover:text-gray-500"
                            onClick={onClose}
                        >
                            <svg
                                className="w-6 h-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                        </button>
                    </div>
                    <div>{children}</div>
                </div>
            </div>
        </div>
    );
};

export default Modal;
