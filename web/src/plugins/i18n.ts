import Vue from 'vue'
import VueI18n from 'vue-i18n'
import ja from '../locale/ja.json'

Vue.use(VueI18n)

const i18n = new VueI18n({
  locale: 'ja',
  messages: {
    ja
  }
})

export default i18n
