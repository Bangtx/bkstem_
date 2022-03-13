interface State {
  assignOrderByCustomerPanelState: Record<string, unknown>
  assignOrderByProductPanelState: Record<string, unknown>
  filterBy: string
  showBy: string
}

export const assignOrder = {
  state: {
    assignOrderByCustomerPanelState: {},
    assignOrderByProductPanelState: {},
    filterBy: 'SHOW_ALL',
    showBy: 'CUSTOMER'
  },
  mutations: {
    setAssignOrderByCustomerPanelState(state: State, value: Record<string, unknown>): void {
      state.assignOrderByCustomerPanelState = value
    },
    setAssignOrderByProductPanelState(state: State, value: Record<string, unknown>): void {
      state.assignOrderByProductPanelState = value
    },
    setFilterByAssignOrder(state: State, value: string): void {
      state.filterBy = value
    },
    setShowByAssignOrder(state: State, value: string): void {
      state.showBy = value
    }
  },
  actions: {}
}
