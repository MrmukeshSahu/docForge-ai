import re
from typing import List, Dict, Any

US_UK_PAIRS = [
    ("color", "colour"),
    ("center", "centre"),
    ("analyze", "analyse"),
    ("organize", "organise"),
    ("defense", "defence"),
    ("behavior", "behaviour"),
    ("flavor", "flavour"),
    ("theater", "theatre"),
    ("neighbor", "neighbour"),
    ("traveled", "travelled")
]

class GrammarConsistencyChecker:
    @staticmethod
    def analyze_consistency(elements_with_classes: List[Dict[str, Any]]) -> Dict[str, Any]:
        us_counts = {}
        uk_counts = {}
        repeat_words = []
        passive_voice_count = 0

        passive_patterns = r'\b(is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en)\b'

        for idx, item in enumerate(elements_with_classes):
            text = item.get('text', '')
            lower_text = text.lower()

            # US vs UK check
            for us, uk in US_UK_PAIRS:
                us_matches = len(re.findall(r'\b' + us + r'\b', lower_text))
                uk_matches = len(re.findall(r'\b' + uk + r'\b', lower_text))
                if us_matches > 0: us_counts[us] = us_counts.get(us, 0) + us_matches
                if uk_matches > 0: uk_counts[uk] = uk_counts.get(uk, 0) + uk_matches

            # Repeat word glitches (e.g. "the the")
            repeats = re.findall(r'\b([a-zA-Z]{2,})\s+\1\b', text, re.IGNORECASE)
            for r in repeats:
                repeat_words.append({"element_idx": idx+1, "word": r, "snippet": text[:60]})

            # Passive voice heuristic
            passives = re.findall(passive_patterns, lower_text)
            passive_voice_count += len(passives)

        dialect_summary = "US English Dominant" if sum(us_counts.values()) >= sum(uk_counts.values()) else "UK English Dominant"

        return {
            "us_spelling_count": sum(us_counts.values()),
            "uk_spelling_count": sum(uk_counts.values()),
            "us_breakdown": us_counts,
            "uk_breakdown": uk_counts,
            "dominant_dialect": dialect_summary,
            "repeat_word_glitches": repeat_words,
            "passive_voice_count": passive_voice_count
        }
