import React, { useEffect, useState } from 'react';
import { Dimensions } from 'react-native';
import { Image, ScrollView, Text, YStack, Spinner } from 'tamagui';
const screenWidth = Dimensions.get('window').width *0.8
import { useFocusEffect } from '@react-navigation/native'

export default function ProfileScreen() {
  const [images, setImages] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  const fetchImageIds = async () => {
    try {
      const userIdentifier = "example_user"
      const res = await fetch('http://192.168.84.177:8080/picture/experience/'+userIdentifier) // replace with real endpoint
      const ids: string[] = await res.json()

      // Get original dimensions for each image
      const withDimensions = await Promise.all(
        ids.map(async (id) => {
          const uri = `http://192.168.84.177:8080/picture/${id}`
          return new Promise<any>((resolve) => {
            Image.getSize(uri, (width, height) => {
              resolve({ id, uri, width, height })
            }, () => {
              resolve({ id, uri, width: '100%', height: 200 }) // fallback
            })
          })
        })
      )

      setImages(withDimensions)
    } catch (err) {
      console.error('Error fetching image data:', err)
    } finally {
      setLoading(false)
    }
  }

  useFocusEffect(() => {
    fetchImageIds()
  })

  return (
    <ScrollView>
      <YStack  padding="$4" alignItems='center' gap="$5">
        <Text fontSize={24} fontWeight="700" width='100%' marginBottom="$5">📷 Image Gallery</Text>

        {loading && <Spinner size="large" />}

        {!loading && images.map(({ id, uri, width, height }) => {
          const scaledHeight = (screenWidth * height) / width
          return (
            <Image
            
              key={id}
              source={{ uri }}
              width={screenWidth}
              height={scaledHeight}
              borderRadius="$4"
            />
          )
        })}
      </YStack>
    </ScrollView>
  )
}
  
