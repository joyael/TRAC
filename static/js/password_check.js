document.addEventListener("DOMContentLoaded", function () {
    let n=0;
    document.getElementById("id_hashed_password").addEventListener("input", function () {
        n=n+1;
        console.log(`Entered Input ${n} times`);
        const password = this.value;

        // Conditions
        const conditions = [
            { id: "min-length", regex: /.{8,}/ },
            { id: "uppercase", regex: /[A-Z]/ },
            { id: "lowercase", regex: /[a-z]/ },
            { id: "number", regex: /\d/ },
            { id: "special-char", regex: /[!@#$%^&*(),.?":{}|<>]/ }
        ];

        conditions.forEach(({ id, regex }) => {
            const element = document.getElementById(id);
            if (regex.test(password)) {
                element.classList.remove("invalid");
                element.classList.add("valid");
            } else {
                element.classList.remove("valid");
                element.classList.add("invalid");
            }
        });
    });
});