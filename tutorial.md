# Tutorial: Creando tu Primer Servidor de IA con fastMCP

## 1. Introducción: El Nuevo Ecosistema de Agentes de IA

En el panorama actual de la inteligencia artificial, los Grandes Modelos de Lenguaje (LLMs) como Gemini son increíblemente potentes, pero tienen una limitación fundamental: operan en un vacío, sin acceso directo al mundo exterior. No pueden leer tus archivos locales, consultar una base de datos en tiempo real o interactuar con APIs de terceros de forma nativa.

Para solucionar esto, ha surgido el **Protocolo de Contexto de Modelo (MCP)**. La mejor forma de entender MCP es pensar en él como un **"puerto USB-C para la IA"**. Así como el USB-C unificó el caos de cables y conectores, MCP busca estandarizar la forma en que los agentes de IA (clientes) se comunican de manera segura y predecible con herramientas y fuentes de datos externas (servidores).

Esto permite que cualquier herramienta (un servidor MCP) pueda "enchufarse" a cualquier agente de IA, fomentando un ecosistema de herramientas reutilizables y modulares.

## 2. ¿Qué es fastMCP?

Si MCP es el estándar (el "qué"), **fastMCP es la implementación de referencia en Python (el "cómo")**.

`fastMCP` es un framework de alto rendimiento que nos permite construir servidores MCP de una forma increíblemente sencilla y "Pythónica". Su propuesta de valor es abstraer toda la complejidad del protocolo (gestión de conexiones, serialización de datos, errores, etc.) para que los desarrolladores podamos centrarnos exclusivamente en la lógica de negocio de nuestras herramientas.

Esto lo logra a través de una API muy elegante basada en decoradores. A menudo, basta con añadir `@mcp.tool` a una función de Python normal para exponerla de forma segura a un agente de IA.

## 3. Tutorial Práctico: Servidor Calculadora

Vamos a construir un servidor MCP canónico: una simple calculadora. Este ejercicio demuestra la simplicidad y elegancia de `fastmcp`.

### Paso 3.1: Configuración del Entorno

1.  **Requisitos**: Python 3.10+ y `uv` (`pip install uv`).
2.  **Entorno Virtual**: `uv venv`
3.  **Activación**: `.venv\Scripts\activate` (Windows) o `source .venv/bin/activate` (macOS/Linux).
4.  **Instalación**: `uv pip install "fastmcp"`

### Paso 3.2: Creación del Código del Servidor

Crea un archivo llamado `servidor_calculadora.py`:

```python
from fastmcp import FastMCP

# 1. Instanciar el servidor con un nombre descriptivo.
mcp = FastMCP("ServidorCalculadora 🧮")

# 2. Definir una herramienta usando el decorador @mcp.tool.
@mcp.tool
def add(a: int, b: int) -> int:
    """Suma dos números enteros y devuelve el resultado."""
    print(f"Ejecutando add({a}, {b})")
    return a + b
```

### Paso 3.3: Ejecución del Servidor

Para que nuestro servidor sea accesible a través de la red para otros programas, lo iniciamos en modo HTTP. Abre una terminal y ejecuta:

```sh
fastmcp run servidor_calculadora.py:mcp --transport http --port 8080
```

El servidor se quedará escuchando peticiones en el puerto 8080.

### Paso 3.4: Creación de un Cliente para Probar el Servidor

Ahora, ¿cómo interactuamos con él? Creamos un script `cliente_prueba.py` que se conectará y usará la herramienta `add`.

```python
import asyncio
from fastmcp import Client

async def main():
    # La URL correcta debe incluir la ruta /mcp/
    server_url = "http://127.0.0.1:8080/mcp/"
    print(f"Conectando al servidor en {server_url}...")

    try:
        async with Client(server_url) as client:
            print("¡Conexión exitosa!")
            
            tools = await client.list_tools()
            print(f"Herramientas disponibles: {[tool.name for tool in tools]}")

            print(f"\nLlamando a la herramienta 'add' con a=5, b=7...")
            # La forma correcta: un diccionario como segundo argumento posicional
            result = await client.call_tool("add", {"a": 5, "b": 7})
            
            print(f"Resultado obtenido: {result.content}")

    except Exception as e:
        print(f"\nOcurrió un error al interactuar con el servidor: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

Al ejecutar `python cliente_prueba.py` en una segunda terminal, verás cómo se conecta al servidor y recibe el resultado `12`.

## 4. Anexo: Depuración y Errores Comunes

Durante nuestro desarrollo, aprendimos varias lecciones importantes:

*   **La sintaxis de `call_tool` es precisa**: Los argumentos de la herramienta deben agruparse en un **único diccionario** como segundo argumento: `client.call_tool("add", {"a": 5, "b": 7})`.
*   **La URL del cliente necesita la ruta `/mcp/`**: Al conectarse, el cliente debe apuntar a la ruta base del protocolo: `http://127.0.0.1:8080/mcp/`.
*   **El modo `dev` es para depuración**: El comando `fastmcp dev` es una herramienta fantástica que lanza el **MCP Inspector**, pero protege la conexión con un token de seguridad, lo que dificulta la conexión de clientes externos. Para la interacción programática, es mejor usar `fastmcp run`.

```