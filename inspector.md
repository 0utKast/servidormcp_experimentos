# Guía Detallada del Inspector MCP de fastMCP para Depuración y Conexión

## Introducción

El Inspector MCP de fastMCP es una herramienta invaluable para el desarrollo y depuración de servidores que implementan el Protocolo de Contexto de Modelo (MCP). Permite a los desarrolladores interactuar visualmente con sus servidores, inspeccionar sus capacidades y verificar su comportamiento en tiempo real. Esta guía detalla qué es el Inspector, cómo se utiliza para la depuración y el proceso exacto para conectarlo a tu servidor fastMCP.

## ¿Qué es el Inspector MCP?

El Inspector MCP es una **herramienta de desarrollo visual basada en web** que actúa como un proxy entre tu navegador y tu servidor fastMCP en ejecución. Su propósito principal es:

*   **Inspeccionar Servidores:** Permite ver una lista de todas las herramientas, recursos y prompts registrados en tu servidor MCP.
*   **Probar Interactivamente:** Ofrece una interfaz para ejecutar herramientas y leer recursos directamente desde el navegador, proporcionando argumentos y mostrando los resultados en tiempo real.
*   **Verificación Rápida:** Facilita la verificación de que las herramientas y recursos están definidos correctamente y se comportan como se espera, ofreciendo una retroalimentación rápida y depuración visual.
*   **Manejo de Tokens:** Para servidores que requieren autenticación, el Inspector genera un token de sesión y lo incluye en la URL, manejando la autenticación de forma transparente para el desarrollador durante la fase de depuración.

## Uso del Inspector para Depuración

Durante el desarrollo, el Inspector es una herramienta esencial para:

1.  **Validación de Esquemas:** Asegurarse de que los esquemas de entrada y salida de tus herramientas y recursos son correctos.
2.  **Pruebas Funcionales:** Ejecutar tus herramientas con diferentes entradas para verificar su lógica y el resultado que devuelven.
3.  **Observación del Protocolo:** Monitorear los mensajes de protocolo intercambiados entre el cliente (el Inspector) y el servidor, lo cual es útil para entender cómo interactúan.
4.  **Identificación de Errores:** Detectar rápidamente problemas en la implementación de tus herramientas o en la configuración del servidor.

## Cambios en `servidor_calculadora.py` (y por qué se revirtieron)

Inicialmente, al intentar habilitar la conexión del Inspector con autenticación, se consideró modificar directamente `servidor_calculadora.py` para incluir un `BearerAuthProvider` y configurar explícitamente el transporte HTTP en `mcp.run()`. La idea era que el servidor validara un token generado por el Inspector.

Sin embargo, tras consultar el documento `fastMCP.pdf` (Sección 5.1, "Depuración Visual con el MCP Inspector", página 21), se aclaró que el comando `fastmcp dev` está diseñado específicamente para este propósito de desarrollo y depuración. Este comando se encarga de:

*   Iniciar el servidor fastMCP en un proceso en segundo plano.
*   Configurar un servidor proxy.
*   Lanzar la aplicación web del Inspector.
*   Abrir automáticamente el Inspector en el navegador con el token de sesión ya incluido en la URL.

Debido a esta funcionalidad integrada de `fastmcp dev`, **los cambios realizados en `servidor_calculadora.py` para añadir `BearerAuthProvider` y configurar el transporte HTTP explícitamente fueron revertidos a su estado original.** El archivo `servidor_calculadora.py` ahora es un servidor fastMCP simple que, por defecto, se ejecutaría en modo `stdio` si se ejecutara directamente con `python servidor_calculadora.py`. Sin embargo, cuando se usa `fastmcp dev`, el CLI de fastMCP se encarga de ejecutarlo con el transporte HTTP necesario y de gestionar la comunicación con el Inspector.

Es importante destacar que, para despliegues en producción donde se requiere un transporte HTTP y autenticación robusta, la configuración de la autenticación (por ejemplo, con `BearerAuthProvider` o mediante un archivo `fastmcp.json`) y el transporte HTTP (`mcp.run(transport="http", ...)`) sí se configurarían explícitamente en el código del servidor o en su configuración de despliegue.

## Proceso de Conexión Detallado: Servidor y Inspector

Para conectar el Inspector MCP a tu servidor fastMCP y utilizarlo para depuración, debes ejecutar dos procesos distintos en terminales separadas.

### Paso 1: Iniciar tu Servidor FastMCP

Este proceso ejecuta tu código Python que define las herramientas y recursos de tu servidor.

*   **Acción:** Abre una **primera terminal externa** (fuera de tu IDE, como VS Code) y navega hasta el directorio raíz de tu proyecto (`C:\Videotutoriales\fastMCP\fastmcp_experimentos`).
*   **Comando a ejecutar:**
    ```bash
    fastmcp run servidor_calculadora.py:mcp --transport http --port 8080
    ```
*   **Resultado Esperado en la Terminal:**
    Verás una salida similar a la siguiente, indicando que el servidor se ha iniciado y está escuchando en el puerto 8080.
    ```
    INFO:     Started server process [XXXX]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
    ```
    **Es crucial entender que en esta terminal NO se mostrará ningún token.** El servidor simplemente está esperando conexiones HTTP. **Deja esta terminal abierta y el servidor ejecutándose.**

### Paso 2: Iniciar el Inspector MCP

Este proceso lanza la interfaz web del Inspector y genera el token de sesión necesario.

*   **Acción:** Abre una **segunda terminal externa, DIFERENTE** a la que usaste para el servidor. Asegúrate de estar también en el directorio raíz de tu proyecto.
*   **Comando a ejecutar:**
    ```bash
    npx @modelcontextprotocol/inspector
    ```
*   **Resultado Esperado en la Terminal:**
    El Inspector se iniciará. Verás una salida que incluirá una URL con un token de sesión. Por ejemplo:
    ```
    MCP Inspector running at: http://localhost:5173/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
    **Automáticamente, esta URL se abrirá en tu navegador web.**

### Paso 3: Verificación en el Navegador

*   **Resultado Esperado en el Navegador:**
    El navegador mostrará la interfaz del Inspector MCP. Si ambos procesos se están ejecutando correctamente y el Inspector se ha iniciado con la URL que contiene el token, deberías ver que el Inspector está **conectado a tu servidor FastMCP**. Podrás ver tus herramientas (como `add`) y recursos listados, y podrás interactuar con ellos. El token incluido en la URL es lo que permite que el Inspector se autentique con tu servidor y establezca la comunicación.

---

Siguiendo estos pasos, tendrás tu servidor fastMCP ejecutándose y el Inspector MCP conectado, listo para ayudarte en la depuración y prueba de tus herramientas.
