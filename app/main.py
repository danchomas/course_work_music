from fastapi import FastAPI
from routers.user_routers import router as user_router
import uvicorn

app = FastAPI(
    title="Resonance Music App",
    descriprion="Music App for new artists",
)

app.include_router(user_router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)