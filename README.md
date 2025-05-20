# Prueba Técnica Bascosta

Este proyecto contiene una libreta de contactos con frontend en Vue y backend en Django. Usa Docker Compose para facilitar la ejecución.

## Requisitos

- Docker
- Docker Compose

## Ejecución

### 🔧 Pasos para ejecutar

1. **Clona el repositorio**

bash
[git clone https://github.com/tu-usuario/prueba_bascosta.git
cd prueba_bascosta](https://github.com/YoinerCamano/Prueba-Tecnica-Bascosta.git)

 Acceso a la aplicación
🔸 Frontend: http://localhost:5173
🔹 Backend API: http://localhost:8000/api/contactos/

Estructura del Repositorio
.
├── backend/                  # Proyecto Django
│── Dockerfile.backend
├── frontend/                 # Proyecto Vue
│── Dockerfile.frontend
├── docker-compose.yml        # Orquestación de servicios
└── README.md                 # Este archivo

Imágenes Docker disponibles
Puedes usar directamente las imágenes subidas en Docker Hub:

🐍 Backend: docker pull yoicam/prueba_bascosta_backend

🌐 Frontend: docker pull yoicam/prueba_bascosta_frontend

Yoine Camaño
Docker Hub: yoicam

