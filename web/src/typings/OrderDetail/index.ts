import { Item } from '../Item'
import { Variety } from '../Variety'
import { Size } from '../Size'
import { Unit } from '../Unit'
import Color from '../Color'
import { Order } from '../Order'
import { CommonProperty } from '../Common'
import { Customer } from '../Customer'
import { OrderType } from '../OrderType'
import { Quality } from '../Quality'

export interface OrderDetail {
  id: number
  quantity: number
  boxes: number
  stems: number
  order: Order
  remark: string
  item: Item
  variety: Variety
  size: Size
  unit: Unit
  colors: Array<Color>
  buyerInfo: string
  quality: CommonProperty
  isAssigned: boolean
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type IOrderDetail = any

export type PropertyState = {
  quickInput: string
  auctionDate: string
  customer: string
  item: string
  variety: string
  size: string
  colors: string
  quality: string
  unit: string
  orderType: string
  quantity: string
}

export type DetailByProduct = {
  ids: Array<number>
  totalBoxes: number
  item: Item
  variety: Variety
}

export type DetailGroupByItem = {
  item: string
  data: Array<OrderDetail | DetailByProduct>
}

interface ChildrenBase {
  boxes: number
  buyerInfo: number
  colorIds: Array<number>
  colors: Array<Color>
  customer: Customer
  customerName: string
  id: number
  isAssigned: boolean
  isLock: boolean
  isSpecial: boolean
  item: Item
  itemName: string
  order: Order
  orderType: OrderType
  pck: number
  price: number
  quality: Quality
  qualitySizeName: string
  quantity: number
  remark: string
  size: Size
  stems: number
  unit: Unit
  variety: Variety
  varietyId: number
  varietyName: string
}

interface ChildrenByCustomer2 {
  customerName: string
  stems: number
  pck: number
  children: ChildrenBase
}

interface ChildrenByQualitySizeArray {
  qualitySizeName: string
  stems: number
  pck: number
  children: ChildrenBase
}

interface ChildrenByQualitySize {
  qualitySizeName: string
  stems: number
  pck: number
  children: Array<ChildrenByCustomer2>
}

interface ChildrenByVariety {
  varietyName: string
  stems: number
  pck: number
  children: Array<ChildrenByQualitySize>
}

interface ChildrenByItem {
  customerName: string
  itemName: string
  stems: number
  pck: number
  children: Array<ChildrenByVariety>
}

interface ChildrenByCustomer {
  customerName: string
  stems: number
  pck: number
  children: Array<ChildrenByItem>
}

interface SelectTab {
  name: string
  key: string
}

export {
  SelectTab,
  ChildrenBase,
  ChildrenByCustomer,
  ChildrenByCustomer2,
  ChildrenByItem,
  ChildrenByVariety,
  ChildrenByQualitySize,
  ChildrenByQualitySizeArray
}
