<p align="center">
  <img src="https://github.com/cporgom/multichannel-blog/blob/main/multichannel-logo.png?raw=true" alt="Logo Multichannel Blog" width="200" />
</p>

# MultiChannel Blog

#### Todos los videos que te interesan en un solo lugar.

---

## Concepto

MultiChannel Blog es un agregador de contenido web diseñado para unificar las suscripciones de un usuario de **YouTube** y los canales seguidos de **Twitch** en un único *feed* cronológico.

El usuario inicia sesión con ambas plataformas (vía OAuth 2.0) y la aplicación se encarga de obtener el contenido nuevo de todos sus canales, permitiéndole al usuario ver todos los vídeos y clips recientes en una sola página, con opciones de filtrado y ordenamiento.

---

## Stack Tecnológico

Este proyecto se construye con las siguientes tecnologías:

* **Backend:** Python
* **Framework Web:** Flask
* **Motor de Plantillas:** Jinja2 (Para la interfaz)
* **Autenticación:** OAuth 2.0 (APIs de Google/YouTube y Twitch)
* **Base de Datos (ORM):** SQLAlchemy
* **Base de Datos (Driver):** SQLite (Para persistencia de tokens)

---

## Cómo Activar el Servidor (Instalación Local)

Para ejecutar este proyecto en tu máquina local, sigue estos pasos:

### 1. Prerrequisitos
* Tener [Git](https://git-scm.com/) instalado.
* Tener [Python 3.10+](https://www.python.org/downloads/) instalado.

### 2. Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/cporgom/multichannel-blog.git](https://github.com/cporgom/multichannel-blog.git)
    cd multichannel-blog
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuración de Credenciales (¡Muy Importante!)

Este proyecto no funcionará sin las claves de API de Google y Twitch.

1.  **Crea un archivo `.env`** en la raíz del proyecto.
2.  **Copia y pega** la siguiente estructura en tu archivo `.env` y rellénala con tus propias claves (obtenidas de las consolas de desarrollador de Google y Twitch):

    ```ini
    # .env
    
    # Credenciales de Google/YouTube
    GOOGLE_CLIENT_ID="TU_ID_CLIENTE_DE_GOOGLE"
    GOOGLE_CLIENT_SECRET="TU_SECRETO_DE_GOOGLE"
    
    # Credenciales de Twitch
    TWITCH_CLIENT_ID="TU_ID_CLIENTE_DE_TWITCH"
    TWITCH_CLIENT_SECRET="TU_SECRETO_DE_TWITCH"
    
    # URL de tu servidor Flask (para el callback)
    REDIRECT_URI="[http://127.0.0.1:5000](http://127.0.0.1:5000)"
    
    # Clave secreta de Flask (para sesiones)
    SECRET_KEY="PON_UNA_CADENA_ALEATORIA_MUY_LARGA_AQUI"
    ```

### 4. Ejecutar el Servidor

Una vez instalado y configurado, arranca el servidor de Flask:

```bash
python app.py
