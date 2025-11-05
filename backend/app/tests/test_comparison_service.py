import pytest
from app.services.comparison_service import ComparisonService

def test_compare_exact_match():
    """Test comparison with exact match."""
    service = ComparisonService()
    
    recognized = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    verse = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    
    result = service.compare(recognized, verse)
    
    assert result["match_percentage"] == 100.0
    assert result["matched_words"] == result["total_words"]
    assert result["mismatched_words"] == 0

def test_compare_partial_match():
    """Test comparison with partial match."""
    service = ComparisonService()
    
    recognized = "بِسْمِ اللَّهِ الرَّحِيمِ"
    verse = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    
    result = service.compare(recognized, verse)
    
    assert result["match_percentage"] < 100.0
    assert result["matched_words"] > 0
    assert result["mismatched_words"] > 0

def test_compare_no_match():
    """Test comparison with no match."""
    service = ComparisonService()
    
    recognized = "الْحَمْدُ لِلَّهِ"
    verse = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    
    result = service.compare(recognized, verse)
    
    assert result["match_percentage"] < 100.0
    assert result["total_words"] > 0

