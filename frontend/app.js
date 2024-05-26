import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import CaptureImage from './CaptureImage';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Highlight Text Extractor</Text>
      <CaptureImage />
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
