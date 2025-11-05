import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import HomeScreen from '../screens/HomeScreen';
import { transcriptionAPI } from '../services/api';

// Mock the API
jest.mock('../services/api', () => ({
  transcriptionAPI: {
    transcribeAudio: jest.fn(),
  },
}));

// Mock expo-av
jest.mock('expo-av', () => ({
  Audio: {
    requestPermissionsAsync: jest.fn(() => Promise.resolve({ status: 'granted' })),
    setAudioModeAsync: jest.fn(),
    Recording: {
      createAsync: jest.fn(() =>
        Promise.resolve({
          recording: {
            stopAndUnloadAsync: jest.fn(),
            getURI: jest.fn(() => 'test://audio.m4a'),
          },
        })
      ),
      OptionsPresets: {
        HIGH_QUALITY: {},
      },
    },
  },
}));

const mockNavigation = {
  navigate: jest.fn(),
};

describe('HomeScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render correctly', () => {
    const { getByText } = render(<HomeScreen navigation={mockNavigation} />);
    expect(getByText('Iqra')).toBeTruthy();
    expect(getByText('Quran Recitation Practice')).toBeTruthy();
    expect(getByText('Start Recording')).toBeTruthy();
  });

  it('should start recording when button is pressed', async () => {
    const { getByText } = render(<HomeScreen navigation={mockNavigation} />);
    const recordButton = getByText('Start Recording');

    fireEvent.press(recordButton);

    await waitFor(() => {
      expect(getByText('Stop Recording')).toBeTruthy();
    });
  });

  it('should transcribe audio after stopping recording', async () => {
    transcriptionAPI.transcribeAudio.mockResolvedValue({
      text: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ',
      confidence: 0.85,
    });

    const { getByText } = render(<HomeScreen navigation={mockNavigation} />);
    const recordButton = getByText('Start Recording');

    // Start recording
    fireEvent.press(recordButton);

    await waitFor(() => {
      expect(getByText('Stop Recording')).toBeTruthy();
    });

    // Stop recording
    const stopButton = getByText('Stop Recording');
    fireEvent.press(stopButton);

    await waitFor(() => {
      expect(transcriptionAPI.transcribeAudio).toHaveBeenCalled();
    });
  });
});

