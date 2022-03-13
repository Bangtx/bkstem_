interface ISize {
  name: string
  sizeGroupId: number
  yomi?: string
  nameEng?: string
  shortName?: string
}

interface ISizeGroup {
  name: string
  yomi?: string
  nameEng?: string
  shortName?: string
}

interface SizeGroupBasicInfo {
  id: number
  name: string
}

interface Size {
  id: number
  name: string
  yomi: string
  nameEng: string
  shortName: string | null
  searchStr: string
  orderNum: number | null
  sizeGroup: SizeGroupBasicInfo
}

interface SizeGroup {
  id: number
  name: string
  yomi: string
  nameEng: string
  shortName: string
  orderNum: number | null
  searchStr: string
  isDefault: boolean
  active?: boolean
}

interface SizesBySizeGroup extends SizeGroup {
  sizes: Array<Size>
}

export { ISize, ISizeGroup, Size, SizeGroup, SizesBySizeGroup }
