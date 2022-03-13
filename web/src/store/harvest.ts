import { HarvestOrderState, Item, Variety, Size, Quality } from 'typings'

type ProducState = {
  item: Item | null
  variety: Variety | null
  size: Size | null
  quality: Quality | null
}

interface State {
  panelState: Record<string, unknown>
  productPanelState: Record<string, unknown>
  harvestOrderState: HarvestOrderState
  productState: ProducState
  showValue: Record<string, unknown>
}

export const harvest = {
  state: {
    panelState: {},
    productPanelState: {},
    harvestOrderState: {
      item: null,
      variety: null,
      size: null,
      quality: null,
      result: null,
      ids: []
    },
    productState: {
      item: null,
      variety: null,
      size: null,
      quality: null
    },
    showValue: {}
  },
  mutations: {
    setHarvestPanelState(state: State, value: Record<string, unknown>): void {
      state.panelState = value
    },
    setProductPanelState(state: State, value: Record<string, unknown>): void {
      state.productPanelState = value
    },
    setHarvestOrderState(state: State, value: HarvestOrderState): void {
      state.harvestOrderState = value
    },
    resetHarvestOrderState(state: State): void {
      state.harvestOrderState = {
        item: null,
        variety: null,
        size: null,
        quality: null,
        result: null,
        ids: []
      }
    },
    setProductState(state: State, value: ProducState): void {
      state.productState = value
    },
    resetProductState(state: State): void {
      state.productState = {
        item: null,
        variety: null,
        size: null,
        quality: null
      }
    },
    setShowValueHarvest(state: State, value: Record<string, unknown>): void {
      state.showValue = value
    }
  },
  actions: {}
}
