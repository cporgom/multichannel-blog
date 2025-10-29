### 🧭 Metodología de Desarrollo: Kanban Híbrido

Para gestionar el desarrollo de MultiChannel Blog (Twitch/YouTube) en Python, se ha elegido una metodología ágil: **Kanban Híbrido**.

#### 1. Justificación
Dada la naturaleza del proyecto, que requiere múltiples integraciones y pruebas incrementales (primero OAuth de Twitch, luego OAuth de YouTube, luego la interfaz), un enfoque que priorice el flujo continuo de trabajo es el más eficiente.

#### 2. Funcionamiento
* **Fases del Flujo:** El proyecto se gestionará a través de un tablero con las siguientes fases claras:
    * `To Do (Por Hacer)`: Tareas pendientes y requisitos de la API.
    * `In Progress (En Progreso)`: Tareas que se están desarrollando **actualmente**.
    * `Testing (Pruebas)`: Tareas con código implementado, esperando ser probadas (ej. probar el *refresh token*).
    * `Done (Terminado)`: Funcionalidad implementada, probada y lista para el *deploy*.
* **WIP Limit (Límite de Trabajo en Curso):** Se establecerá un límite de **3 tareas** en la fase *In Progress* para asegurar la concentración y finalizar el código antes de empezar nuevos desarrollos.