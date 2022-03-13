import { Customer } from '../Customer'

export interface Order {
  id: number
  auctionDate: Date
  totalBoxes: number
  totalAmount: number
  assignAmount: number
  createdAt: string
  pckBoxes?: number
  pckStems?: number
  customer: Customer
}

export type AnyOrder = any

export interface IOrder {
  auctionDate: string | null
  customerId: number | null
}

export interface OrderByProduct {
  ids: Array<number>
  item: {
    id: number
    name: string
    searchStr: string
  }
  variety: {
    id: number
    name: string
    searchStr: string
  }
  totalBoxes: number
  totalStems: number
  assignBoxes: number
  assignStems: number
}

export interface OrderByCustomer {
  customer: {
    id: number
    name: string
    searchStr: string
  }
  totalBoxes: number
  totalStems: number
  assignBoxes: number
  assignStems: number
  ids: Array<number>
}

type OrderSummaryMonth = {
  month: string
  items: Array<{
    year: number
    month: number
    id: number
    auctionDate: Date
    totalBoxes: number
    totalAmount: number
    assignAmount: number
    createdAt: string
  }>
  active: boolean
}

export interface OrderSummary {
  year: string
  months: Array<OrderSummaryMonth>
}
