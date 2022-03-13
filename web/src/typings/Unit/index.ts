interface IUnit {
  name: string
  yomi?: string
  shortName?: string
}

interface Unit {
  id: number
  name: string
  yomi: string
  searchStr: string
  shortName: string | null
  orderNum: number | null
}

interface DefaultUnit {
  id: number
  name: string
  isCheck: boolean
}

export { IUnit, Unit, DefaultUnit }
