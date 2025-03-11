import React from "react";

const Footer = () => {
    return (
        <footer className="bg-gray-800 text-white py-4">
            <div className="container mx-auto px-4 text-center">
                <p className="text-sm">
                    Developed by{" "}
                    <a href="https://github.com/imdhruv99" target="_blank">
                        Dhruv Prajapati 👨🏻‍💻
                    </a>
                    &copy; {new Date().getFullYear()}
                </p>
            </div>
        </footer>
    );
};

export default Footer;
