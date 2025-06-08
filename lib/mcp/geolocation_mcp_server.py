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

async def get_location(params):
    ip = params.get("ip", "127.0.0.1")
    mapping = {
        "127.0.0.1": {"latitude": 37.7749, "longitude": -122.4194, "city": "San Francisco"}
    }
    loc = mapping.get(ip, {"latitude": 0.0, "longitude": 0.0, "city": "Unknown"})
    return json.dumps(loc)

async def main():
    server = McpServer()
    server.tool(
        name="get-location",
        description="Lookup approximate location for an IP address",
        input_schema={"ip": {"type": "string", "description": "IPv4 address"}},
        callback=get_location,
    )

    async with serve(server.handle_connection, "0.0.0.0", 8085):
        print("Geolocation MCP running on ws://0.0.0.0:8085")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
