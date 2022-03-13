interface State {
  assignSeriPanelState: Record<string, unknown>
}

export const assignSeri = {
  state: {
    assignSeriPanelState: {}
  },
  mutations: {
    setAssignSeriPanelState(state: State, value: Record<string, unknown>): void {
      state.assignSeriPanelState = value
    }
  },
  actions: {}
}
