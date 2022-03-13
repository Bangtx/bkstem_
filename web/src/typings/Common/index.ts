export interface CommonProperty {
  id: number | null
  name: string
  // for boxType
  bundleSize?: number
}

export interface MultiLevelQualitySize {
  qualitySizeName: string
  children: Array<any>
}

export interface MultiLevelVariety {
  varietyName: string
  children: Array<MultiLevelQualitySize>
}

export interface MultiLevelProduct {
  itemName: string
  children: Array<MultiLevelVariety>
}

export interface MultiLevelCustomer {
  customerName: string
  children: Array<MultiLevelProduct>
}
