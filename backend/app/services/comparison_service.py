from typing import Dict, List
import re

class ComparisonService:
    """
    Service for comparing recognized text with Qur'an verse text.
    """
    
    def __init__(self):
        pass
    
    def compare(self, recognized_text: str, verse_text: str) -> Dict:
        """
        Compare recognized text with verse text word by word.
        
        Args:
            recognized_text: Text recognized from audio
            verse_text: Reference verse text from Qur'an
            
        Returns:
            Dict with comparison results including word-by-word matches
        """
        # Normalize texts (remove diacritics for more lenient matching)
        normalized_recognized = self._normalize_text(recognized_text)
        normalized_verse = self._normalize_text(verse_text)
        
        # Split into words
        recognized_words = self._split_words(normalized_recognized)
        verse_words = self._split_words(normalized_verse)
        
        # Compare words
        word_comparisons = []
        matched_words = 0
        mismatched_words = 0
        max_len = max(len(recognized_words), len(verse_words))
        
        for i in range(max_len):
            recognized_word = recognized_words[i] if i < len(recognized_words) else None
            verse_word = verse_words[i] if i < len(verse_words) else None
            
            is_match = (
                recognized_word is not None and
                verse_word is not None and
                recognized_word == verse_word
            )
            
            if is_match:
                matched_words += 1
            else:
                mismatched_words += 1
            
            word_comparisons.append({
                "position": i,
                "recognized": recognized_word or "",
                "verse": verse_word or "",
                "match": is_match
            })
        
        total_words = len(verse_words)
        match_percentage = (matched_words / total_words * 100) if total_words > 0 else 0.0
        
        return {
            "match_percentage": round(match_percentage, 2),
            "word_comparisons": word_comparisons,
            "total_words": total_words,
            "matched_words": matched_words,
            "mismatched_words": mismatched_words
        }
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize Arabic text by removing diacritics and extra whitespace.
        """
        # Remove Arabic diacritics (tashkeel)
        diacritics = "ًٌٍَُِّْٰۖۗۘۙۚۛۜ"
        normalized = "".join(char for char in text if char not in diacritics)
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def _split_words(self, text: str) -> List[str]:
        """
        Split text into words, handling Arabic text properly.
        """
        # Split by whitespace and filter empty strings
        words = [w.strip() for w in text.split() if w.strip()]
        return words

