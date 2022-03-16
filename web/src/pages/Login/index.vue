<template lang="pug">
  div(:style="{backgroundColor: '#FFF', marginTop: '20vh'}")
    v-container(fluid fill-height)
      v-layout(align-center justify-center)
        v-flex(xs12 sm8 md4)
          v-card.elevation-12
            v-toolbar(dark color="primary")
              v-toolbar-title Đăng Nhập
            v-card-text
              v-form
                v-text-field(
                  prepend-icon="mdi-account" :label="'Sđt/mail'" type="mai" v-model="userData.name"
                )
                v-text-field#password(
                  prepend-icon="mdi-key"
                  :label="'Mật khẩu'"
                  type="password"
                  v-model="userData.password"
                )
            v-card-actions
              v-spacer
              v-btn(color="primary" @click="onClickLogin()") Đăng Nhập
              v-btn(color="primary") Quên Mật Khẩu
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import axios from 'axios'
import { endpoints, toSnakeCase, urlPath } from 'utils'

const Login = defineComponent({
  setup(props, { root }) {
    const { $toast, $router } = root
    const userData = ref({ name: '', password: '' })
    const onClickLogin = async () => {
      userData.value.name = userData.value.name.trim()
      userData.value.password = userData.value.password.trim()
      if (userData.value.name.length === 0) $toast.error('Vui lòng nhập mail/sđt')
      if (userData.value.password.length === 0) $toast.error('Vui lòng nhập mật khẩu')
      if (userData.value.name.length > 0 && userData.value.password.length > 0) {
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

<style lang="sass"></style>
