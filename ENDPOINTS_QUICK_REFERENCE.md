# 🚀 API Endpoints Quick Reference

**Base URL:** `http://localhost:8000/api/v1`

---

## 📋 Endpoints Summary Table

| Category | Method | Endpoint | Auth | Description |
|----------|--------|----------|------|-------------|
| **Authentication** |
| | POST | `/auth/register` | ❌ | Register new user |
| | POST | `/auth/login` | ❌ | Login and get tokens |
| | POST | `/auth/refresh` | ❌ | Refresh access token |
| **Users** |
| | GET | `/users/me` | ✅ | Get current user profile |
| | PUT | `/users/me` | ✅ | Update user profile |
| | DELETE | `/users/me` | ✅ | Delete account |
| **Practice** |
| | GET | `/practice/questions` | ✅ | Get practice questions |
| | POST | `/practice/submit-answer` | ✅ | Submit answer |
| | GET | `/practice/attempts` | ✅ | Get attempt history |
| **Study Plan** |
| | POST | `/study-plan/` | ✅ | Create study plan |
| | GET | `/study-plan/active` | ✅ | Get active plan |
| | POST | `/study-plan/sessions` | ✅ | Start session |
| | POST | `/study-plan/sessions/end` | ✅ | End session |
| | GET | `/study-plan/sessions` | ✅ | Get sessions history |
| **Mock Tests** |
| | GET | `/mock-tests/` | ❌ | List mock tests |
| | GET | `/mock-tests/{id}` | ❌ | Get test details |
| | POST | `/mock-tests/attempts` | ✅ | Start test |
| | POST | `/mock-tests/attempts/submit` | ✅ | Submit test |
| | GET | `/mock-tests/attempts/my` | ✅ | Get my attempts |
| **Analytics** |
| | GET | `/analytics/stats` | ✅ | Get user stats |
| | GET | `/analytics/progress` | ✅ | Get progress analytics |
| | GET | `/analytics/leaderboard` | ✅ | Get leaderboard |

---

## 🔑 Quick Authentication

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123!"}'

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123!"}'

# Response: {"access_token":"...", "refresh_token":"..."}

# 3. Use token for protected endpoints
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📦 Request/Response Formats

### Register User
```
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "exam_type": "GRE"
}
→ 201 Created
```

### Get Practice Questions
```
GET /api/v1/practice/questions?topic_id=UUID&count=10
Authorization: Bearer TOKEN
→ 200 OK [array of questions]
```

### Submit Answer
```
POST /api/v1/practice/submit-answer
Authorization: Bearer TOKEN
{
  "question_id": "UUID",
  "answer": "A",
  "time_taken_seconds": 45
}
→ 200 OK {"is_correct": true, "xp_earned": 10}
```

### Get User Stats
```
GET /api/v1/analytics/stats
Authorization: Bearer TOKEN
→ 200 OK {"total_xp": 5420, "level": 12, "accuracy_rate": 77.67}
```

---

## 🎯 Common Query Parameters

| Endpoint | Parameter | Type | Description |
|----------|-----------|------|-------------|
| `/practice/questions` | `topic_id` | UUID | Topic ID (required) |
| | `count` | number | Questions count (1-50) |
| | `difficulty` | string | easy/medium/hard |
| `/practice/attempts` | `limit` | number | Results limit (1-200) |
| `/mock-tests/` | `exam_type` | string | Filter by exam type |
| `/analytics/leaderboard` | `limit` | number | Top users count |

---

## 🔄 Typical User Flow

```
1. Register → POST /auth/register
2. Login → POST /auth/login (get tokens)
3. Get Profile → GET /users/me
4. Create Study Plan → POST /study-plan/
5. Start Session → POST /study-plan/sessions
6. Get Questions → GET /practice/questions
7. Submit Answers → POST /practice/submit-answer (multiple times)
8. End Session → POST /study-plan/sessions/end
9. View Stats → GET /analytics/stats
10. Check Leaderboard → GET /analytics/leaderboard
```

---

## 🚨 Error Codes

- `400` - Bad Request
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (inactive account)
- `404` - Not Found
- `422` - Validation Error
- `500` - Server Error

---

## 📚 Full Documentation

- **Complete API Docs:** `API_DOCUMENTATION.md`
- **Frontend Integration:** `FRONTEND_API_GUIDE.md`
- **Interactive Swagger:** http://localhost:8000/docs
- **JSON Summary:** `endpoints-summary.json`

---

## ⚡ Rate Limits

- **60** requests per minute
- **1000** requests per hour

---

**Quick Start:** `uvicorn app.main:app --reload`
