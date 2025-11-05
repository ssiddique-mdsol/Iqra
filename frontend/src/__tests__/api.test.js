import { transcriptionAPI, comparisonAPI } from '../services/api';
import axios from 'axios';

jest.mock('axios');

describe('API Services', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('transcriptionAPI', () => {
    it('should transcribe audio successfully', async () => {
      const mockResponse = {
        data: {
          success: true,
          text: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ',
          confidence: 0.85,
        },
      };

      axios.create.mockReturnValue({
        post: jest.fn().mockResolvedValue(mockResponse),
      });

      const formData = new FormData();
      formData.append('audio_file', { uri: 'test.mp3', type: 'audio/mp3' });

      const result = await transcriptionAPI.transcribeAudio(formData);

      expect(result.success).toBe(true);
      expect(result.text).toBeDefined();
      expect(result.confidence).toBeDefined();
    });

    it('should handle transcription errors', async () => {
      axios.create.mockReturnValue({
        post: jest.fn().mockRejectedValue({
          response: {
            data: {
              detail: 'Failed to transcribe audio',
            },
          },
        }),
      });

      const formData = new FormData();
      formData.append('audio_file', { uri: 'test.mp3', type: 'audio/mp3' });

      await expect(transcriptionAPI.transcribeAudio(formData)).rejects.toThrow(
        'Failed to transcribe audio'
      );
    });
  });

  describe('comparisonAPI', () => {
    it('should compare verse successfully', async () => {
      const mockResponse = {
        data: {
          success: true,
          match_percentage: 100.0,
          word_comparisons: [],
          total_words: 4,
          matched_words: 4,
          mismatched_words: 0,
        },
      };

      axios.create.mockReturnValue({
        post: jest.fn().mockResolvedValue(mockResponse),
      });

      const result = await comparisonAPI.compareVerse(
        'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ',
        'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ',
        '1:1'
      );

      expect(result.success).toBe(true);
      expect(result.match_percentage).toBe(100.0);
      expect(result.word_comparisons).toBeDefined();
    });

    it('should handle comparison errors', async () => {
      axios.create.mockReturnValue({
        post: jest.fn().mockRejectedValue({
          response: {
            data: {
              detail: 'Failed to compare verse',
            },
          },
        }),
      });

      await expect(
        comparisonAPI.compareVerse('text1', 'text2')
      ).rejects.toThrow('Failed to compare verse');
    });
  });
});

