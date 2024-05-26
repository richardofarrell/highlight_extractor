import React, { useState } from 'react';
import { Button, Image, View } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import Constants from 'expo-constants';
import * as FileSystem from 'expo-file-system';

export default function CaptureImage() {
  const [image, setImage] = useState(null);
  const [highlightedText, setHighlightedText] = useState('');

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.uri);
      const formData = new FormData();
      formData.append('file', {
        uri: result.uri,
        name: 'photo.jpg',
        type: 'image/jpeg',
      });

      fetch('http://your_backend_ip:5000/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => response.json())
      .then((data) => {
        setHighlightedText(data.highlighted_text);
      })
      .catch((error) => {
        console.error(error);
      });
    }
  };

  return (
    <View>
      <Button title="Pick an image from camera roll" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
      {highlightedText ? <Text>Highlighted Text: {highlightedText}</Text> : null}
    </View>
  );
}
