import { Route } from 'vue-router'

interface State {
  histories: Array<Route>
}

export const history = {
  state: {
    histories: []
  },
  mutations: {
    pushHistory(state: State, value: Route): void {
      state.histories.push(value)
    },
    popHistory(state: State): void {
      state.histories.pop()
    },
    updateHistory(state: State, value: Route): void {
      state.histories.pop()
      state.histories.push(value)
    }
  },
  getters: {
    showHistories(state: State): State {
      return state
    }
  }
}
