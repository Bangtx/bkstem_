import Vue from 'vue'
import Vuex from 'vuex'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import { broadcast } from 'vuex-iframe-sync'

export default new Vuex.Store({
  state: {
    panelStateProduct: {
      panels: []
    },
    panelStateCustomer: {
      panels: []
    },
    listStates: {
      order: [],
      packing: [],
      harvest: [],
      assign: [],
      assignSeri: []
    }
  },
  mutations: {
    setListStates(state, value) {
      state.listStates = value
    }
  },
  actions: {}
})
