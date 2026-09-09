"use strict";

/*
 * Central frontend configuration.
 *
 * If frontend and backend are deployed separately,
 * change API_BASE_URL to the deployed backend URL.
 */
const API_BASE_URL = "http://127.0.0.1:5000";

const TOKEN_KEY = "student_portal_token";
const STUDENT_KEY = "student_portal_student";


/* ---------------------------------------------------------
 * Authentication state
 * --------------------------------------------------------- */

function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function setAuthState(token, student) {
    localStorage.setItem(TOKEN_KEY, token);

    if (student) {
        localStorage.setItem(
            STUDENT_KEY,
            JSON.stringify(student)
        );
    }
}

function clearAuthState() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(STUDENT_KEY);
}

function getStoredStudent() {
    const student = localStorage.getItem(STUDENT_KEY);

    if (!student) {
        return null;
    }

    try {
        return JSON.parse(student);
    } catch {
        return null;
    }
}


/* ---------------------------------------------------------
 * API helper
 * --------------------------------------------------------- */

async function apiRequest(endpoint, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,
            headers
        }
    );

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = {
            success: false,
            message: "Server returned an invalid response."
        };
    }

    if (!response.ok) {
        const error = new Error(
            data.message || "Request failed."
        );

        error.status = response.status;
        error.data = data;

        throw error;
    }

    return data;
}


/* ---------------------------------------------------------
 * Alert framework
 * --------------------------------------------------------- */

function showAlert(element, message, type = "error") {
    if (!element) {
        return;
    }

    element.textContent = message;
    element.className = `alert show ${type}`;
}

function hideAlert(element) {
    if (!element) {
        return;
    }

    element.textContent = "";
    element.className = "alert";
}


/* ---------------------------------------------------------
 * Loading state
 * --------------------------------------------------------- */

function setButtonLoading(button, loading, loadingText = "Please wait...") {
    if (!button) {
        return;
    }

    if (loading) {
        button.dataset.originalText = button.textContent;
        button.textContent = loadingText;
        button.disabled = true;
    } else {
        button.textContent =
            button.dataset.originalText || button.textContent;

        button.disabled = false;
    }
}


/* ---------------------------------------------------------
 * Register
 * --------------------------------------------------------- */

async function handleRegister(event) {
    event.preventDefault();

    const form = event.currentTarget;

    const alertBox = document.getElementById("alert");
    const button = form.querySelector("button[type='submit']");

    hideAlert(alertBox);

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const confirmPassword =
        document.getElementById("confirm-password").value;

    if (password !== confirmPassword) {
        showAlert(
            alertBox,
            "Passwords do not match."
        );
        return;
    }

    setButtonLoading(button, true, "Creating account...");

    try {
        const data = await apiRequest(
            "/register",
            {
                method: "POST",
                body: JSON.stringify({
                    name,
                    email,
                    password
                })
            }
        );

        showAlert(
            alertBox,
            data.message || "Registration successful.",
            "success"
        );

        form.reset();

        setTimeout(() => {
            window.location.href = "login.html";
        }, 1200);

    } catch (error) {
        showAlert(
            alertBox,
            error.data?.message || "Registration failed."
        );
    } finally {
        setButtonLoading(button, false);
    }
}


/* ---------------------------------------------------------
 * Login
 * --------------------------------------------------------- */

async function handleLogin(event) {
    event.preventDefault();

    const form = event.currentTarget;

    const alertBox = document.getElementById("alert");
    const button = form.querySelector("button[type='submit']");

    hideAlert(alertBox);

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    setButtonLoading(button, true, "Signing in...");

    try {
        const data = await apiRequest(
            "/login",
            {
                method: "POST",
                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        setAuthState(
            data.token,
            data.student
        );

        window.location.href = "dashboard.html";

    } catch (error) {
        showAlert(
            alertBox,
            error.data?.message || "Login failed."
        );
    } finally {
        setButtonLoading(button, false);
    }
}


/* ---------------------------------------------------------
 * Forget password
 * --------------------------------------------------------- */

async function handleForgetPassword(event) {
    event.preventDefault();

    const form = event.currentTarget;

    const alertBox = document.getElementById("alert");
    const button = form.querySelector("button[type='submit']");

    hideAlert(alertBox);

    const email = document.getElementById("email").value.trim();

    setButtonLoading(
        button,
        true,
        "Processing..."
    );

    try {
        const data = await apiRequest(
            "/forget-password",
            {
                method: "POST",
                body: JSON.stringify({
                    email
                })
            }
        );

        showAlert(
            alertBox,
            data.message,
            "success"
        );

        form.reset();

    } catch (error) {
        showAlert(
            alertBox,
            error.data?.message || "Request failed."
        );
    } finally {
        setButtonLoading(button, false);
    }
}


/* ---------------------------------------------------------
 * Dashboard
 * --------------------------------------------------------- */

async function loadDashboard() {
    const token = getToken();

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const loading = document.getElementById("loading");
    const content = document.getElementById("dashboard-content");

    try {
        const data = await apiRequest(
            "/dashboard",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const student = data.student;

        document.getElementById("student-name").textContent =
            student.name || "-";

        document.getElementById("student-email").textContent =
            student.email || "-";

        document.getElementById("student-id").textContent =
            student.student_id || "-";

        document.getElementById("created-at").textContent =
            student.created_at || "-";

        document.getElementById("account-status").textContent =
            student.is_active ? "Active" : "Inactive";

        if (loading) {
            loading.style.display = "none";
        }

        if (content) {
            content.style.display = "block";
        }

    } catch (error) {
        clearAuthState();

        if (error.status === 401) {
            window.location.href = "login.html";
            return;
        }

        if (loading) {
            loading.textContent =
                error.data?.message ||
                "Unable to load dashboard.";
        }
    }
}


/* ---------------------------------------------------------
 * Logout
 * --------------------------------------------------------- */

function logout() {
    clearAuthState();
    window.location.href = "login.html";
}


/* ---------------------------------------------------------
 * Page initialization
 * --------------------------------------------------------- */

document.addEventListener("DOMContentLoaded", () => {

    const registerForm =
        document.getElementById("register-form");

    const loginForm =
        document.getElementById("login-form");

    const forgetPasswordForm =
        document.getElementById("forget-password-form");

    const logoutButton =
        document.getElementById("logout-button");

    if (registerForm) {
        registerForm.addEventListener(
            "submit",
            handleRegister
        );
    }

    if (loginForm) {
        loginForm.addEventListener(
            "submit",
            handleLogin
        );
    }

    if (forgetPasswordForm) {
        forgetPasswordForm.addEventListener(
            "submit",
            handleForgetPassword
        );
    }

    if (logoutButton) {
        logoutButton.addEventListener(
            "click",
            logout
        );
    }
});


window.addEventListener("load", () => {
    if (
        window.location.pathname.endsWith(
            "dashboard.html"
        )
    ) {
        loadDashboard();
    }
});