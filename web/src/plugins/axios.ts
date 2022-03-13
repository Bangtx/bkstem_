import axios from 'axios'
import { Auth } from 'aws-amplify'

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL
})

api.interceptors.request.use(
  async (config) => {
    if ('Cypress' in window) {
      return config
    }

    const token = await Auth.currentSession().then((res) => {
      const accessToken = res.getAccessToken()
      return accessToken.getJwtToken()
    })

    if (token) {
      // eslint-disable-next-line no-param-reassign
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api
