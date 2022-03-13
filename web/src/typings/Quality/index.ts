interface IQuality {
  name: string
  qualityGroupId: number
  yomi?: string
  nameEng?: string
  shortName?: string
}

interface IQualityGroup {
  name: string
  yomi?: string
  nameEng?: string
  shortName?: string
}

interface QualityGroupBasicInfo {
  id: number
  name: string
}

interface Quality {
  id: number
  name: string
  yomi: string
  nameEng: string
  shortName?: string
  searchStr: string
  orderNum: number | null
  qualityGroup: QualityGroupBasicInfo
}

interface QualityGroup {
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

interface QualitiesByQualityGroup extends QualityGroup {
  qualities: Array<Quality>
}

export { IQuality, IQualityGroup, Quality, QualityGroup, QualitiesByQualityGroup }
