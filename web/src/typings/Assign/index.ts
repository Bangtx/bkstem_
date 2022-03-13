import { Item } from '../Item'
import { Variety } from '../Variety'
import { Size } from '../Size'
import { Unit } from '../Unit'
import Color from '../Color'
import { Customer } from '../Customer'
import { BoxType } from '../BoxType'
import { CommonProperty } from '../Common'

interface Assign {
  id: number
  auctionDate: string
  buyerInfo: string
  customer: Customer
  item: Item
  variety: Variety
  size: Size
  unit: Unit
  quality: CommonProperty
  orderType: CommonProperty
  boxType: BoxType
  colors: Array<Color>
  quantity: number
  boxes: number
  stems: number
  price: number
  amount: number
  remark: string
  orderDetailId: number
  harvestResultId: number
  packingResultId: number,
  packingResult: number,
  orderDetail: number
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type IAssign = any

interface Property {
  id: number
  name: string
}

interface Quality {
  id: number
  shortName?: string
  name: string
}

interface PackingResult {
  id: number
  packedDate: string
  item: Property
  variety: Property
  size: Property
  color: Color
  quality: Quality
  quantity: number
  boxType: Property
  boxes: number
  unit: Property
  totalStems: number
  desiredPrice: number
  assignBoxes: number
  assignStems: number
  searchStr: string
  breakdowns: any
  deliveries: any
  remark: string
  orderedStems: number
  orderedBoxes: number
  assignedStems: number
  assignedBoxes: number
}

interface Assignment {
  id: number
  boxes: number
  stems: number
  price: number
  amount: number
  packingResult: PackingResult
}

interface OrderDetailAssign {
  id: number
  orderTypeId: number
  item: Property
  variety: Property
  size: Property
  colors: Array<Color>
  quality: Quality
  boxes: number
  unit: Property
  stems: number
  price: number
  amount: number
  remark: string
  isLock: boolean
  assignStems: number
  assignments: Array<number>
}

interface OrderByAuctionDate {
  id: number
  pic: number
  auctionDate: string
  customer: Customer
  orderDetails: Array<OrderDetailAssign>
}

interface IAssignment {
  boxes: number
  stems: number
  price: number
  amount: number
  orderDetailId: number
  packingResultId: number
}

interface BatchAssignState {
  item: Item | null
  variety: Variety | null
  quality: Quality | null
  size: Size | null
  orderDetailIds: Array<number>
}

export {
  PackingResult,
  OrderByAuctionDate,
  IAssignment,
  Assignment,
  OrderDetailAssign,
  Assign,
  IAssign,
  BatchAssignState
}
