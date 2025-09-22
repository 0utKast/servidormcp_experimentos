
# Experimentos con fastMCP - Documentación de la Fase 1

Este documento resume los pasos y lecciones aprendidas durante la fase inicial de experimentación con `fastmcp`.

## Resumen del Proceso

Se implementó un servidor básico (`servidor_calculadora.py`) con una herramienta para sumar dos números. También se creó un cliente en Python (`cliente_prueba.py`) para interactuar con dicho servidor a través de HTTP.

### 1. Configuración del Entorno

1.  **Requisitos previos**: Python 3.10+ y `uv` (`pip install uv`).
2.  **Crear entorno virtual**: `uv venv`
3.  **Activar entorno**: `.venv\Scripts\activate` (Windows) o `source .venv/bin/activate` (macOS/Linux).
4.  **Instalar dependencias**: `uv pip install "fastmcp"`

### 2. Ejecución

1.  **Iniciar el Servidor**: `fastmcp run servidor_calculadora.py:mcp --transport http --port 8080`
2.  **Ejecutar el Cliente**: `python cliente_prueba.py` (en otra terminal).

---

## 💡 Lecciones Aprendidas y Puntos Clave

Esta sección documenta los problemas encontrados y sus soluciones.

1.  **`curl` en PowerShell**: `curl` es un alias de `Invoke-WebRequest` y tiene una sintaxis diferente. Es más fiable usar `Invoke-WebRequest` directamente o el `curl.exe` de Git.

2.  **Modo `dev` vs. `run`**: 
    *   `fastmcp dev` es para depuración, inicia un proxy y requiere un **token de autenticación** que lo hace incompatible con clientes externos sencillos.
    *   `fastmcp run` inicia el servidor directamente y es el modo adecuado para la interacción programática.

3.  **Sintaxis de `client.call_tool`**: La forma correcta de llamar a una herramienta es pasando sus argumentos en un **único diccionario** como segundo argumento posicional.
    *   **CORRECTO**: `client.call_tool("add", {"a": 5, "b": 7})`
    *   **INCORRECTO**: `client.call_tool("add", input={"a": 5, "b": 7})`
    *   **INCORRECTO**: `client.call_tool("add", a=5, b=7)`

4.  **URL del Cliente**: El cliente de `fastmcp` debe apuntar a la ruta base del protocolo, que por defecto es `/mcp/`.
    *   **CORRECTO**: `http://127.0.0.1:8080/mcp/`
    *   **INCORRECTO**: `http://127.0.0.1:8080`
