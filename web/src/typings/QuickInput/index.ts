import { CommonProperty } from '../Common'

export interface QuickInput {
  id: number | null
  code: number | null
  item: CommonProperty | null
  variety?: CommonProperty | null
  size?: CommonProperty | null
  quality?: CommonProperty | null
  unit?: CommonProperty | null
  quantity: number | null
  orderNum?: number | null
  searchStr: string
}

export type IQuickInput = any

export type QuickInputState = {
  code: string
  item: string
  variety: string
  size: string
  quality: string
  unit: string
  quantity: string
}
