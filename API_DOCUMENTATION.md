# 📘 Synapse AI Backend - Complete API Documentation

**Base URL:** `http://localhost:8000`  
**API Version:** v1  
**API Prefix:** `/api/v1`

## 🔐 Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 📍 API Endpoints

### Authentication Endpoints

#### 1. Register User
**Endpoint:** `POST /api/v1/auth/register`  
**Authentication:** None  
**Description:** Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "exam_type": "GRE",
  "target_score": 320,
  "exam_date": "2026-12-31"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "exam_type": "GRE",
  "target_score": 320,
  "exam_date": "2026-12-31",
  "created_at": "2026-06-11T10:00:00",
  "last_active": "2026-06-11T10:00:00",
  "is_active": true,
  "is_verified": false
}
```

**Error Responses:**
- `409 Conflict` - Email already registered
- `422 Unprocessable Entity` - Validation error

---

#### 2. Login User
**Endpoint:** `POST /api/v1/auth/login`  
**Authentication:** None  
**Description:** Login and receive access/refresh tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect email or password
- `403 Forbidden` - Inactive user account

---

#### 3. Refresh Access Token
**Endpoint:** `POST /api/v1/auth/refresh`  
**Authentication:** None  
**Description:** Get new access token using refresh token

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### User Management Endpoints

#### 4. Get Current User Profile
**Endpoint:** `GET /api/v1/users/me`  
**Authentication:** Required  
**Description:** Get authenticated user's profile

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "exam_type": "GRE",
  "target_score": 320,
  "exam_date": "2026-12-31",
  "created_at": "2026-06-11T10:00:00",
  "last_active": "2026-06-11T10:00:00",
  "is_active": true,
  "is_verified": false
}
```

---

#### 5. Update User Profile
**Endpoint:** `PUT /api/v1/users/me`  
**Authentication:** Required  
**Description:** Update user profile information

**Request Body:**
```json
{
  "full_name": "John Smith",
  "exam_type": "GATE",
  "target_score": 700,
  "exam_date": "2027-01-15"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Smith",
  "exam_type": "GATE",
  "target_score": 700,
  "exam_date": "2027-01-15",
  "created_at": "2026-06-11T10:00:00",
  "last_active": "2026-06-11T10:00:00",
  "is_active": true,
  "is_verified": false
}
```

---

#### 6. Delete User Account
**Endpoint:** `DELETE /api/v1/users/me`  
**Authentication:** Required  
**Description:** Soft delete user account (deactivate)

**Response:** `204 No Content`

---

### Practice Endpoints

#### 7. Get Practice Questions
**Endpoint:** `GET /api/v1/practice/questions`  
**Authentication:** Required  
**Description:** Get practice questions for a topic with adaptive difficulty

**Query Parameters:**
- `topic_id` (required): UUID of the topic
- `count` (optional): Number of questions (1-50, default: 10)
- `difficulty` (optional): "easy", "medium", or "hard" (auto if not provided)

**Example Request:**
```
GET /api/v1/practice/questions?topic_id=550e8400-e29b-41d4-a716-446655440000&count=5
```

**Response:** `200 OK`
```json
[
  {
    "id": "650e8400-e29b-41d4-a716-446655440001",
    "topic_id": "550e8400-e29b-41d4-a716-446655440000",
    "question_text": "What is the capital of France?",
    "question_type": "mcq",
    "options": {
      "A": "London",
      "B": "Paris",
      "C": "Berlin",
      "D": "Madrid"
    },
    "difficulty": "easy",
    "tags": ["geography", "europe"]
  }
]
```

---

#### 8. Submit Answer
**Endpoint:** `POST /api/v1/practice/submit-answer`  
**Authentication:** Required  
**Description:** Submit answer for a question and receive feedback

**Request Body:**
```json
{
  "question_id": "650e8400-e29b-41d4-a716-446655440001",
  "answer": "B",
  "time_taken_seconds": 45
}
```

**Response:** `200 OK`
```json
{
  "is_correct": true,
  "correct_answer": "B",
  "explanation": "Paris is the capital and largest city of France.",
  "xp_earned": 10
}
```

---

#### 9. Get Question Attempts History
**Endpoint:** `GET /api/v1/practice/attempts`  
**Authentication:** Required  
**Description:** Get user's question attempt history

**Query Parameters:**
- `limit` (optional): Number of attempts to return (1-200, default: 50)

**Response:** `200 OK`
```json
[
  {
    "id": "750e8400-e29b-41d4-a716-446655440002",
    "question_id": "650e8400-e29b-41d4-a716-446655440001",
    "user_answer": "B",
    "is_correct": true,
    "time_taken_seconds": 45,
    "attempted_at": "2026-06-11T10:30:00",
    "explanation": "Paris is the capital..."
  }
]
```

---

### Study Plan Endpoints

#### 10. Create Study Plan
**Endpoint:** `POST /api/v1/study-plan/`  
**Authentication:** Required  
**Description:** Create a new personalized study plan

**Request Body:**
```json
{
  "start_date": "2026-06-15T00:00:00",
  "end_date": "2026-12-31T23:59:59",
  "daily_hours": 3.0,
  "target_topics": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440001"
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": "850e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "plan_name": "Study Plan (2026-06-15)",
  "start_date": "2026-06-15T00:00:00",
  "end_date": "2026-12-31T23:59:59",
  "daily_hours": 3.0,
  "is_active": true,
  "generated_at": "2026-06-11T10:00:00",
  "plan_data": {
    "total_days": 199,
    "total_hours": 597,
    "target_topics": ["550e8400-...", "550e8400-..."]
  }
}
```

---

#### 11. Get Active Study Plan
**Endpoint:** `GET /api/v1/study-plan/active`  
**Authentication:** Required  
**Description:** Get user's currently active study plan

**Response:** `200 OK`
```json
{
  "id": "850e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "plan_name": "Study Plan (2026-06-15)",
  "start_date": "2026-06-15T00:00:00",
  "end_date": "2026-12-31T23:59:59",
  "daily_hours": 3.0,
  "is_active": true,
  "generated_at": "2026-06-11T10:00:00",
  "plan_data": {...}
}
```

**Error Responses:**
- `404 Not Found` - No active study plan

---

#### 12. Start Study Session
**Endpoint:** `POST /api/v1/study-plan/sessions`  
**Authentication:** Required  
**Description:** Start a new study session

**Request Body:**
```json
{
  "topic_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_type": "practice"
}
```

**Session Types:** `practice`, `review`, `mock_test`, `tutoring`

**Response:** `201 Created`
```json
{
  "id": "950e8400-e29b-41d4-a716-446655440004",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "topic_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_type": "practice",
  "start_time": "2026-06-11T10:00:00",
  "end_time": null,
  "duration_minutes": null,
  "questions_attempted": 0,
  "correct_answers": 0,
  "xp_earned": 0
}
```

---

#### 13. End Study Session
**Endpoint:** `POST /api/v1/study-plan/sessions/end`  
**Authentication:** Required  
**Description:** End an active study session

**Request Body:**
```json
{
  "session_id": "950e8400-e29b-41d4-a716-446655440004"
}
```

**Response:** `200 OK`
```json
{
  "id": "950e8400-e29b-41d4-a716-446655440004",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "topic_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_type": "practice",
  "start_time": "2026-06-11T10:00:00",
  "end_time": "2026-06-11T11:30:00",
  "duration_minutes": 90,
  "questions_attempted": 25,
  "correct_answers": 20,
  "xp_earned": 250
}
```

---

#### 14. Get Study Sessions History
**Endpoint:** `GET /api/v1/study-plan/sessions`  
**Authentication:** Required  
**Description:** Get user's study session history

**Response:** `200 OK`
```json
[
  {
    "id": "950e8400-e29b-41d4-a716-446655440004",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "topic_id": "550e8400-e29b-41d4-a716-446655440000",
    "session_type": "practice",
    "start_time": "2026-06-11T10:00:00",
    "end_time": "2026-06-11T11:30:00",
    "duration_minutes": 90,
    "questions_attempted": 25,
    "correct_answers": 20,
    "xp_earned": 250
  }
]
```

---

### Mock Test Endpoints

#### 15. Get Mock Tests
**Endpoint:** `GET /api/v1/mock-tests/`  
**Authentication:** None  
**Description:** Get list of available mock tests

**Query Parameters:**
- `exam_type` (optional): Filter by exam type (e.g., "GRE", "GATE")

**Response:** `200 OK`
```json
[
  {
    "id": "a50e8400-e29b-41d4-a716-446655440005",
    "exam_type": "GRE",
    "test_name": "GRE Practice Test 1",
    "duration_minutes": 180,
    "total_questions": 80,
    "topic_distribution": {
      "verbal": 40,
      "quant": 40
    },
    "passing_score": 150,
    "max_score": 340,
    "is_official": false,
    "created_at": "2026-06-01T00:00:00"
  }
]
```

---

#### 16. Get Mock Test by ID
**Endpoint:** `GET /api/v1/mock-tests/{test_id}`  
**Authentication:** None  
**Description:** Get details of a specific mock test

**Response:** `200 OK`
```json
{
  "id": "a50e8400-e29b-41d4-a716-446655440005",
  "exam_type": "GRE",
  "test_name": "GRE Practice Test 1",
  "duration_minutes": 180,
  "total_questions": 80,
  "topic_distribution": {...},
  "passing_score": 150,
  "max_score": 340,
  "is_official": false,
  "created_at": "2026-06-01T00:00:00"
}
```

---

#### 17. Start Mock Test
**Endpoint:** `POST /api/v1/mock-tests/attempts`  
**Authentication:** Required  
**Description:** Start a new mock test attempt

**Request Body:**
```json
{
  "mock_test_id": "a50e8400-e29b-41d4-a716-446655440005"
}
```

**Response:** `201 Created`
```json
{
  "id": "b50e8400-e29b-41d4-a716-446655440006",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "mock_test_id": "a50e8400-e29b-41d4-a716-446655440005",
  "start_time": "2026-06-11T10:00:00",
  "end_time": null,
  "score": null,
  "max_score": 340,
  "percentile": null,
  "time_taken_minutes": null,
  "completed": false,
  "detailed_analysis": null
}
```

---

#### 18. Submit Mock Test
**Endpoint:** `POST /api/v1/mock-tests/attempts/submit`  
**Authentication:** Required  
**Description:** Submit answers for a mock test

**Request Body:**
```json
{
  "attempt_id": "b50e8400-e29b-41d4-a716-446655440006",
  "answers": {
    "question_id_1": "A",
    "question_id_2": "B",
    "question_id_3": "42.5"
  }
}
```

**Response:** `200 OK`
```json
{
  "id": "b50e8400-e29b-41d4-a716-446655440006",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "mock_test_id": "a50e8400-e29b-41d4-a716-446655440005",
  "start_time": "2026-06-11T10:00:00",
  "end_time": "2026-06-11T13:00:00",
  "score": 310,
  "max_score": 340,
  "percentile": 85.5,
  "time_taken_minutes": 180,
  "completed": true,
  "detailed_analysis": {
    "verbal_score": 160,
    "quant_score": 150,
    "topic_breakdown": {...}
  }
}
```

---

#### 19. Get My Mock Test Attempts
**Endpoint:** `GET /api/v1/mock-tests/attempts/my`  
**Authentication:** Required  
**Description:** Get user's mock test attempt history

**Response:** `200 OK`
```json
[
  {
    "id": "b50e8400-e29b-41d4-a716-446655440006",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "mock_test_id": "a50e8400-e29b-41d4-a716-446655440005",
    "start_time": "2026-06-11T10:00:00",
    "end_time": "2026-06-11T13:00:00",
    "score": 310,
    "max_score": 340,
    "percentile": 85.5,
    "time_taken_minutes": 180,
    "completed": true,
    "detailed_analysis": {...}
  }
]
```

---

### Analytics Endpoints

#### 20. Get User Statistics
**Endpoint:** `GET /api/v1/analytics/stats`  
**Authentication:** Required  
**Description:** Get comprehensive user statistics

**Response:** `200 OK`
```json
{
  "total_xp": 5420,
  "level": 12,
  "current_streak": 7,
  "longest_streak": 15,
  "total_study_hours": 48,
  "total_questions_attempted": 542,
  "total_correct_answers": 421,
  "mock_tests_taken": 3,
  "topics_mastered": 8,
  "accuracy_rate": 77.67,
  "rank": 145,
  "percentile": 92.3
}
```

---

#### 21. Get Progress Analytics
**Endpoint:** `GET /api/v1/analytics/progress`  
**Authentication:** Required  
**Description:** Get detailed progress analytics and trends

**Response:** `200 OK`
```json
{
  "daily_activity": [
    {
      "date": "2026-06-10",
      "questions_attempted": 25,
      "study_minutes": 90,
      "xp_earned": 250
    }
  ],
  "topic_performance": [
    {
      "topic_name": "Algebra",
      "mastery_score": 85.5,
      "questions_attempted": 120,
      "accuracy": 0.82
    }
  ],
  "accuracy_trend": [
    {
      "date": "2026-06-10",
      "accuracy": 0.82
    }
  ],
  "study_time_distribution": {
    "practice": 1200,
    "review": 600,
    "mock_test": 540
  }
}
```

---

#### 22. Get Leaderboard
**Endpoint:** `GET /api/v1/analytics/leaderboard`  
**Authentication:** Required  
**Description:** Get global leaderboard rankings

**Query Parameters:**
- `limit` (optional): Number of top users to return (default: 50)

**Response:** `200 OK`
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "user_name": "TopStudent",
      "total_xp": 15420,
      "level": 28,
      "is_current_user": false
    },
    {
      "rank": 2,
      "user_name": "John Doe",
      "total_xp": 12340,
      "level": 24,
      "is_current_user": true
    }
  ],
  "current_user_rank": 2,
  "total_users": 1543
}
```

---

## 🔒 Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Inactive user account"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 📊 Data Models

### User Object
```typescript
{
  id: string (UUID)
  email: string
  full_name?: string
  exam_type?: string
  target_score?: number
  exam_date?: string (ISO 8601)
  created_at: string (ISO 8601)
  last_active: string (ISO 8601)
  is_active: boolean
  is_verified: boolean
}
```

### Question Object
```typescript
{
  id: string (UUID)
  topic_id: string (UUID)
  question_text: string
  question_type: "mcq" | "numeric" | "descriptive"
  options?: { [key: string]: string }
  difficulty: "easy" | "medium" | "hard"
  tags?: string[]
}
```

### Session Object
```typescript
{
  id: string (UUID)
  user_id: string (UUID)
  topic_id?: string (UUID)
  session_type: "practice" | "review" | "mock_test" | "tutoring"
  start_time: string (ISO 8601)
  end_time?: string (ISO 8601)
  duration_minutes?: number
  questions_attempted: number
  correct_answers: number
  xp_earned: number
}
```

---

## 🔄 Rate Limiting

- **Per Minute:** 60 requests
- **Per Hour:** 1000 requests

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1654855200
```

---

## 🌐 CORS

Allowed origins are configured in the `.env` file:
```
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

---

## 📝 Notes

- All timestamps are in UTC
- All IDs are UUIDs (v4)
- Token expiration: Access token (15 minutes), Refresh token (7 days)
- Maximum file upload size: 10MB
- API versioning: `/api/v1`, `/api/v2`, etc.

---

**Interactive Documentation:** http://localhost:8000/docs  
**Alternative Documentation:** http://localhost:8000/redoc
