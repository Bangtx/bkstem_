<template lang="pug">
  div(:style="{backgroundColor: '#FFF', marginTop: '16vh'}")
    div.text-red-600.text-center.font-bold.text-3xl.pb-6.hidden(class="md:block")
      div.flex.justify-center
        img.w-14(:src="`/img/icons/android-chrome-192x192.png`")
      div HỌC VIỆN STEAM BÁCH KHOA
    div
      v-layout(align-center justify-center)
        v-flex.justify-center
          div.bg-gray-50.border.rounded-lg.w-500.pb-2
            div.rounded-t-lg.bg-orange
              v-toolbar-title.py-3.ml-6.text-white.font-semibold Đăng Nhập
            v-card-text
              v-form
                v-text-field(
                  prepend-icon="mdi-account" :label="'Mail'" type="email" v-model="userData.mail"
                )
                v-text-field#password(
                  prepend-icon="mdi-key"
                  :label="'Mật khẩu'"
                  type="password"
                  v-model="userData.password"
                )
            v-card-actions
              v-spacer
              v-btn.bg-orange.mr-4( @click="onClickLogin()") Đăng Nhập
              v-btn Quên Mật Khẩu
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import axios from 'axios'
import { endpoints, toSnakeCase, urlPath } from 'utils'

const Login = defineComponent({
  setup(props, { root }) {
    const { $toast, $router } = root
    const userData = ref({ mail: '', password: '' })
    const onClickLogin = async () => {
      userData.value.mail = userData.value.mail.trim()
      userData.value.password = userData.value.password.trim()
      if (userData.value.mail.length === 0) $toast.error('Vui lòng nhập mail/sđt')
      if (userData.value.password.length === 0) $toast.error('Vui lòng nhập mật khẩu')
      if (userData.value.mail.length > 0 && userData.value.password.length > 0) {
        try {
          const { data } = await axios.post(`${endpoints.AUTH}login`, toSnakeCase(userData.value))
          if (data.status === 404) {
            $toast.error('Tài khoản mật khẩu không chính xác')
          }
          localStorage.setItem('token', data.token)
          $router.push({
            name: urlPath.START.name
          })
        } catch (e) {
          $toast.error('Đăng nhập thấy bại')
        }
      }
    }
    return {
      userData,
      onClickLogin
    }
  }
})
export default Login
</script>

<style lang="sass">
.bg-orange
  background: #fb923c !important
  color: white !important
.w-500
  width: 300px
@media (min-width: 500px)
  .w-500
    width: 500px
</style>
