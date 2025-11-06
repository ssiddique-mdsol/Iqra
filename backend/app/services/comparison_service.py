from typing import Dict, List
import re
from difflib import SequenceMatcher

class ComparisonService:
    """
    Service for comparing recognized text with Qur'an verse text.
    Uses fuzzy matching to reduce false negatives.
    """
    
    def __init__(self):
        # Similarity threshold for considering words as matches (0.0 to 1.0)
        self.similarity_threshold = 0.75  # 75% similarity = match
        # Allow reordering of words within a small window
        self.max_word_distance = 2  # Words can be 2 positions apart and still match
    
    def compare(self, recognized_text: str, verse_text: str) -> Dict:
        """
        Compare recognized text with verse text word by word using fuzzy matching.
        
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
        
        # Use fuzzy matching with word alignment
        word_comparisons, matched_words, mismatched_words = self._fuzzy_compare_words(
            recognized_words, verse_words
        )
        
        total_words = len(verse_words)
        match_percentage = (matched_words / total_words * 100) if total_words > 0 else 0.0
        
        return {
            "match_percentage": round(match_percentage, 2),
            "word_comparisons": word_comparisons,
            "total_words": total_words,
            "matched_words": matched_words,
            "mismatched_words": mismatched_words
        }
    
    def _fuzzy_compare_words(self, recognized_words: List[str], verse_words: List[str]) -> tuple:
        """
        Compare words using fuzzy matching algorithm.
        Allows for minor spelling variations and word order flexibility.
        
        Returns:
            (word_comparisons, matched_words, mismatched_words)
        """
        word_comparisons = []
        matched_words = 0
        mismatched_words = 0
        
        # Track which verse words have been matched
        verse_matched = [False] * len(verse_words)
        
        # First pass: exact and high-similarity matches
        for i, verse_word in enumerate(verse_words):
            best_match_idx = None
            best_similarity = 0.0
            
            # Look for matches in a window around the expected position
            start_idx = max(0, i - self.max_word_distance)
            end_idx = min(len(recognized_words), i + self.max_word_distance + 1)
            
            for j in range(start_idx, end_idx):
                if j < len(recognized_words):
                    recognized_word = recognized_words[j]
                    
                    # Calculate similarity
                    similarity = self._word_similarity(verse_word, recognized_word)
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match_idx = j
            
            # Check if match is good enough
            is_match = best_similarity >= self.similarity_threshold
            
            if is_match and best_match_idx is not None:
                matched_words += 1
                verse_matched[i] = True
                recognized_word = recognized_words[best_match_idx]
            else:
                mismatched_words += 1
                recognized_word = None
            
            word_comparisons.append({
                "position": i,
                "recognized": recognized_word or "",
                "verse": verse_word,
                "match": is_match,
                "similarity": round(best_similarity * 100, 1) if best_match_idx is not None else 0.0
            })
        
        # Second pass: handle unmatched recognized words
        unmatched_recognized = []
        for j, recognized_word in enumerate(recognized_words):
            # Check if this word was matched in first pass
            was_matched = False
            for comp in word_comparisons:
                if comp.get("recognized") == recognized_word and comp.get("match"):
                    # Find which position this matched word came from
                    if j < len(recognized_words):
                        was_matched = True
                        break
            
            if not was_matched:
                unmatched_recognized.append((j, recognized_word))
        
        # Add unmatched recognized words as extra
        for j, recognized_word in unmatched_recognized:
            word_comparisons.append({
                "position": len(word_comparisons),
                "recognized": recognized_word,
                "verse": "",
                "match": False,
                "similarity": 0.0
            })
        
        return word_comparisons, matched_words, mismatched_words
    
    def _word_similarity(self, word1: str, word2: str) -> float:
        """
        Calculate similarity between two words (0.0 to 1.0).
        Uses multiple methods for better accuracy.
        """
        if not word1 or not word2:
            return 0.0
        
        # Exact match
        if word1 == word2:
            return 1.0
        
        # Normalize for comparison (remove extra spaces)
        word1 = word1.strip()
        word2 = word2.strip()
        
        # Use SequenceMatcher for similarity
        similarity = SequenceMatcher(None, word1, word2).ratio()
        
        # Boost similarity if words are similar length
        length_ratio = min(len(word1), len(word2)) / max(len(word1), len(word2)) if max(len(word1), len(word2)) > 0 else 0
        similarity = (similarity * 0.7) + (length_ratio * 0.3)
        
        # Check for common prefixes/suffixes
        if word1.startswith(word2[:min(3, len(word2))]) or word2.startswith(word1[:min(3, len(word1))]):
            similarity = max(similarity, 0.6)
        
        return similarity
    
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

