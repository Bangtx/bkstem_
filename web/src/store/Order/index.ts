interface State {
  showValue: Record<string, unknown>
}

export const order = {
  state: {
    showValue: {}
  },
  mutations: {
    setShowValueOrder(state: State, value: Record<string, unknown>): void {
      state.showValue = value
    }
  },
  actions: {}
}
