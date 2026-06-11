# 🎨 Frontend Developer's API Integration Guide

**API Base URL:** `http://localhost:8000/api/v1`

---

## 🚀 Quick Integration

### Step 1: Setup API Client

```javascript
// api/client.js
const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.accessToken && !options.skipAuth) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (response.status === 401 && this.refreshToken) {
        // Token expired, try to refresh
        await this.refreshAccessToken();
        return this.request(endpoint, options);
      }

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'API request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async refreshAccessToken() {
    const response = await fetch(`${this.baseURL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: this.refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      this.setTokens(data.access_token, data.refresh_token);
    } else {
      this.clearTokens();
      window.location.href = '/login';
    }
  }

  setTokens(accessToken, refreshToken) {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export default new ApiClient();
```

---

## 📋 API Methods Reference

### Authentication

#### Register User
```javascript
// api/auth.js
import api from './client';

export const registerUser = async (userData) => {
  return await api.post('/auth/register', {
    email: userData.email,
    password: userData.password,
    full_name: userData.fullName,
    exam_type: userData.examType,
    target_score: userData.targetScore,
    exam_date: userData.examDate,
  });
};

// Usage in component:
const handleRegister = async () => {
  try {
    const user = await registerUser({
      email: 'user@example.com',
      password: 'SecurePass123!',
      fullName: 'John Doe',
      examType: 'GRE',
      targetScore: 320,
      examDate: '2026-12-31',
    });
    console.log('User registered:', user);
  } catch (error) {
    console.error('Registration failed:', error.message);
  }
};
```

#### Login
```javascript
export const loginUser = async (email, password) => {
  const data = await api.post('/auth/login', { email, password }, { skipAuth: true });
  api.setTokens(data.access_token, data.refresh_token);
  return data;
};

// Usage:
const handleLogin = async () => {
  try {
    await loginUser('user@example.com', 'SecurePass123!');
    // Redirect to dashboard
    navigate('/dashboard');
  } catch (error) {
    alert('Login failed: ' + error.message);
  }
};
```

#### Logout
```javascript
export const logout = () => {
  api.clearTokens();
  window.location.href = '/login';
};
```

---

### User Profile

#### Get Current User
```javascript
// api/users.js
import api from './client';

export const getCurrentUser = async () => {
  return await api.get('/users/me');
};

// Usage in React:
import { useEffect, useState } from 'react';

function ProfilePage() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    getCurrentUser().then(setUser);
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.full_name}</h1>
      <p>Email: {user.email}</p>
      <p>Exam: {user.exam_type}</p>
      <p>Target Score: {user.target_score}</p>
    </div>
  );
}
```

#### Update Profile
```javascript
export const updateProfile = async (updates) => {
  return await api.put('/users/me', updates);
};

// Usage:
const handleUpdate = async () => {
  try {
    const updated = await updateProfile({
      full_name: 'Jane Doe',
      target_score: 330,
    });
    console.log('Profile updated:', updated);
  } catch (error) {
    console.error('Update failed:', error.message);
  }
};
```

---

### Practice Questions

#### Get Questions
```javascript
// api/practice.js
import api from './client';

export const getPracticeQuestions = async (topicId, count = 10, difficulty = null) => {
  const params = new URLSearchParams({
    topic_id: topicId,
    count: count.toString(),
  });
  
  if (difficulty) params.append('difficulty', difficulty);
  
  return await api.get(`/practice/questions?${params}`);
};

// Usage in component:
function PracticeSession() {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const loadQuestions = async () => {
      const data = await getPracticeQuestions('topic-uuid-here', 10);
      setQuestions(data);
    };
    loadQuestions();
  }, []);

  const currentQuestion = questions[currentIndex];

  return (
    <div>
      {currentQuestion && (
        <div>
          <h3>Question {currentIndex + 1} of {questions.length}</h3>
          <p>{currentQuestion.question_text}</p>
          {currentQuestion.options && (
            <div>
              {Object.entries(currentQuestion.options).map(([key, value]) => (
                <button key={key} onClick={() => handleAnswer(key)}>
                  {key}. {value}
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

#### Submit Answer
```javascript
export const submitAnswer = async (questionId, answer, timeTaken) => {
  return await api.post('/practice/submit-answer', {
    question_id: questionId,
    answer: answer,
    time_taken_seconds: timeTaken,
  });
};

// Usage:
const handleAnswer = async (selectedOption) => {
  const startTime = Date.now(); // Track when question was shown
  
  try {
    const result = await submitAnswer(
      currentQuestion.id,
      selectedOption,
      Math.floor((Date.now() - startTime) / 1000)
    );
    
    if (result.is_correct) {
      alert(`Correct! +${result.xp_earned} XP`);
    } else {
      alert(`Incorrect. Correct answer: ${result.correct_answer}`);
    }
    
    // Show explanation
    console.log(result.explanation);
    
    // Move to next question
    setCurrentIndex(prev => prev + 1);
  } catch (error) {
    console.error('Submit failed:', error);
  }
};
```

---

### Study Plans

#### Create Study Plan
```javascript
// api/studyPlan.js
import api from './client';

export const createStudyPlan = async (planData) => {
  return await api.post('/study-plan/', {
    start_date: planData.startDate,
    end_date: planData.endDate,
    daily_hours: planData.dailyHours,
    target_topics: planData.targetTopics,
  });
};

// Usage:
const handleCreatePlan = async () => {
  try {
    const plan = await createStudyPlan({
      startDate: '2026-06-15T00:00:00',
      endDate: '2026-12-31T23:59:59',
      dailyHours: 3.0,
      targetTopics: ['topic-uuid-1', 'topic-uuid-2'],
    });
    console.log('Plan created:', plan);
  } catch (error) {
    console.error('Failed to create plan:', error);
  }
};
```

#### Start Study Session
```javascript
export const startSession = async (topicId, sessionType = 'practice') => {
  return await api.post('/study-plan/sessions', {
    topic_id: topicId,
    session_type: sessionType,
  });
};

// Usage:
let currentSessionId = null;

const handleStartStudy = async () => {
  const session = await startSession('topic-uuid', 'practice');
  currentSessionId = session.id;
  console.log('Session started:', session.id);
};
```

#### End Study Session
```javascript
export const endSession = async (sessionId) => {
  return await api.post('/study-plan/sessions/end', {
    session_id: sessionId,
  });
};

// Usage:
const handleEndStudy = async () => {
  if (currentSessionId) {
    const session = await endSession(currentSessionId);
    console.log(`Session completed: ${session.duration_minutes} minutes`);
    console.log(`Questions: ${session.questions_attempted}, Correct: ${session.correct_answers}`);
    console.log(`XP Earned: ${session.xp_earned}`);
  }
};
```

---

### Mock Tests

#### Get Mock Tests
```javascript
// api/mockTests.js
import api from './client';

export const getMockTests = async (examType = null) => {
  const params = examType ? `?exam_type=${examType}` : '';
  return await api.get(`/mock-tests/${params}`);
};

// Usage:
function MockTestsList() {
  const [tests, setTests] = useState([]);

  useEffect(() => {
    getMockTests('GRE').then(setTests);
  }, []);

  return (
    <div>
      {tests.map(test => (
        <div key={test.id}>
          <h3>{test.test_name}</h3>
          <p>Duration: {test.duration_minutes} minutes</p>
          <p>Questions: {test.total_questions}</p>
          <button onClick={() => handleStartTest(test.id)}>
            Start Test
          </button>
        </div>
      ))}
    </div>
  );
}
```

#### Start Mock Test
```javascript
export const startMockTest = async (testId) => {
  return await api.post('/mock-tests/attempts', {
    mock_test_id: testId,
  });
};

// Usage:
const handleStartTest = async (testId) => {
  const attempt = await startMockTest(testId);
  // Store attempt ID and start test UI
  localStorage.setItem('current_test_attempt', attempt.id);
  navigate(`/mock-test/${attempt.id}`);
};
```

#### Submit Mock Test
```javascript
export const submitMockTest = async (attemptId, answers) => {
  return await api.post('/mock-tests/attempts/submit', {
    attempt_id: attemptId,
    answers: answers,
  });
};

// Usage:
const handleSubmitTest = async () => {
  const attemptId = localStorage.getItem('current_test_attempt');
  const answers = {
    'question-uuid-1': 'A',
    'question-uuid-2': 'B',
    'question-uuid-3': '42.5',
  };
  
  const result = await submitMockTest(attemptId, answers);
  
  console.log(`Score: ${result.score}/${result.max_score}`);
  console.log(`Percentile: ${result.percentile}%`);
  console.log('Detailed Analysis:', result.detailed_analysis);
  
  // Show results page
  navigate('/test-results');
};
```

---

### Analytics

#### Get User Stats
```javascript
// api/analytics.js
import api from './client';

export const getUserStats = async () => {
  return await api.get('/analytics/stats');
};

// Usage:
function StatsCard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getUserStats().then(setStats);
  }, []);

  if (!stats) return <div>Loading...</div>;

  return (
    <div className="stats-card">
      <div>Level: {stats.level}</div>
      <div>XP: {stats.total_xp}</div>
      <div>Streak: {stats.current_streak} days</div>
      <div>Accuracy: {stats.accuracy_rate.toFixed(1)}%</div>
      <div>Rank: #{stats.rank}</div>
      <div>Percentile: {stats.percentile}%</div>
    </div>
  );
}
```

#### Get Leaderboard
```javascript
export const getLeaderboard = async (limit = 50) => {
  return await api.get(`/analytics/leaderboard?limit=${limit}`);
};

// Usage:
function Leaderboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getLeaderboard(10).then(setData);
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h2>Top Players</h2>
      <p>Your Rank: #{data.current_user_rank} of {data.total_users}</p>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Level</th>
            <th>XP</th>
          </tr>
        </thead>
        <tbody>
          {data.leaderboard.map(entry => (
            <tr key={entry.rank} className={entry.is_current_user ? 'current-user' : ''}>
              <td>{entry.rank}</td>
              <td>{entry.user_name}</td>
              <td>{entry.level}</td>
              <td>{entry.total_xp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## 🎯 Complete User Flow Example

```javascript
// Example: Complete study session flow
import { 
  loginUser, 
  startSession, 
  getPracticeQuestions, 
  submitAnswer, 
  endSession,
  getUserStats 
} from './api';

async function completeStudySession() {
  try {
    // 1. Login
    await loginUser('user@example.com', 'password123');
    console.log('✓ Logged in');

    // 2. Start session
    const session = await startSession('topic-uuid', 'practice');
    console.log('✓ Session started:', session.id);

    // 3. Get questions
    const questions = await getPracticeQuestions('topic-uuid', 5);
    console.log('✓ Got questions:', questions.length);

    // 4. Answer questions
    for (const question of questions) {
      const result = await submitAnswer(question.id, 'A', 30);
      console.log(`✓ Question ${question.id}:`, result.is_correct ? 'Correct!' : 'Incorrect');
    }

    // 5. End session
    const completedSession = await endSession(session.id);
    console.log('✓ Session ended');
    console.log(`  - Duration: ${completedSession.duration_minutes} min`);
    console.log(`  - Accuracy: ${completedSession.correct_answers}/${completedSession.questions_attempted}`);
    console.log(`  - XP Earned: ${completedSession.xp_earned}`);

    // 6. Get updated stats
    const stats = await getUserStats();
    console.log('✓ Updated stats:', stats);

  } catch (error) {
    console.error('Error:', error.message);
  }
}
```

---

## 🔒 Authentication State Management

### React Context Example

```javascript
// contexts/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/client';
import { getCurrentUser } from '../api/users';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    if (api.accessToken) {
      getCurrentUser()
        .then(setUser)
        .catch(() => api.clearTokens())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const data = await api.post('/auth/login', { email, password });
    api.setTokens(data.access_token, data.refresh_token);
    const userData = await getCurrentUser();
    setUser(userData);
  };

  const logout = () => {
    api.clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

---

## 🚨 Error Handling

```javascript
// utils/errorHandler.js
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        return 'Invalid request. Please check your input.';
      case 401:
        return 'Session expired. Please login again.';
      case 403:
        return 'You do not have permission to perform this action.';
      case 404:
        return 'Resource not found.';
      case 422:
        return 'Validation error: ' + (data.detail?.[0]?.msg || 'Invalid data');
      case 500:
        return 'Server error. Please try again later.';
      default:
        return 'An unexpected error occurred.';
    }
  } else if (error.request) {
    // Request made but no response
    return 'Network error. Please check your connection.';
  } else {
    // Other errors
    return error.message || 'An error occurred.';
  }
};

// Usage:
try {
  await submitAnswer(questionId, answer);
} catch (error) {
  const message = handleApiError(error);
  showNotification(message, 'error');
}
```

---

## 📱 Environment Configuration

```javascript
// config.js
const config = {
  development: {
    apiBaseUrl: 'http://localhost:8000/api/v1',
  },
  production: {
    apiBaseUrl: 'https://api.synapseai.com/api/v1',
  },
};

export default config[process.env.NODE_ENV || 'development'];
```

---

## ✅ Checklist for Frontend Integration

- [ ] Setup API client with token management
- [ ] Implement authentication (login/register)
- [ ] Create protected route wrapper
- [ ] Implement error handling
- [ ] Add loading states for async operations
- [ ] Setup environment variables
- [ ] Test all API endpoints
- [ ] Implement token refresh logic
- [ ] Add request/response interceptors if needed
- [ ] Handle offline scenarios

---

**Need help?** Check the interactive API docs at http://localhost:8000/docs
