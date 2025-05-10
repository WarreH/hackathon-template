import { useNavigation } from '@react-navigation/native'
import { useEffect, useState } from 'react'
import { Button, Input, Text, XStack, YStack } from 'tamagui'

const defaultInterests = ['Music', 'Art', 'Travel', 'Tech', 'Fitness']
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function StartScreen() {
  const navigation = useNavigation()
  const [interests, setInterests] = useState(defaultInterests)
  const [selected, setSelected] = useState<string[]>([])
  const [newInterest, setNewInterest] = useState('')


const storeList = async (list: string[]) => {
  try {
    // Convert the list into a JSON string and store it
    await AsyncStorage.setItem('@interests', JSON.stringify(list));
    console.log('List stored successfully');
  } catch (error) {
    console.error('Error storing list', error);
  }
};

  const toggleInterest = (interest: string) => {
    console.log('Toggling interest:', interest)
    setSelected((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    )
  }

  const addInterest = () => {
    console.log('Adding new interest:', newInterest)
    const trimmed = newInterest.trim()
    if (trimmed && !interests.includes(trimmed)) {
      setInterests((prev) => [...prev, trimmed])
      setNewInterest('')
      toggleInterest(trimmed)
    }
  }
  const fetchList = async () => {
    try {
      const storedList = await AsyncStorage.getItem('@interests');
      if (storedList !== null) {
        // Parse the JSON string back into an array
  const    list =  JSON.parse(storedList);
  return list
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
    fetchList().then((list)=>{
        if(list.length > 0){
          navigation.navigate('MainTabs')
        }
    })
  })
  const start = ()=>{
    // Save interests somewhere
    console.log(interests)
    storeList(interests)
    // Navigate into main
    navigation.navigate('MainTabs')
  }

  return (
    <YStack  space="$6" p="$4" gap="$5">
      <Text fontSize={24} fontWeight="700">NorthStarCompass: Start your journey</Text>
      <Text fontSize={16} color="gray10">Select your interests:</Text>

     <XStack
        justifyContent="center"
        
        flex={1}
        flexWrap="wrap"
        gap="$1"

        width="100%"
        
      >
        {interests && interests.map((interest) => {
          const isSelected = selected.includes(interest)
          console.log('Interest selected:', interest, isSelected) // Log to check interest states
          return (
            
            <Button
              key={interest}
              onPress={() => toggleInterest(interest)}
              {...!isSelected?{variant:'outlined'}:{}}
              px="$4"
              py="$1.5"
            >
              {interest}
            </Button>
          )
        })}
      </XStack>

      <XStack gap="$3" flex={1} justify="center" mt="$4">
          <Input
            placeholder="Add interest"
            value={newInterest}
            onChangeText={setNewInterest}
            size="$3"
            width={180}
          />
          <Button size="$3" onPress={addInterest}>
            Add
          </Button>
        </XStack>
       <XStack flex={1} justify="center">
       <Button
        mt="$6"
        size="$4"
        width={180}
        disabled={selected.length === 0}
        opacity={selected.length === 0 ? 0.5 : 1}
        onPress={() => start()}
      >
        Enter App
      </Button>
       </XStack>
     

      
    </YStack>
  )
}
