const platforms = [
    { name: "Instagram", url: "https://www.instagram.com/", icon: "fa-instagram" },
    { name: "Facebook", url: "https://www.facebook.com/", icon: "fa-facebook" },
    { name: "YouTube", url: "https://www.youtube.com/c/", icon: "fa-youtube" },
    { name: "GitHub", url: "https://github.com/", icon: "fa-github" },
    { name: "LinkedIn", url: "https://www.linkedin.com/in/", icon: "fa-linkedin" },
    { name: "Twitter", url: "https://twitter.com/", icon: "fa-twitter" }
];

document.getElementById("searchBtn").addEventListener("click", () => {
    const username = document.getElementById("usernameInput").value.trim();
    const resultArea = document.getElementById("resultArea");
    resultArea.innerHTML = ""; // Temizle

    if (username === "") {
        resultArea.innerHTML = "<p>Please enter a username</p>";
        return;
    }

    platforms.forEach(platform => {
        const profileUrl = platform.url + username;
        const resultItem = document.createElement("div");
        resultItem.classList.add("result-item");

        // Kullanıcı adını kontrol etmek için iframe (örn. fetch) yerine linkler gösteriyoruz
        resultItem.innerHTML = `
            <i class="fa ${platform.icon}"></i> 
            <a href="${profileUrl}" target="_blank">${platform.name} Profiline Git</a>
        `;
        resultArea.appendChild(resultItem);
    });
});