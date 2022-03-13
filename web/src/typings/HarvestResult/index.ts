import { Item } from '../Item'
import { Variety } from '../Variety'
import { Size } from '../Size'
import { Unit } from '../Unit'
import Color from '../Color'
import { Quality } from '../Quality'

export interface HarvestResult {
  id: number
  harvestDate: string
  stems: number
  desiredPrice: number
  quantity: number
  boxes: number
  item: Item
  variety: Variety
  size: Size
  unit: Unit
  color: Color
  quality: Quality
  orderedStems: number
  orderedBoxes: number
  assignedStems: number
  totalStems: number
}

export type InputHarvestResult = any

export interface HarvestOrderState {
  item: Item | null
  variety: Variety | null
  size: Size | null
  quality: Quality | null
  result: HarvestResult | null
  ids: Array<number>
}

export interface HarvestProductInfo {
  item: Item
  variety: Variety
  size: Size
  quality: Quality
}
