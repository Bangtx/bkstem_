interface ICustomer {
  name: string
  tel: string
  yomi?: string
  shortName?: string
  email?: string
  code?: string
  zipCode?: string
  address1?: string
  address2?: string
  fax?: string
  defaultInvoiceMethod: string | null
  allowPreSale: boolean
  levelCustomer?: string
}

interface Customer {
  id: number
  name: string
  tel: string
  yomi: string
  shortName: string
  email: string
  code: string
  zipCode: string
  address1: string
  address2: string
  fax: string
  searchStr: string
  orderNum: number | null
  defaultInvoiceMethod: string | null
  allowPreSale: boolean
  levelCustomer: string
}

export { ICustomer, Customer }
