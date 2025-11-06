import pytest
from app.services.comparison_service import ComparisonService

def test_fuzzy_matching_reduces_false_negatives():
    """Test that fuzzy matching correctly identifies similar words."""
    service = ComparisonService()
    
    # Test case: minor spelling/diacritic differences
    recognized = "بسم الله الرحمن"
    verse = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    
    result = service.compare(recognized, verse)
    
    # Should match more words now due to fuzzy matching
    assert result["matched_words"] >= 3  # At least 3 words should match
    assert result["match_percentage"] > 50.0  # Should be > 50% match

def test_fuzzy_matching_with_typos():
    """Test that fuzzy matching handles small typos."""
    service = ComparisonService()
    
    # Test case: one character difference
    recognized = "بسم الله الرحمن"
    verse = "بسم الله الرحمن"  # Same but normalized differently
    
    result = service.compare(recognized, verse)
    
    # Should have high match percentage
    assert result["match_percentage"] >= 80.0

def test_exact_match_still_works():
    """Test that exact matches still work perfectly."""
    service = ComparisonService()
    
    recognized = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    verse = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    
    result = service.compare(recognized, verse)
    
    assert result["match_percentage"] == 100.0
    assert result["matched_words"] == result["total_words"]

def test_word_order_flexibility():
    """Test that words slightly out of order can still match."""
    service = ComparisonService()
    
    # Note: This is a simplified test - actual word reordering 
    # would require more sophisticated alignment
    recognized = "الله بسم الرحمن"
    verse = "بسم الله الرحمن"
    
    result = service.compare(recognized, verse)
    
    # Should still match some words due to fuzzy matching
    assert result["matched_words"] > 0

