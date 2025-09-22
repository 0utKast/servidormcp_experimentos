import asyncio
import os
from fastmcp import Client

async def main():
    server_url = "http://127.0.0.1:8080/mcp/"
    print(f"Conectando al servidor en {server_url}...")

    try:
        async with Client(server_url) as client:
            print("¡Conexión exitosa!")
            
            is_alive = await client.ping()
            print(f"Servidor vivo: {is_alive}")

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