# ⚙️ Service Exchange App (The Backend Part)

This repository holds the code for the server-side part of the Service Exchange App.

---

## 🛠️ Tech Stack: Python & Django

| Category                | What I Used                        | Why I Used It (Simple Reason)                                                                    |
| :---------------------- | :--------------------------------- | :----------------------------------------------------------------------------------------------- |
| **Main Framework**      | **Django**                         | A full-featured Python framework to handle the whole server.                                     |
| **APIs**                | **Django REST Framework (DRF)**    | Helps quickly build API endpoints that the frontend can talk to.                                 |
| **Real-time Chat**      | **Django Channels**                | Extends Django to handle WebSockets, which allows to talk to frontend in real-time               |
| **Static Files**        | **Whitenoise**                     | Makes it easy to serve CSS, JavaScript, and other static files, especially in production.        |
| **Cloud Storage**       | **Cloudinary**                     | Used to securely store user-uploaded files on cloud                                              |
| **Auth (Signup/Login)** | **Django All-Auth & Google OAuth** | Manages standard email/password login and lets users sign in easily using their Google accounts. |
| **User Sessions**       | **JWT (JSON Web Tokens)**          | It lets the frontend securely store the user's session, keeping the backend lightweight.         |
| **Database (Dev)**      | **SQLite**                         | Simple database used locally while developing the app.                                           |
| **Database (Prod)**     | **MySQL**                          | A powerful and scalable database used for the final, live version of the app.                    |
| **Mailing System**      | **Brevo**                          | Makes it easy to send emails to the users                                                        |

---

## Note

This is the repository for the backend code, you can find the code for frontend here: https://github.com/KaberaSamuel/tradetalent-app-frontend
