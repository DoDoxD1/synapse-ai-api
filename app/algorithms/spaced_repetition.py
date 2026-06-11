from datetime import datetime, timedelta
from typing import Tuple
from app.models.topic import UserTopicMastery


class SM2Algorithm:
    """SuperMemo 2 (SM-2) Spaced Repetition Algorithm"""
    
    @staticmethod
    def calculate_next_review(
        mastery: UserTopicMastery,
        quality: int  # 0-5: 0=complete forget, 5=perfect recall
    ) -> Tuple[datetime, int, float, int]:
        """
        Calculate next review date based on performance
        
        Returns:
            (next_review_date, interval_days, easiness_factor, repetition_count)
        """
        if quality < 3:
            # Failed recall - reset to beginning
            interval = 1
            repetitions = 0
            easiness = mastery.easiness_factor
        else:
            # Successful recall
            if mastery.repetition_count == 0:
                interval = 1
            elif mastery.repetition_count == 1:
                interval = 6
            else:
                interval = round(mastery.interval_days * mastery.easiness_factor)
            
            repetitions = mastery.repetition_count + 1
            
            # Adjust easiness factor
            easiness = mastery.easiness_factor + (
                0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
            )
            
            # Easiness factor shouldn't go below 1.3
            if easiness < 1.3:
                easiness = 1.3
        
        next_review = datetime.utcnow() + timedelta(days=interval)
        
        return next_review, interval, easiness, repetitions
    
    @staticmethod
    def calculate_quality_from_accuracy(accuracy: float, time_ratio: float = 1.0) -> int:
        """
        Convert practice accuracy to quality rating (0-5)
        
        Args:
            accuracy: 0.0 to 1.0
            time_ratio: actual_time / expected_time (1.0 = perfect timing)
        
        Returns:
            quality: 0-5
        """
        # Base quality from accuracy
        if accuracy >= 0.95:
            base_quality = 5
        elif accuracy >= 0.85:
            base_quality = 4
        elif accuracy >= 0.70:
            base_quality = 3
        elif accuracy >= 0.50:
            base_quality = 2
        elif accuracy >= 0.30:
            base_quality = 1
        else:
            base_quality = 0
        
        # Adjust for time (minor adjustment)
        if time_ratio > 1.5:
            base_quality = max(0, base_quality - 1)  # took too long
        elif time_ratio < 0.7:
            base_quality = min(5, base_quality + 1)  # very fast
        
        return base_quality
