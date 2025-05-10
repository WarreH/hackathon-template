import { useRoute } from '@react-navigation/native';
import { useNavigation } from 'expo-router';
import { Text, YStack, Image, Button } from 'tamagui';

export default function DetailScreen() {
  // Use the `useRoute` hook to get parameters passed via navigation
  const route = useRoute();
  const navigation = useNavigation()
  const { cardId } = route.params as { cardId: number };

  // Example card data (this should typically come from a database or an API)
  const cardData = [
    {
      id: 1,
      title: 'Card 1',
      description: 'This is a detailed description for card 1.',
      imageUrl: 'https://via.placeholder.com/150',
    },
    {
      id: 2,
      title: 'Card 2',
      description: 'This is a detailed description for card 2.',
      imageUrl: 'https://via.placeholder.com/150',
    },
    {
      id: 3,
      title: 'Card 3',
      description: 'This is a detailed description for card 3.',
      imageUrl: 'https://via.placeholder.com/150',
    },
  ];

  // Find the card data by cardId
  const card = cardData.find((item) => item.id === cardId);

  if (!card) {
    return (
      <YStack f={1} ai="center" jc="center" space="$4">
        <Text fontSize={20} color="gray10">
          Card not found
        </Text>
      </YStack>
    );
  }

  return (
    <YStack flex={1} gap="$4" space="$6">
      {/* Title */}
      <Text fontSize={32} fontWeight="700" textAlign="center">
        {card.title}
      </Text>

      {/* Image */}
      <Image source={{ uri: card.imageUrl }} width={300} height={300} borderRadius="$2" alignSelf="center" />

      {/* Description */}
      <Text fontSize={16} color="gray10" textAlign="center">
        {card.description}
      </Text>

      {/* Back Button */}
      <Button
        size="$4"
        onPress={() => {
          // Go back to the previous screen
          navigation.goBack();
        }}
      >
        Go Back
      </Button>
    </YStack>
  );
}
