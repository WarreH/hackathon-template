import { useNavigation } from '@react-navigation/native';
import { Button, Image, Text, View, XStack, YStack } from 'tamagui';
import React, { useEffect, useRef, useState } from 'react';
import { useCameraPermissions, Camera, CameraView, CameraType } from 'expo-camera';
import { ActivityIndicator, TouchableOpacity } from 'react-native';

import { AntDesign, Entypo, MaterialIcons } from '@expo/vector-icons'
import * as Location from 'expo-location'
import AsyncStorage from '@react-native-async-storage/async-storage';

// Dummy data for the cards
const cardData = [
  {
    id: 1,
    title: 'Card 1',
    description: 'This is a description for card 1',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 2,
    title: 'Card 2',
    description: 'This is a description for card 2',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 3,
    title: 'Card 3',
    description: 'This is a description for card 3',
    imageUrl: 'https://via.placeholder.com/150',
  },
];

export default function HomeScreen() {
  const navigation = useNavigation();
  const [permission, requestPermission] = useCameraPermissions(); // Camera permissions hook
  const [photoUri, setPhotoUri] = useState(null); // To store the photo URI after capturing
  const cameraRef = useRef<any>(null);
  const [takingPic,setTakingPic] = useState(false);
  const [picId,setPicId] = useState<any>(null);
  const [loading, setLoading] = useState(false)
  const [resultImageUrl, setResultImageUrl] = useState<string | null>(null)
  const [places, setPlaces] = useState<any[]>(cardData)

const [interests, setInterests] = useState<any[]>([])
async function fetchRecommendations() {
  try {
    // Ask for permission
    const { status } = await Location.requestForegroundPermissionsAsync()
    if (status !== 'granted') {
      throw new Error('Location permission not granted')
    }

    // Get current location
    const location = await Location.getCurrentPositionAsync({})
    const { latitude, longitude } = location.coords

    // Build the request body
    const body = {
      location: {
        latitude: latitude,
        longitude: longitude
      },
      user_identifier: 'example_user',
      interests: interests,
    }

    // Fetch data using POST method and send the body in JSON format
    const response = await fetch('http://192.168.84.177:8080/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      throw new Error('Failed to fetch recommendations')
    }

    const data = await response.json()
    console.log('Received:', data)
    setPlaces(data) // This will update the state with the fetched places

  } catch (error) {
    console.error('Error fetching location-based recommendations:', error)
  }
}

const fetchList = async () => {
  try {
    const storedList = await AsyncStorage.getItem('@interests');
    if (storedList !== null) {
      // Parse the JSON string back into an array
const    list =  JSON.parse(storedList);
setInterests(list)
    } else {
      console.log('No list found in storage');
      return [];
    }
  } catch (error) {
    console.error('Error fetching list', error);
    return [];
  }
};
useEffect(()=>{
 fetchList().then(()=>{
  // setInterval(()=>{
  //   console.log("Fetching")
  //   fetchRecommendations()
  // },10000)
 })

},[])

  const handleTakePicture = async (id:any) => {
    console.log('Taking picture...');
    // You can use expo-camera's takePictureAsync here.
    console.log('Button Pressed');

     if (cameraRef.current) {
      try {
        setLoading(true)
        const options = { quality: 0.1, fixOrientation: true, 
          exif: true};
          await cameraRef.current.takePictureAsync(options).then((photo:any) => {
             photo.exif.Orientation = 1;            
              console.log(photo);            
              }); 
              const photo = await cameraRef.current.takePictureAsync()
              console.log('Photo taken:', photo.uri)
        
              const userIdentifier = 'example_user' // <-- Replace with actual user ID
        
              // Convert image to blob
              const imageUri = photo.uri
              const fileName = imageUri.split('/').pop() || 'photo.jpg'
              const match = /\.(\w+)$/.exec(fileName)
              const fileType = match ? `image/${match[1]}` : 'image/jpeg'
        
              const file = {
                uri: imageUri,
                name: fileName,
                type: fileType,
              }
        
              // Construct form data
              const formData = new FormData()
              formData.append('file', file as any)
        
              // Send to API
              const response = await fetch(`http://192.168.84.177:8080/picture/${userIdentifier}`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'multipart/form-data',
                },
                body: formData,
              })
        
              if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`)
              }
        
              const fileIdentifier = await (await response.text()).replaceAll('"','')
              console.log('Uploaded file identifier:', fileIdentifier)
        
              // Optional: use a fixed temp image for now
              const tempUrl = 'http://192.168.84.177:8080/picture/'+fileIdentifier;
              setResultImageUrl(tempUrl)
              console.log(tempUrl)
            } catch (error) {
              console.error('Error taking/uploading picture:', error)
            } finally {
              setLoading(false)
            }
        // Simulate image processing delay
        // TODO: replace with api logic
       
     
    }
  };

  const handleCardClick = (cardId: number) => {
    console.log('Navigating to detail page for card:', cardId);
    // Implement navigation to the detail page here
    navigation.navigate('DetailPage', { cardId });
  };


  const [facing, setFacing] = useState<CameraType>('back');
  function toggleCameraFacing() {
    console.log("flip")
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  }
  return (
    <YStack flex={1} gap="$4" paddingHorizontal="$5">
      {/* Title */}
      <Text fontSize={32} fontWeight="700">
        Home Screen
      </Text>

      {/* Small Header */}
      <Text fontSize={18} color="gray10">
        Choose a card to view more details
      </Text>

      {!permission || !permission.granted &&  <View>
        <Text>We need your permission to show the camera</Text>
        <Button onPress={requestPermission}>Grant Permission</Button>
      </View>}

      {/* List of Cards */}
     { !takingPic &&
       <YStack rowGap="$3">
       {places.map((card) => (
         <XStack
           key={card.id}
           backgroundColor="$background"
           borderRadius="$7"
           elevation="$2"
           padding="$4"
           gap="$4"
           onPress={() => handleCardClick(card.id)}
           verticalAlign="center"
           alignItems="center"
           justifyContent="space-between"
         >
           {/* Image */}
           {/* <Image source={{ uri: card.imageUrl }} width={100} height={100} /> */}

           {/* Card Content */}
           <YStack flex={1} verticalAlign="flex-start">
             <Text fontSize={18} fontWeight="600">{card.name} - {Math.round(card.distance)}km</Text>
             <Text fontSize={14} color="gray10">{card.description}</Text>
           </YStack>

           {/* Camera Icon */}
           <Button onPress={() =>    {setTakingPic(true); setPicId(card.id)}} circular size="$6" theme="light">
             <AntDesign name="camera" size={24} color="black" />
           </Button>
         </XStack>
       ))}
     </YStack>
     }

      {/* Show the captured photo (if any) 
      {photoUri && (
        <YStack space="$4" ai="center">
          <Text fontSize={18}>Your captured photo:</Text>
          <Image source={{ uri: photoUri }} width={200} height={200} borderRadius={10} />
        </YStack>
      )}*/}
       {/* Camera view (hidden for now) */}
       {takingPic &&  <View flex={1} position="relative">
      {resultImageUrl ? (
       <YStack flex={1} justifyContent="center" alignItems="center" padding="$4" position="relative">
       {/* Image Fullscreen */}
       <Image
         source={{ uri: resultImageUrl }}
         width="100%"
         height="100%"
         borderRadius={12}
       />
     
       {/* Button on Top */}
       <TouchableOpacity
         onPress={() => {
           setTakingPic(false);
           setResultImageUrl(null);
         }}
         style={{
           position: 'absolute',
           bottom: 30,
           alignSelf: 'center',
         }}
       >
         <AntDesign name="checkcircle" size={48} color="green" />
       </TouchableOpacity>
     </YStack>
     
      ) : (
        <>
          <CameraView
            ref={cameraRef}
            facing={facing}
            style={{ flex: 1, borderRadius: 20, overflow: 'hidden' }}
          />

          {/* Top Controls */}
          <View
            position="absolute"
            top={20}
            left={20}
            right={20}
            flexDirection="row"
            justifyContent="space-between"
            alignItems="center"
          >
            <TouchableOpacity onPress={()=>setTakingPic(false)}>
              <AntDesign name="closecircle" size={32} color="white" />
            </TouchableOpacity>
            <TouchableOpacity onPress={toggleCameraFacing}>
              <MaterialIcons name="flip-camera-ios" size={32} color="white" />
            </TouchableOpacity>
          </View>

          {/* Loader or Capture Button */}
          <View
            position="absolute"
            bottom={40}
            left={0}
            right={0}
            alignItems="center"
            justifyContent="center"
          >
            {loading ? (
              <ActivityIndicator size="large" color="#fff" />
            ) : (
              <TouchableOpacity
                onPress={handleTakePicture}
                style={{
                  width: 70,
                  height: 70,
                  borderRadius: 35,
                  backgroundColor: 'white',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Entypo name="camera" size={30} color="black" />
              </TouchableOpacity>
            )}
          </View>
        </>
      )}
    </View>}
       
    </YStack>
  );
}
