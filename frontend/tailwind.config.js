module.exports = {
    content: ["./src/**/*.{js,jsx,ts,tsx}"],
    theme: {
        extend: {
            boxShadow: {
                standard: "1px 1px 16px #F1F2F2",
                strong: "1px 1px 16px #e8e8e8",
            },
            colors: {
                "logo-red": "#CC444B",
            },
        },
    },
    plugins: [require("@tailwindcss/forms")],
};
