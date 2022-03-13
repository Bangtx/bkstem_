export const common = {
  state: {
    newDataMaster: {},
    allVarietyByItem: [],
    historyPath: []
  },
  mutations: {
    setHistoryPath(state: any, value: Array<string>) {
      state.historyPath = value
    },
    setNewDataMaster: (state: any, value: any) => {
      state.newDataMaster = value
    },
    setAllVarietyByItem: (state: any, value: any) => {
      state.allVarietyByItem = value
    }
  },
  actions: {}
}
