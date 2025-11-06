import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  ScrollView,
} from 'react-native';
import { Audio } from 'expo-av';
import Constants from 'expo-constants';
import { transcriptionAPI } from '../services/api';

export default function HomeScreen({ navigation }) {
  const [recording, setRecording] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [transcribedText, setTranscribedText] = useState('');
  const [isTranscribing, setIsTranscribing] = useState(false);

  async function startRecording() {
    try {
      console.log('[Mobile] Requesting audio permissions...');
      const permission = await Audio.requestPermissionsAsync();
      console.log('[Mobile] Permission status:', permission.status);
      
      if (permission.status !== 'granted') {
        Alert.alert('Permission Required', 'Please grant microphone permission');
        return;
      }

      console.log('[Mobile] Setting audio mode...');
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
        staysActiveInBackground: false,
      });

      console.log('[Mobile] Creating recording with optimized settings...');
      // Use optimized recording settings for Arabic speech recognition
      // Simplified settings that work across all platforms
      const recordingOptions = {
        android: {
          extension: '.m4a',
          outputFormat: Audio.AndroidOutputFormat.MPEG_4,
          audioEncoder: Audio.AndroidAudioEncoder.AAC,
          sampleRate: 16000,
          numberOfChannels: 1,
          bitRate: 64000,
        },
        ios: {
          extension: '.m4a',
          outputFormat: Audio.IOSOutputFormat.MPEG4AAC,
          audioQuality: Audio.IOSAudioQuality.HIGH,
          sampleRate: 16000,
          numberOfChannels: 1,
          // Note: bitRate is not valid for iOS MPEG4AAC format
        },
        web: {
          mimeType: 'audio/webm',
          bitsPerSecond: 64000,
        },
      };
      
      console.log('[Mobile] Recording options:', JSON.stringify(recordingOptions, null, 2));
      const { recording: newRecording } = await Audio.Recording.createAsync(recordingOptions);
      
      console.log('[Mobile] ✅ Recording started successfully');
      setRecording(newRecording);
      setIsRecording(true);
    } catch (err) {
      console.error('[Mobile] ❌ Failed to start recording:', err);
      console.error('[Mobile] Error details:', JSON.stringify(err, null, 2));
      Alert.alert(
        'Recording Error', 
        `Failed to start recording: ${err.message || 'Unknown error'}\n\nCheck console for details.`
      );
    }
  }

  async function stopRecording() {
    if (!recording) return;

    setIsRecording(false);
    await recording.stopAndUnloadAsync();
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
    });

    const uri = recording.getURI();
    setRecording(null);

    // Transcribe the audio
    if (uri) {
      await transcribeAudio(uri);
    }
  }

  async function transcribeAudio(uri) {
    setIsTranscribing(true);
    try {
      console.log('[Mobile] Starting transcription for:', uri);
      
      // For React Native, FormData needs special handling
      const formData = new FormData();
      
      // React Native FormData format - must use this exact structure
      formData.append('audio_file', {
        uri: uri,
        type: 'audio/m4a',
        name: `recording_${Date.now()}.m4a`,
      });

      console.log('[Mobile] FormData created, sending to backend...');
      console.log('[Mobile] API URL:', Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8000');
      
      const result = await transcriptionAPI.transcribeAudio(formData);
      
      console.log('[Mobile] ✅ Transcription result:', result);
      console.log('[Mobile] ✅ Transcribed text:', result.text);
      
      if (!result.text || result.text.trim().length === 0) {
        console.warn('[Mobile] ⚠️  Warning: Transcription result is empty!');
        Alert.alert('Warning', 'Transcription returned empty text. Please try recording again.');
      }
      
      setTranscribedText(result.text);

      // Navigate to comparison screen if text is available
      if (result.text && result.text.trim()) {
        navigation.navigate('Comparison', {
          recognizedText: result.text,
        });
      }
    } catch (error) {
      Alert.alert('Transcription Error', error.message);
    } finally {
      setIsTranscribing(false);
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Iqra</Text>
        <Text style={styles.subtitle}>Quran Recitation Practice</Text>

        <View style={styles.recordingSection}>
          <TouchableOpacity
            style={[styles.recordButton, isRecording && styles.recordButtonActive]}
            onPress={isRecording ? stopRecording : startRecording}
            disabled={isTranscribing}
          >
            <Text style={styles.recordButtonText}>
              {isRecording ? 'Stop Recording' : 'Start Recording'}
            </Text>
          </TouchableOpacity>

          {isTranscribing && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#007AFF" />
              <Text style={styles.loadingText}>Transcribing audio...</Text>
            </View>
          )}
        </View>

        {transcribedText ? (
          <View style={styles.transcriptionSection}>
            <Text style={styles.sectionTitle}>Recognized Text:</Text>
            <View style={styles.textBox}>
              <Text style={styles.transcribedText}>{transcribedText}</Text>
            </View>
          </View>
        ) : (
          <View style={styles.placeholderSection}>
            <Text style={styles.placeholderText}>
              Record your recitation to get started
            </Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    color: '#7f8c8d',
    marginBottom: 40,
    textAlign: 'center',
  },
  recordingSection: {
    width: '100%',
    alignItems: 'center',
    marginBottom: 30,
  },
  recordButton: {
    backgroundColor: '#007AFF',
    paddingVertical: 20,
    paddingHorizontal: 40,
    borderRadius: 30,
    minWidth: 200,
    alignItems: 'center',
  },
  recordButtonActive: {
    backgroundColor: '#FF3B30',
  },
  recordButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  loadingContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    color: '#7f8c8d',
    fontSize: 14,
  },
  transcriptionSection: {
    width: '100%',
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 10,
  },
  textBox: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    minHeight: 100,
  },
  transcribedText: {
    fontSize: 18,
    color: '#2c3e50',
    textAlign: 'center',
    lineHeight: 28,
  },
  placeholderSection: {
    marginTop: 40,
    padding: 20,
  },
  placeholderText: {
    fontSize: 16,
    color: '#95a5a6',
    textAlign: 'center',
    fontStyle: 'italic',
  },
});

