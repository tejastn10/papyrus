<p align="center">
  <img src="logo.svg" alt="Papyrus Logo" height="160" />
</p>

# Papyrus 📄

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-009688?logo=fastapi&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7+-646CFF?logo=vite&logoColor=white)
![React](https://img.shields.io/badge/React-19+-61DAFB?logo=react&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative&logoColor=white)

**Papyrus** is a lightweight and secure PDF management tool that helps you seamlessly **add or remove passwords** from PDF files. Built with a blazing-fast frontend using **React + Vite** and a high-performance **FastAPI** backend, Papyrus ensures privacy and ease of use — right from your browser.

---

## ✨ Features

- 🔐 **Add Password**: Secure your PDF files with a password in just one click.
- 🔓 **Remove Password**: Strip password protection from encrypted PDF files.
- ⚡ **Fast & Lightweight**: Optimized for speed with Vite + React and FastAPI.
- 🛡️ **No File Storage**: All files are processed in memory — nothing is stored on disk.
- 🎯 **User-Friendly UI**: Simple drag-and-drop interface for quick interaction.

---

## 🚀 Getting Started

### 📦 Prerequisites

Ensure you have the following installed:

- **Node.js**: v22 or later
- **Python**: v3.11 or later
- **Poetry**: for managing Python dependencies
- **Docker** (optional, for containerized setup)

---

### 🧪 Local Development

#### Backend (FastAPI)

```bash
# Navigate to backend folder
cd backend

# Install dependencies
poetry install

# Start FastAPI server
poetry run uvicorn app.main:app --reload --port 5000
````

Server will be available at: [http://localhost:5000/docs](http://localhost:5000/docs)

#### Frontend (Vite + React)

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: [http://localhost:3000](http://localhost:3000)

---

### 🐳 Using Docker (Optional)

```bash
docker-compose up --build
```

This starts both the FastAPI backend and React frontend.

---

## 📂 Project Structure

```bash
papyrus/
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── utils/             # Common utility functions
│   │   ├── models/            # Models
│   │   ├── config/            # Settings, config
│   │   ├── services/          # PDF encryption/decryption logic
│   │   ├── middleware/        # Middleware
│   │   └── main.py            # App entry point
│   ├── tests/                 # Backend unit tests
│   ├── pyproject.toml         # Poetry config
│   └── Dockerfile             # Backend Docker setup
│
├── frontend/                  # React + Vite frontend
│   ├── src/                   # Main app code
│   ├── public/                # Static assets
│   ├── vite.config.ts         # Vite configuration
│   └── Dockerfile             # Frontend Docker setup
│
├── compose.yml         # Multi-service Docker config
└── README.md                  # You're here!
```

---

## 📘 API Documentation

Swagger docs are auto-generated and available at:

```bash
http://localhost:5000/docs
```

---

## ⚖️ License

This project is licensed under the [MIT License](./LICENSE.md).

---

## 🙌 Acknowledgments

- Powered by [FastAPI](https://fastapi.tiangolo.com) and [React](https://react.dev)
- PDF operations handled by [PyPDF2](https://pypdf2.readthedocs.io/)
- UI inspired by minimal productivity apps like CleanShot and Arc Browser.

---

Built with 💙 by Tejas.
