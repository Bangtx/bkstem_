import Color from './Color'

export * from './Order'
export * from './OrderDetail'
export * from './Error'

export * from './PackingResult'

export * from './Size'
export * from './Unit'
export * from './Item'
export * from './Variety'
export * from './Image'
export * from './Customer'
export * from './Quality'
export * from './BoxType'
export * from './OrderType'

export * from './QuickInput'
export * from './HarvestResult'
export * from './Assign'

export * from './Common'
export { Color }

export * from './BottomSheet'

export interface Body {
  id: number
  orderNum: number
}

export interface ObjectWrapper {
  [key: string]: any
}

export interface Tab {
  name: string
  param: string
}

export interface IState {
  order: Array<string>
  packing: Array<string>
  harvest: Array<string>
  assign: Array<string>
}
