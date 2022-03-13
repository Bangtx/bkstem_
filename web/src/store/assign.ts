import { BatchAssignState } from 'typings'

interface State {
  orderPanelState: Record<string, unknown>
  customerPanelState: Record<string, unknown>
  assignByProductPanelState: Record<string, unknown>
  assignByCustomerPanelState: Record<string, unknown>
  packingListState: Record<string, unknown>
  batchAssignState: BatchAssignState
  selectedFromResult: string | null
  showValue: Record<string, unknown>
}

export const assign = {
  state: {
    orderPanelState: {},
    customerPanelState: {},
    assignByProductPanelState: {},
    assignByCustomerPanelState: {},
    packingListState: {},
    selectedFromResult: null,
    batchAssignState: {
      item: null,
      variety: null,
      quality: null,
      size: null,
      orderDetailIds: []
    },
    showValue: {}
  },
  mutations: {
    setOrderPanelState(state: State, value: Record<string, unknown>): void {
      state.orderPanelState = value
    },
    setCustomerPanelState(state: State, value: Record<string, unknown>): void {
      state.customerPanelState = value
    },
    setAssignByProductPanelState(state: State, value: Record<string, unknown>): void {
      state.assignByProductPanelState = value
    },
    setAssignByCustomerPanelState(state: State, value: Record<string, unknown>): void {
      state.assignByCustomerPanelState = value
    },
    setPackingListState(state: State, value: Record<string, unknown>): void {
      state.packingListState = value
    },
    setBatchAssignState(state: State, value: BatchAssignState): void {
      state.batchAssignState = value
    },
    resetBatchAssignState(state: State): void {
      state.batchAssignState = {
        item: null,
        variety: null,
        quality: null,
        size: null,
        orderDetailIds: []
      }
    },
    setSelectedFromResult(state: State, value: string | null): void {
      state.selectedFromResult = value
    },
    setShowValueAssign(state: State, value: Record<string, unknown>): void {
      state.showValue = value
    }
  },
  actions: {}
}
