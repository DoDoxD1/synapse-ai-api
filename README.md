# 🧠 Synapse AI Backend

AI-powered exam preparation platform with spaced repetition, adaptive learning, and gamification.

## 🚀 Features

- **JWT Authentication** - Secure user authentication with access and refresh tokens
- **Spaced Repetition** - SM-2 algorithm for optimal learning retention
- **Adaptive Difficulty** - Dynamic question difficulty based on performance
- **AI-Powered Questions** - Generate questions using OpenAI GPT-4
- **Mock Tests** - Full-length practice tests with detailed analytics
- **Gamification** - XP system, levels, streaks, and achievements
- **Progress Analytics** - Comprehensive tracking and insights
- **Study Plans** - Personalized study schedules

## 📋 Tech Stack

- **Framework:** FastAPI 0.104+
- **Database:** PostgreSQL 15+ with SQLAlchemy (async)
- **Cache:** Redis 7+
- **AI:** OpenAI GPT-4 Turbo
- **Authentication:** JWT with python-jose
- **Migrations:** Alembic
- **Testing:** Pytest with async support

## 🛠️ Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone and setup virtual environment:**
```bash
cd synapse-backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run database migrations:**
```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

5. **Run the application:**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 🐳 Docker Setup

```bash
cd docker
docker-compose up -d
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔑 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update user profile
- `DELETE /api/v1/users/me` - Delete account

### Practice
- `GET /api/v1/practice/questions` - Get practice questions
- `POST /api/v1/practice/submit-answer` - Submit answer
- `GET /api/v1/practice/attempts` - Get attempt history

### Study Plan
- `POST /api/v1/study-plan/` - Create study plan
- `GET /api/v1/study-plan/active` - Get active plan
- `POST /api/v1/study-plan/sessions` - Start study session
- `POST /api/v1/study-plan/sessions/end` - End session

### Mock Tests
- `GET /api/v1/mock-tests/` - List mock tests
- `POST /api/v1/mock-tests/attempts` - Start test
- `POST /api/v1/mock-tests/attempts/submit` - Submit test

### Analytics
- `GET /api/v1/analytics/stats` - User statistics
- `GET /api/v1/analytics/progress` - Progress analytics
- `GET /api/v1/analytics/leaderboard` - Leaderboard

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_spaced_repetition.py
```

## 📦 Project Structure

```
synapse-backend/
├── alembic/              # Database migrations
├── app/
│   ├── ai/              # AI integration (OpenAI)
│   ├── algorithms/      # Spaced repetition, adaptive difficulty
│   ├── api/             # API endpoints
│   ├── core/            # Database, Redis, security
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access layer
│   ├── schemas/         # Pydantic schemas
│   ├── config.py        # Configuration
│   ├── dependencies.py  # Dependency injection
│   └── main.py          # FastAPI application
├── docker/              # Docker configuration
├── tests/               # Test suite
├── .env.example         # Example environment variables
├── requirements.txt     # Python dependencies
└── README.md
```

## 🔐 Environment Variables

See `.env.example` for all required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key
- `OPENAI_API_KEY` - OpenAI API key

## 🚀 Deployment

### Railway / Render

1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### Manual Deployment

```bash
# Build Docker image
docker build -f docker/Dockerfile -t synapse-backend .

# Run container
docker run -p 8000:8000 --env-file .env synapse-backend
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.
