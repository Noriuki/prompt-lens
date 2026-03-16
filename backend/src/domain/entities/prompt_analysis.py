from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class PromptAnalysis:
    summary: str
    word_count: int
    char_count: int
    line_count: int
    clarity_score: int
    has_examples: bool
    sections: List[str]
    estimated_tokens: int
    has_instructions: bool
    suggestions: List[str]
