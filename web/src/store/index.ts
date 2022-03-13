import Vue from 'vue'
import Vuex from 'vuex'

import { assign } from './assign'
import { assignSeri } from './AssignSeriFromPacking'
import { assignOrder } from './AssignOrderFromPacking'
import { harvest } from './harvest'
import { packingResult } from './PackingResult'
import { order } from './Order'
import { history } from './history'
import { common } from './common'

Vue.use(Vuex)

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
      assignSeri: [],
      assignOrder: []
    }
  },
  mutations: {
    setListStates(state, value) {
      state.listStates = value
    }
  },
  actions: {},
  modules: {
    assign,
    harvest,
    packingResult,
    order,
    common,
    assignSeri,
    assignOrder,
    history
  }
})
