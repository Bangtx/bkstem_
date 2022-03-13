import Vue from 'vue'
import router from 'router'
import store from 'store'
import VueCompositionAPI from '@vue/composition-api'
import PortalVue from 'portal-vue'
import Toast from 'vue-toastification'
import VueVirtualScroller from 'vue-virtual-scroller'
import 'vue-toastification/dist/index.css'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

import { vuetify, i18n, api, moment } from 'plugins'
import App from './App.vue'
import './registerServiceWorker'

Vue.config.productionTip = false

Vue.prototype.$api = api
Vue.prototype.moment = moment

Vue.use(VueCompositionAPI)
Vue.use(PortalVue)
Vue.use(Toast, { hideProgressBar: true })
Vue.use(VueVirtualScroller)

declare global {
  interface Window {
    logout?: any
  }
}

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: (h) => h(App)
}).$mount('#app')
