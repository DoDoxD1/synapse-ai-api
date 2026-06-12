from enum import Enum


class ExamType(str, Enum):
    """Supported Indian competitive exams."""
    JEE_MAIN = "JEE_MAIN"
    JEE_ADVANCED = "JEE_ADVANCED"
    NEET = "NEET"
    GATE = "GATE"
    CAT = "CAT"
    UPSC_CSE_PRELIMS = "UPSC_CSE_PRELIMS"
    CLAT = "CLAT"
    NDA = "NDA"


# Maximum possible score for each exam type
EXAM_MAX_SCORES: dict[ExamType, int] = {
    ExamType.JEE_MAIN: 300,
    ExamType.JEE_ADVANCED: 360,
    ExamType.NEET: 720,
    ExamType.GATE: 100,
    ExamType.CAT: 300,
    ExamType.UPSC_CSE_PRELIMS: 200,
    ExamType.CLAT: 150,
    ExamType.NDA: 900,
}


def get_max_score(exam_type: ExamType) -> int:
    """Return the maximum possible score for the given exam type."""
    return EXAM_MAX_SCORES[exam_type]
