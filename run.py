import contextlib
from fastapi import FastAPI
from weather_server import mcp_app
import os


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_app.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/weather", mcp_app.streamable_http_app())

@app.get("/health")
def health():
    return {"status": "ok"}

PORT = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
