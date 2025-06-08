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

async def schedule_meeting(params):
    event = params.get("event", "meeting")
    date = params.get("date", "unspecified date")
    time = params.get("time", "unspecified time")
    return f"Scheduled {event} on {date} at {time}."

async def main():
    server = McpServer()
    server.tool(
        name="schedule-meeting",
        description="Schedule or reschedule a meeting",
        input_schema={
            "event": {"type": "string", "description": "Event title"},
            "date": {"type": "string", "description": "Date of event"},
            "time": {"type": "string", "description": "Time of event"},
        },
        callback=schedule_meeting,
    )

    async with serve(server.handle_connection, "0.0.0.0", 8082):
        print("Calendar MCP running on ws://0.0.0.0:8082")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
