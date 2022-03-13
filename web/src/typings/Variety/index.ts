import { Image, SizeGroup, QualityGroup, Item } from 'typings'

interface IVariety {
  name: string
  shortName?: string
  yomi?: string
  nameEng?: string
  item: number
  sizeGroupId?: number
  qualityGroupId?: number
}

interface Variety {
  id: number
  name: string
  yomi: string
  nameEng: string
  shortName: string
  orderNum: number | null
  searchStr: string
  item: Item
  images: Array<Image>
  uuid: string
  sizeGroup: SizeGroup | null
  qualityGroup: QualityGroup | null
}

interface VarietiesByItem {
  id: number
  name: string
  nameEng: string | null
  shortName: string | null
  yomi: string | null
  orderNum: number | null
  searchStr: string
  sizeGroup: SizeGroup | null
  qualityGroup: QualityGroup | null
  images: Array<Image>
  active?: boolean
  varieties: Array<Variety>
}

interface VarietySort {
  id: number
  orderNum: number | null
}

export { IVariety, Variety, VarietiesByItem, VarietySort }
