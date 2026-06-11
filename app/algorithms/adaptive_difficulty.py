from typing import Literal


class AdaptiveDifficultyEngine:
    """Determine appropriate difficulty level based on user performance"""
    
    @staticmethod
    def calculate_difficulty(
        mastery_score: float,
        recent_accuracy: float,
        topic_attempts: int
    ) -> Literal["easy", "medium", "hard"]:
        """
        Calculate appropriate difficulty level
        
        Args:
            mastery_score: 0-100 topic mastery score
            recent_accuracy: 0.0-1.0 recent performance
            topic_attempts: number of questions attempted
        
        Returns:
            difficulty level: "easy", "medium", or "hard"
        """
        # New topic - start with easy
        if topic_attempts < 5:
            return "easy"
        
        # High mastery and accuracy - hard questions
        if mastery_score >= 70 and recent_accuracy >= 0.80:
            return "hard"
        
        # Medium mastery - medium questions
        if mastery_score >= 40 or recent_accuracy >= 0.60:
            return "medium"
        
        # Low mastery - easy questions
        return "easy"
    
    @staticmethod
    def calculate_mastery_score(
        total_attempts: int,
        correct_answers: int,
        recent_accuracy: float
    ) -> float:
        """
        Calculate overall mastery score (0-100)
        
        Args:
            total_attempts: total questions attempted
            correct_answers: total correct answers
            recent_accuracy: accuracy in recent attempts (0.0-1.0)
        
        Returns:
            mastery_score: 0-100
        """
        if total_attempts == 0:
            return 0.0
        
        # Overall accuracy
        overall_accuracy = correct_answers / total_attempts
        
        # Weight recent performance more heavily (70% recent, 30% overall)
        weighted_accuracy = (0.7 * recent_accuracy) + (0.3 * overall_accuracy)
        
        # Factor in attempt count (bonus for more practice)
        attempt_bonus = min(10, total_attempts / 10)  # max 10 bonus points
        
        mastery = (weighted_accuracy * 90) + attempt_bonus
        
        return min(100.0, mastery)
