# 📦 EXPROOF - Sistema de Control de Inventario y Gestión de Activos

Este sistema tiene como propósito la gestión eficiente de inventarios y activos, implementado con una arquitectura moderna y escalable.
- **Backend**: Construido con **FastAPI** (Python) y **PostgreSQL**.
- **Frontend**: Desarrollado en **React Native** con **Expo**, siguiendo una **Feature-Based Architecture**.

## Requisitos Previos

Para ejecutar este proyecto, necesitas tener instaladas las siguientes herramientas:

- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL** (o Docker para correr la base de datos)
- **Expo Go** (opcional, para probar en dispositivo móvil)

## Configuración y Ejecución del Backend (FastAPI)

Sigue estos pasos para levantar el servidor backend:

1.  **Navegar a la carpeta del backend:**
    ```bash
    cd backend
    ```

2.  **Crear y activar el entorno virtual:**
    - En Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
    - En macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Copia el archivo de ejemplo `.env.example` a un nuevo archivo llamado `.env` y configura los valores necesarios (Base de datos, `SECRET_KEY`, etc.).
    ```bash
    cp .env.example .env
    ```

5.  **Ejecutar migraciones de base de datos:**
    ```bash
    alembic upgrade head
    ```

6.  **Crear Super Admin (Script semilla):**
    ```bash
    python -m app.db.seed
    ```

7.  **Levantar el servidor de desarrollo:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    El servidor estará corriendo en `http://localhost:8000`.

## Configuración y Ejecución del Frontend (React Native / Expo)

Sigue estos pasos para iniciar la aplicación móvil:

1.  **Navegar a la carpeta del frontend:**
    ```bash
    cd frontend
    ```

2.  **Instalar dependencias:**
    ```bash
    npm install
    ```

3.  **Configurar conexión al Backend:**
    Asegúrate de configurar la IP local de tu máquina en `src/shared/api/api.ts` o en el archivo `.env` correspondiente para que el dispositivo móvil pueda comunicarse con el backend (por ejemplo, usar la IP de tu red local `192.168.x.x` en lugar de `localhost` si pruebas en un dispositivo físico).

4.  **Levantar la aplicación:**
    ```bash
    npx expo start
    ```

5.  **Abrir la aplicación:**
    - **En Web**: Presiona la tecla `w` en la terminal.
    - **En Móvil**: Escanea el código QR que aparece en la terminal usando la aplicación **Expo Go** (Android/iOS).

## Pruebas (Testing)

### Backend
Para ejecutar las pruebas unitarias del backend:
```bash
cd backend
pytest
```

### Frontend
Para ejecutar las pruebas del frontend:
```bash
cd frontend
npm test
```

## Credenciales por Defecto (Entorno de Desarrollo)

El script semilla (`python -m app.db.seed`) crea un usuario Super Administrador con las siguientes credenciales:

- **Usuario:** `admin@empresa.com`
- **Contraseña:** `AdminSystem_2024!`
