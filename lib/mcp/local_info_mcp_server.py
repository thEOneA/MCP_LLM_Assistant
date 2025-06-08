import asyncio
import json
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

async def find_nearby(params):
    location = params.get("location", "your area")
    category = params.get("category", "points of interest")
    suggestions = [
        f"Sample {category} A near {location}",
        f"Sample {category} B near {location}",
    ]
    return "\n".join(suggestions)

async def main():
    server = McpServer()
    server.tool(
        name="find-nearby",
        description="Suggest nearby restaurants, cafés, or landmarks",
        input_schema={
            "location": {"type": "string", "description": "City or coordinates"},
            "category": {"type": "string", "description": "Type of place"},
        },
        callback=find_nearby,
    )

    async with serve(server.handle_connection, "0.0.0.0", 8084):
        print("Local Info MCP running on ws://0.0.0.0:8084")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
