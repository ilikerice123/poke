import React from 'react';
import { StyleSheet, Text, View, TextInput } from 'react-native';
import PokePage from './components/PokePage'

export default function App() {
  return (
    <View style={styles.container}>
      <PokePage />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
