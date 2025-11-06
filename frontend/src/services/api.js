import axios from 'axios';
import Constants from 'expo-constants';

// Get API URL from environment or use default
// For mobile, you may need to use your Mac's IP address instead of localhost
const API_BASE_URL = Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const transcriptionAPI = {
  /**
   * Transcribe audio file
   * @param {FormData} formData - FormData containing audio file
   * @returns {Promise<Object>} Transcription result with text and confidence
   */
  transcribeAudio: async (formData) => {
    try {
      const response = await apiClient.post('/transcribe_audio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Transcription error:', error);
      throw new Error(
        error.response?.data?.detail || 'Failed to transcribe audio'
      );
    }
  },
};

export const comparisonAPI = {
  /**
   * Compare recognized text with verse
   * @param {string} recognizedText - Text recognized from audio
   * @param {string} verseText - Reference verse text
   * @param {string} verseReference - Optional verse reference (e.g., "1:1")
   * @returns {Promise<Object>} Comparison result with match data
   */
  compareVerse: async (recognizedText, verseText, verseReference = '') => {
    try {
      const response = await apiClient.post('/compare_verse', {
        recognized_text: recognizedText,
        verse_text: verseText,
        verse_reference: verseReference,
      });
      return response.data;
    } catch (error) {
      console.error('Comparison error:', error);
      throw new Error(
        error.response?.data?.detail || 'Failed to compare verse'
      );
    }
  },
};

export default apiClient;

