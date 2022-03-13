// import { Image } from '../Image'
// import { CommonProperty } from '../Common'
// import { Unit } from '../Unit'
import { SizeGroup, QualityGroup, Image, CommonProperty, Unit } from 'typings'

interface IItem {
  name: string
  shortName?: string
  yomi?: string
  nameEng?: string
  defaultUnit: number
  units?: Array<number>
  sizeGroupId?: number
  qualityGroupId?: number
}

interface Item {
  id: number
  name: string
  uuid: string
  shortName: string
  yomi: string
  nameEng: string
  defaultUnit: CommonProperty
  units?: Array<Unit>
  images: Array<Image>
  searchStr: string
  orderNum: number | null
  sizeGroup: SizeGroup | null
  qualityGroup: QualityGroup | null
}

export { IItem, Item }
