console.log("linking")
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = cookie.substring(name.length + 1);
            }
        }
    }
    return cookieValue;
}

async function apiFetch(url, options = {}) {
    const defaultOptions = {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }
    };

    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    return fetch(url, finalOptions);
}
const form = document.getElementById("shorten-form");
function copyToClipboard(url) {
    navigator.clipboard.writeText(url)
        .then(() => {
            const btn = document.getElementById("copy");
            btn.classList.add("copy");
            btn.innerHTML = "Copied!";
        })
        .catch(err => {
            console.error("Failed to copy: ", err);
        });
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    document.getElementById("result").innerHTML = "Processing your request";
    const url = document.getElementById("url").value;

    const response = await apiFetch("/api/shorten/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ original_url: url })
    });

    const data = await response.json();

    if (data.short_url) {
        document.getElementById("result").innerHTML = `
            <a href="${data.short_url}" target="_blank">${data.short_url}</a>
            <button id="copy" onclick="copyToClipboard('${data.short_url}')">Copy</button>
            <button onclick="window.open('${data.short_url}', '_blank')">
            Go to Website
            </button>

        `;
    } else {
        document.getElementById("result").innerText =
            "Error shortening URL (Enter a valid URL, example -> URL should start with http/https)";
    }
});