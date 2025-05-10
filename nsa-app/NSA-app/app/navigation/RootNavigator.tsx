import { createNativeStackNavigator } from '@react-navigation/native-stack'
import StartScreen from '../screens/StartScreen'
import Tabs from './Tabs'
import DetailScreen from '../screens/DetailScreen'


const Stack = createNativeStackNavigator()


export default function RootNavigator() {
  return (
      <Stack.Navigator initialRouteName="Start" screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Start" component={StartScreen} />
        <Stack.Screen name="MainTabs" component={Tabs} />
        <Stack.Screen name="DetailPage" component={DetailScreen}/>
      </Stack.Navigator>
  )
}
