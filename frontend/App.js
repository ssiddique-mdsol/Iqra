import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './src/screens/HomeScreen';
import ComparisonScreen from './src/screens/ComparisonScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ title: 'Iqra - Quran Recitation' }}
        />
        <Stack.Screen 
          name="Comparison" 
          component={ComparisonScreen}
          options={{ title: 'Verse Comparison' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

