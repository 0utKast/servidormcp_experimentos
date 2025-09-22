
from fastmcp import FastMCP

# 1. Instanciar el servidor con un nombre descriptivo.
mcp = FastMCP("ServidorCalculadora 🧮")

# 2. Definir una herramienta usando el decorador @mcp.tool.
@mcp.tool
def add(a: int, b: int) -> int:
    """Suma dos números enteros y devuelve el resultado."""
    print(f"Ejecutando add({a}, {b})")
    return a + b

# 3. (Opcional pero recomendado) Bloque para ejecutar el servidor directamente.
if __name__ == "__main__":
    print("Iniciando servidor FastMCP en modo stdio por defecto...")
    mcp.run()
