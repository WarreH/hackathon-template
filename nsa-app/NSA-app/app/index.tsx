import { TamaguiProvider, Theme, createTamagui } from '@tamagui/core'
import StartScreen from './screens/StartScreen'

// you usually export this from a tamagui.config.ts file
import { defaultConfig } from '@tamagui/config/v4' // for quick config install this
import { View } from 'react-native'
import RootNavigator from './navigation/RootNavigator'

const config = createTamagui(defaultConfig)

export default () => {
  return (
    <TamaguiProvider config={config}>
      <View style={styles.container}>
        <Theme name="light">
          <RootNavigator/>
        </Theme>
      </View>
    </TamaguiProvider>
  )
}
const styles = {
  container: {
    flex: 1,
    backgroundColor: 'gray',  // Set the background to white for the light theme
  },
};

