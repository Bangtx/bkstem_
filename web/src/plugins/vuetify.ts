import Vue from 'vue'
// eslint-disable-next-line import/no-extraneous-dependencies
import Vuetify from 'vuetify/lib/framework'

import { theme } from 'utils'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: theme.LIGHT
    },
    options: {
      customProperties: true
    }
  }
})
