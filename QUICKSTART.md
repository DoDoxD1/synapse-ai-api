# 🚀 Synapse AI Backend - Quick Start

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.11+ installed
- ✅ PostgreSQL 15+ installed and running
- ✅ Redis 7+ installed and running
- ✅ OpenAI API key (get from https://platform.openai.com)

## Step-by-Step Setup (5 minutes)

### Step 1: Activate Virtual Environment
```bash
cd synapse-backend
venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create Environment File
```bash
# Option A: Interactive setup (Recommended)
python scripts/create_env.py

# Option B: Manual copy
cp .env.example .env
# Then edit .env with your settings
```

**Required in .env:**
```env
SECRET_KEY=your-generated-secret-key
DATABASE_URL=postgresql+asyncpg://synapse:password@localhost:5432/synapse_db
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-openai-key-here
```

### Step 4: Create Database
```bash
# In PostgreSQL, create the database
# psql -U postgres
# CREATE DATABASE synapse_db;
```

### Step 5: Run Migrations
```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

### Step 6: Start the Server
```bash
uvicorn app.main:app --reload
```

**Server running at:** http://localhost:8000

## 🧪 Test the API

### 1. Visit Interactive Docs
Open: http://localhost:8000/docs

### 2. Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User",
    "exam_type": "GRE"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

Copy the `access_token` from the response.

### 4. Get User Profile
```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## 🐳 Docker Quick Start (Alternative)

If you prefer Docker:

```bash
cd docker
docker-compose up -d
```

This starts:
- FastAPI application on port 8000
- PostgreSQL on port 5432
- Redis on port 6379

## 📊 Database Schema

The following tables will be created:
- `users` - User accounts
- `topics` - Subject topics
- `user_topic_mastery` - User progress per topic
- `questions` - Question bank
- `question_attempts` - User answers
- `study_sessions` - Study tracking
- `study_plans` - Personalized plans
- `mock_tests` - Practice tests
- `mock_test_attempts` - Test results
- `user_stats` - Gamification stats
- `user_achievements` - Badges & rewards

## 🔧 Common Issues & Solutions

### Issue: "alembic: command not found"
```bash
pip install alembic
```

### Issue: Database connection error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `psql -l`

### Issue: Redis connection error
- Ensure Redis is running
- Windows: Download from https://github.com/microsoftarchive/redis/releases
- Test with: `redis-cli ping` (should return PONG)

### Issue: OpenAI API error
- Verify your API key is correct in .env
- Check you have credits: https://platform.openai.com/usage

## 📱 API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register new user |
| `/api/v1/auth/login` | POST | Login user |
| `/api/v1/users/me` | GET | Get user profile |
| `/api/v1/practice/questions` | GET | Get practice questions |
| `/api/v1/practice/submit-answer` | POST | Submit answer |
| `/api/v1/study-plan/` | POST | Create study plan |
| `/api/v1/mock-tests/` | GET | List mock tests |
| `/api/v1/analytics/stats` | GET | User statistics |
| `/api/v1/analytics/leaderboard` | GET | Leaderboard |

## 🎯 What's Next?

1. **Explore API:** Visit http://localhost:8000/docs
2. **Test Endpoints:** Use the interactive Swagger UI
3. **Add Sample Data:** Create topics and questions
4. **Test Features:** Try practice sessions, mock tests
5. **Customize:** Modify endpoints for your needs

## 📚 Documentation

- **Full API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Implementation Details:** See IMPLEMENTATION_SUMMARY.md
- **Main README:** See README.md

## 🆘 Need Help?

- Check logs in the terminal
- Review .env configuration
- Ensure all services are running
- Check PostgreSQL and Redis status

---

**Ready to build amazing exam prep experiences! 🚀**
