Import asyncio
import websockets
import urllib.request
import json
import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
​async def handler(websocket):
async for message in websocket:
try:
req_data = json.loads(message)
user_input = req_data.get('message')
​url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
headers = {
'Content-Type': 'application/json',
'x-goog-api-key': GEMINI_API_KEY
}
data = {
"contents": [{"parts": [{"text": user_input}]}]
}
​req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
​with urllib.request.urlopen(req) as response:
res_data = json.loads(response.read().decode('utf-8'))
ai_response = res_data['candidates'][0]['content']['parts'][0]['text']
​await websocket.send(json.dumps({'response': ai_response}))
​except Exception as e:
print(f"Error: {e}")
await websocket.send(json.dumps({'response': 'Error connecting to AI'}))
​async def main():
async with websockets.serve(handler, "0.0.0.0", 8080):
await asyncio.Future()
if __name__ == "__main__":
    asyncio.run(main())
  
