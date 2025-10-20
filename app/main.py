from fastapi import FastAPI
from routers.track_routers import router as tracks_router
from routers.user_routers import router as user_router
from routers.profile_routers import router as profile_router
import uvicorn

app = FastAPI(
    title="Резонанс - Музыкальное Приложение",
    description="Музыкальное приложение для новых артистов",
)

app.include_router(tracks_router, prefix="/tracks", tags=["tracks"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(profile_router, prefix="/profiles", tags=["profiles"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
