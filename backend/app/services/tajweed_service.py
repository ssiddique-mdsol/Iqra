from typing import Optional

class TajweedService:
    """
    Service for adding tajweed (diacritics) to Arabic text.
    Uses Mishkal library for automatic diacritization.
    """
    
    def __init__(self):
        self.mishkal = None
        try:
            from mishkal.tashkeel import TashkeelClass
            self.mishkal = TashkeelClass()
            self.available = True
        except ImportError:
            print("Warning: Mishkal not available. Tajweed will use fallback method.")
            self.available = False
    
    def add_tajweed(self, text: str) -> str:
        """
        Add tajweed (diacritics) to Arabic text.
        
        Args:
            text: Arabic text without diacritics
            
        Returns:
            Arabic text with diacritics added
        """
        if not text or not text.strip():
            return text
        
        # Remove existing diacritics first
        text = self._remove_diacritics(text)
        
        if self.available and self.mishkal:
            try:
                # Use Mishkal for diacritization
                diacritized = self.mishkal.tashkeel(text)
                return diacritized
            except Exception as e:
                print(f"Error in Mishkal diacritization: {e}")
                return self._fallback_tajweed(text)
        else:
            return self._fallback_tajweed(text)
    
    def _remove_diacritics(self, text: str) -> str:
        """Remove existing diacritics from text."""
        diacritics = "ًٌٍَُِّْٰۖۗۘۙۚۛۜ"
        return "".join(char for char in text if char not in diacritics)
    
    def _fallback_tajweed(self, text: str) -> str:
        """
        Fallback method: Add basic common diacritics based on patterns.
        This is a simplified version - Mishkal provides better results.
        """
        # Common patterns for basic tajweed
        # This is a very basic implementation
        # For production, use Mishkal or a proper tajweed API
        
        # Common word patterns with diacritics
        patterns = {
            "بسم": "بِسْمِ",
            "الله": "اللَّهِ",
            "الرحمن": "الرَّحْمَٰنِ",
            "الرحيم": "الرَّحِيمِ",
            "الحمد": "الْحَمْدُ",
            "رب": "رَبِّ",
            "العالمين": "الْعَالَمِينَ",
            "مالك": "مَالِكِ",
            "يوم": "يَوْمِ",
            "الدين": "الدِّينِ",
            "إياك": "إِيَّاكَ",
            "نعبد": "نَعْبُدُ",
            "نستعين": "نَسْتَعِينُ",
            "اهدنا": "اهْدِنَا",
            "الصراط": "الصِّرَاطَ",
            "المستقيم": "الْمُسْتَقِيمَ",
            "صراط": "صِرَاطَ",
            "الذين": "الَّذِينَ",
            "أنعمت": "أَنْعَمْتَ",
            "عليهم": "عَلَيْهِمْ",
            "غير": "غَيْرِ",
            "المغضوب": "الْمَغْضُوبِ",
            "عليهم": "عَلَيْهِمْ",
            "ولا": "وَلَا",
            "الضالين": "الضَّالِّينَ",
            "قل": "قُلْ",
            "هو": "هُوَ",
            "أحد": "أَحَدٌ",
            "الصمد": "الصَّمَدُ",
            "لم": "لَمْ",
            "يلد": "يَلِدْ",
            "يولد": "يُولَدْ",
            "ولم": "وَلَمْ",
            "يكن": "يَكُنْ",
            "له": "لَهُ",
            "كفوا": "كُفُوًا",
            "أعوذ": "أَعُوذُ",
            "برب": "بِرَبِّ",
            "الفلق": "الْفَلَقِ",
            "من": "مِنْ",
            "شر": "شَرِّ",
            "ما": "مَا",
            "خلق": "خَلَقَ",
            "الناس": "النَّاسِ",
            "ملك": "مَلِكِ",
            "إله": "إِلَٰهِ",
        }
        
        # Try to match patterns
        result = text
        for pattern, diacritized in patterns.items():
            if pattern in result:
                # Simple replacement (this is basic - proper implementation needs word boundaries)
                result = result.replace(pattern, diacritized)
        
        return result if result != text else text

