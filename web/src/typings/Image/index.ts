export interface Image {
  id: number | null
  name: string
  url: string
  uuid?: string
  token: string
  payload?: string | ArrayBuffer | null
}
