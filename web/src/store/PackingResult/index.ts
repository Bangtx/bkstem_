interface State {
  byPackingResultPanelState: Record<string, unknown>
  byProductPanelState: Record<string, unknown>
  byOrderPanelState: Record<string, unknown>
  byCustomerPanelState: Record<string, unknown>
  showBy: string
  showValue: Record<string, unknown>
}

export const packingResult = {
  state: {
    byPackingResultPanelState: {},
    byProductPanelState: {},
    byOrderPanelState: {},
    byCustomerPanelState: {},
    showBy: '',
    showValue: {}
  },
  mutations: {
    setByPackingResultPanelState(state: State, value: Record<string, unknown>): void {
      state.byPackingResultPanelState = value
    },
    setByProductPanelState(state: State, value: Record<string, unknown>): void {
      state.byProductPanelState = value
    },
    setByOrderPanelState(state: State, value: Record<string, unknown>): void {
      state.byOrderPanelState = value
    },
    setByCustomerPanelState(state: State, value: Record<string, unknown>): void {
      state.byCustomerPanelState = value
    },
    setShowByPackingResult(state: State, value: string): void {
      state.showBy = value
    },
    setShowValuePacking(state: State, value: Record<string, unknown>): void {
      state.showValue = value
    }
  },
  actions: {}
}
