import asyncio
import json
import random
from websockets import serve

class McpServer:
    def __init__(self):
        self.tools: dict[str, dict] = {}
        self.pending_requests: dict = {}

    def tool(self, name: str, description: str, input_schema: dict, callback):
        self.tools[name] = {
            "description": description,
            "input_schema": input_schema,
            "callback": callback,
        }

    async def handle_connection(self, websocket):
        print(f"New connection from {websocket.remote_address}")
        async for message in websocket:
            try:
                print(f"Received: {message}")
                data = json.loads(message)
                request_id = data.get("id")
                method = data.get("method")
                params = data.get("params", {})

                if method in self.tools:
                    result = await self.tools[method]["callback"](params)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"content": [{"text": result}]},
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Method '{method}' not found"},
                    }
                print(f"Sending: {json.dumps(response)}")
                await websocket.send(json.dumps(response))
            except Exception as e:
                print(f"Error handling request: {e}")

async def get_random_joke(params):
    jokes = [
        "Why do Java developers wear glasses? Because they don't C#.",
        "How many programmers does it take to change a light bulb? None. It's a hardware problem.",
        "A SQL query walks into a bar and sees two tables. It asks, 'Can I join you?'",
        "There are 10 kinds of people: those who understand binary and those who don't.",
    ]
    return random.choice(jokes)

async def main():
    server = McpServer()
    server.tool(
        name="get-joke",
        description="Return a random programming joke",
        input_schema={},
        callback=get_random_joke,
    )

    async with serve(server.handle_connection, "0.0.0.0", 8081):
        print("Jokes MCP running on ws://0.0.0.0:8081")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
