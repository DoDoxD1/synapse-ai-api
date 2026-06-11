from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sentry_sdk

from app.config import settings
from app.core.database import init_db, close_db
from app.core.redis import init_redis, close_redis
from app.api.v1 import auth, users, practice, study_plan, analytics, mock_tests


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    await init_db()
    await init_redis()
    
    if settings.SENTRY_DSN:
        sentry_sdk.init(dsn=settings.SENTRY_DSN, environment=settings.ENVIRONMENT)
    
    yield
    
    # Shutdown
    await close_db()
    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    description="""🧠 **Synapse AI Backend API**
    
    AI-powered exam preparation platform with advanced features:
    
    * 🔐 **JWT Authentication** - Secure user authentication with refresh tokens
    * 📚 **Spaced Repetition** - SM-2 algorithm for optimal learning
    * 🎯 **Adaptive Difficulty** - Dynamic question difficulty based on performance
    * 🤖 **AI-Powered Questions** - GPT-4 generated practice questions
    * 📊 **Mock Tests** - Full-length practice exams with analytics
    * 🏆 **Gamification** - XP, levels, streaks, and leaderboards
    * 📈 **Analytics** - Comprehensive progress tracking
    
    ## Authentication
    
    Most endpoints require authentication. To authenticate:
    1. Register a user with `POST /api/v1/auth/register`
    2. Login with `POST /api/v1/auth/login` to get tokens
    3. Click 'Authorize' button and paste your `access_token`
    4. All protected endpoints will now work
    
    ## Rate Limiting
    
    - 60 requests per minute
    - 1000 requests per hour
    
    ## Support
    
    - Documentation: See README.md and API_DOCUMENTATION.md
    - Interactive Docs: /docs (you are here!)
    - Alternative Docs: /redoc
    """,
    version="1.0.0",
    contact={
        "name": "Synapse AI Team",
        "email": "support@synapseai.com",
    },
    license_info={
        "name": "MIT License",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Authentication endpoints - register, login, token refresh"
        },
        {
            "name": "users",
            "description": "User profile management"
        },
        {
            "name": "practice",
            "description": "Practice questions with adaptive difficulty and answer submission"
        },
        {
            "name": "study-plan",
            "description": "Study plan creation and session tracking"
        },
        {
            "name": "analytics",
            "description": "User statistics, progress analytics, and leaderboards"
        },
        {
            "name": "mock-tests",
            "description": "Full-length mock tests with detailed analysis"
        },
    ]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["users"])
app.include_router(practice.router, prefix=f"{settings.API_V1_PREFIX}/practice", tags=["practice"])
app.include_router(study_plan.router, prefix=f"{settings.API_V1_PREFIX}/study-plan", tags=["study-plan"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["analytics"])
app.include_router(mock_tests.router, prefix=f"{settings.API_V1_PREFIX}/mock-tests", tags=["mock-tests"])


@app.get("/")
async def root():
    return {
        "message": "Synapse AI API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
