export interface Error {
  response?: {
    data?: {
      messages?: Array<string>
    }
  }
}
