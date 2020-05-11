import * as React from 'react';
import { Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import PokePage from './components/PokePage';
import SetupPage from './components/SetupPage';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Setup" component={SetupPage} />
        <Tab.Screen name="Send Poke" component={PokePage} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}