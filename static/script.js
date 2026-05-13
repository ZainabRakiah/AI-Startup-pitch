const form = document.querySelector("form");
const textarea = document.querySelector("textarea");

if (form && textarea) {
    form.addEventListener("submit", (e) => {
        if (textarea.value.trim() === "") {
            e.preventDefault();
            alert("Please enter a startup idea.");
        }
    });
}
