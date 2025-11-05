import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { comparisonAPI } from '../services/api';

export default function ComparisonScreen({ route, navigation }) {
  const { recognizedText } = route.params || {};
  const [verseText, setVerseText] = useState('بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ');
  const [verseReference, setVerseReference] = useState('1:1');
  const [comparisonResult, setComparisonResult] = useState(null);
  const [isComparing, setIsComparing] = useState(false);

  useEffect(() => {
    if (recognizedText) {
      performComparison();
    }
  }, []);

  async function performComparison() {
    if (!recognizedText || !verseText.trim()) {
      Alert.alert('Error', 'Please provide both recognized text and verse text');
      return;
    }

    setIsComparing(true);
    try {
      const result = await comparisonAPI.compareVerse(
        recognizedText,
        verseText,
        verseReference
      );
      setComparisonResult(result);
    } catch (error) {
      Alert.alert('Comparison Error', error.message);
    } finally {
      setIsComparing(false);
    }
  }

  const renderWordComparison = () => {
    if (!comparisonResult || !comparisonResult.word_comparisons) {
      return null;
    }

    return comparisonResult.word_comparisons.map((item, index) => {
      const isMatch = item.match;
      return (
        <View
          key={index}
          style={[
            styles.wordContainer,
            isMatch ? styles.wordMatch : styles.wordMismatch,
          ]}
        >
          <Text
            style={[
              styles.wordText,
              isMatch ? styles.wordTextMatch : styles.wordTextMismatch,
            ]}
          >
            {item.recognized || item.verse || '—'}
          </Text>
          {!isMatch && item.verse && (
            <Text style={styles.expectedText}>Expected: {item.verse}</Text>
          )}
        </View>
      );
    });
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recognized Text</Text>
        <View style={styles.textBox}>
          <Text style={styles.text}>{recognizedText || 'No text available'}</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Verse Text</Text>
        <TextInput
          style={styles.input}
          value={verseText}
          onChangeText={setVerseText}
          multiline
          placeholder="Enter verse text"
          textAlignVertical="top"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Verse Reference (Optional)</Text>
        <TextInput
          style={styles.inputReference}
          value={verseReference}
          onChangeText={setVerseReference}
          placeholder="e.g., 1:1"
        />
      </View>

      <TouchableOpacity
        style={styles.compareButton}
        onPress={performComparison}
        disabled={isComparing}
      >
        {isComparing ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.compareButtonText}>Compare</Text>
        )}
      </TouchableOpacity>

      {comparisonResult && (
        <View style={styles.resultSection}>
          <View style={styles.resultHeader}>
            <Text style={styles.resultTitle}>Comparison Result</Text>
            <Text style={styles.matchPercentage}>
              {comparisonResult.match_percentage.toFixed(1)}% Match
            </Text>
          </View>

          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{comparisonResult.matched_words}</Text>
              <Text style={styles.statLabel}>Matched</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{comparisonResult.mismatched_words}</Text>
              <Text style={styles.statLabel}>Mismatched</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{comparisonResult.total_words}</Text>
              <Text style={styles.statLabel}>Total</Text>
            </View>
          </View>

          <View style={styles.wordComparisonSection}>
            <Text style={styles.wordComparisonTitle}>Word-by-Word Comparison</Text>
            <View style={styles.wordsContainer}>
              {renderWordComparison()}
            </View>
          </View>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    padding: 20,
  },
  section: {
    marginBottom: 20,
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
    minHeight: 80,
  },
  text: {
    fontSize: 18,
    color: '#2c3e50',
    textAlign: 'center',
    lineHeight: 28,
  },
  input: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    minHeight: 80,
    fontSize: 18,
    color: '#2c3e50',
    textAlign: 'center',
  },
  inputReference: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    fontSize: 16,
    color: '#2c3e50',
  },
  compareButton: {
    backgroundColor: '#007AFF',
    paddingVertical: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 20,
  },
  compareButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  resultSection: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  resultTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  matchPercentage: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#27ae60',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
    paddingVertical: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 10,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  statLabel: {
    fontSize: 12,
    color: '#7f8c8d',
    marginTop: 5,
  },
  wordComparisonSection: {
    marginTop: 10,
  },
  wordComparisonTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 10,
  },
  wordsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  wordContainer: {
    padding: 8,
    borderRadius: 6,
    marginBottom: 8,
    marginRight: 8,
  },
  wordMatch: {
    backgroundColor: '#d4edda',
    borderWidth: 1,
    borderColor: '#c3e6cb',
  },
  wordMismatch: {
    backgroundColor: '#f8d7da',
    borderWidth: 1,
    borderColor: '#f5c6cb',
  },
  wordText: {
    fontSize: 16,
  },
  wordTextMatch: {
    color: '#155724',
  },
  wordTextMismatch: {
    color: '#721c24',
  },
  expectedText: {
    fontSize: 12,
    color: '#721c24',
    marginTop: 4,
    fontStyle: 'italic',
  },
});

