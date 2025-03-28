from fastapi import FastAPI
from database.database import engine, Base
from routes.user import router as user_router
from routes.auth import router as auth_router  # Ensure auth router is imported
from fastapi.middleware.cors import CORSMiddleware
from routes.fantasy_team import router as fantasy_team_router
from routes.fantasy_points import router as fantasy_points_router
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",  # Local dev
    "https://f1-fantasy-frontend.vercel.app"  # Your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Create DB tables
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)  # ✅ Include the auth router
app.include_router(user_router)  # ✅ Include the user router
app.include_router(fantasy_team_router)
app.include_router(fantasy_points_router)






@app.get("/")
def root():
    return {"message": "F1 Fantasy Backend is running 🚀"}
