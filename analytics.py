import re
from typing import Dict, Any, List

def count_syllables(word: str) -> int:
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    syllables = len(re.findall(r'[aeiouy]{1,2}', word))
    return max(1, syllables)

class DocumentAnalytics:
    @staticmethod
    def analyze(doc, elements_with_classes: List[Dict[str, Any]], tables_count: int = 0, images_count: int = 0) -> Dict[str, Any]:
        total_paragraphs = len(elements_with_classes)
        total_words = 0
        total_chars = 0
        total_sentences = 0
        total_syllables = 0
        
        tally = {}
        heading_hierarchy = []
        
        for item in elements_with_classes:
            text = item.get('text', '')
            cls = item.get('classification', 'Body Paragraph')
            tally[cls] = tally.get(cls, 0) + 1
            
            if cls in ["Title", "Heading 1", "Heading 2", "Heading 3", "Subheading"]:
                heading_hierarchy.append({
                    "text": text,
                    "level": cls
                })
            
            words = text.split()
            w_count = len(words)
            total_words += w_count
            total_chars += len(text)
            
            # Sentence counting heuristic
            sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
            s_count = len(sentences) if sentences else 1
            total_sentences += s_count
            
            for w in words:
                total_syllables += count_syllables(w)
                
        # Fallbacks
        total_sentences = max(1, total_sentences)
        total_words_safe = max(1, total_words)
        
        # Flesch Reading Ease Formula
        flesch_score = 206.835 - (1.015 * (total_words / total_sentences)) - (84.6 * (total_syllables / total_words_safe))
        flesch_score = max(0.0, min(100.0, flesch_score))
        
        # Flesch-Kincaid Grade Level Formula
        fk_grade = (0.39 * (total_words / total_sentences)) + (11.8 * (total_syllables / total_words_safe)) - 15.59
        fk_grade = max(0.0, fk_grade)
        
        # Reading Time (200 WPM)
        reading_time_mins = round(total_words / 200.0, 1)
        
        # Readability Description
        if flesch_score >= 80:
            readability_label = "Easy (6th Grade)"
        elif flesch_score >= 60:
            readability_label = "Standard (8th - 9th Grade)"
        elif flesch_score >= 40:
            readability_label = "Challenging (High School / College)"
        else:
            readability_label = "Academic / Professional (Advanced)"

        # Overused words analysis (length >= 4, excluding stop words)
        stop_words = {"the", "and", "that", "have", "for", "not", "with", "you", "this", "but", "his", "from", "they", "say", "her", "she", "will", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"}
        word_freq = {}
        for item in elements_with_classes:
            words = re.findall(r'\b[a-zA-Z]{4,}\b', item.get('text', '').lower())
            for w in words:
                if w not in stop_words:
                    word_freq[w] = word_freq.get(w, 0) + 1

        sorted_overused = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
        return {
            "total_paragraphs": total_paragraphs,
            "total_words": total_words,
            "total_chars": total_chars,
            "total_sentences": total_sentences,
            "total_tables": tables_count,
            "total_images": images_count,
            "flesch_score": round(flesch_score, 1),
            "fk_grade": round(fk_grade, 1),
            "readability_label": readability_label,
            "reading_time_mins": reading_time_mins,
            "classification_tally": tally,
            "heading_hierarchy": heading_hierarchy,
            "overused_words": sorted_overused
        }

