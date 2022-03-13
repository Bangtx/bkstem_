import { CommonProperty } from '../Common'
import Color from '../Color'
import { Item } from '../Item'
import { Variety } from '../Variety'
import { Size } from '../Size'
import { Quality } from '../Quality'

export interface PackingResultSummary {
  auctionDate: string
  boxes: number
  totalStems: number
  assignBoxes?: number
  assignStems?: number
}

export interface PackingResultPackedDate {
  packedDate: string
  summaries?: Array<PackingResultSummary>
  active?: boolean
  loading?: boolean
}

export interface PackingResultGroupByYear {
  year: string
  data: Array<PackingResultPackedDate>
}

export interface PackedDateByMonth {
  packedDate: string
}

export interface PackingResultDetail {
  auctionDate: string
  quantity: number
  boxes: number
  id: number
  totalStems: number
  desiredPrice: number
  quality: CommonProperty
  variety: CommonProperty
  item: CommonProperty
  size: CommonProperty
  unit: CommonProperty
  color: Color
  boxType: CommonProperty
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type IPackingResult = any

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type IBreakdown = any

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type IDelivery = any

export type BreakdownState = {
  item: string
  variety: string
  size: string
  color: string
  quality: string
  quantity: string
}

export type DeliveryState = {
  auctionDate: string
  customer: string
  boxes: string
  stems: string
  orderType: string
  buyerInfo: string
  price: string
}

export interface Product {
  item: Item
  variety: Variety
  size: Size
  quality: Quality
}
