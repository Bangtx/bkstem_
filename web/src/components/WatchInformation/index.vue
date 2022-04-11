<template lang="pug">
  v-dialog(:value="value" max-width="500" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span {{ title }}
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      .p-4
        v-list-item
          span Họ Tên: {{ info.name }}
        v-divider
        v-list-item
          span Chức vụ: {{ type }}
        v-list-item
          span Sinh ngày: {{ info.dateOfBirth }}
        v-list-item
          span Giới tính: {{ info.gender }}
        v-list-item
          span Mail: {{ info.mail }}
        v-list-item
          span Điện thoại: {{ info.phone }}

</template>

<script lang="ts">
import { defineComponent, watch, ref } from '@vue/composition-api'
import { endpoints, toCamelCase } from 'utils'
import { api } from 'plugins'

const WatchNotification = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    type: {
      type: String,
      required: true
    },
    data: {
      type: Number,
      required: true
    }
  },
  setup(props, { root }) {
    const { $toast } = root
    const info = ref<any>({})

    const getData = async () => {
      let url = ''
      if (props.type === 'giáo viên') {
        url = `${endpoints.TEACHER}${props.data}`
      }
      if (props.type === 'học sinh') {
        url = `${endpoints.STUDENT}${props.data}`
      }
      try {
        const { data } = await api.get(url)
        info.value = toCamelCase(data)
        console.log(toCamelCase(data))
      } catch {
        $toast.error('Get data failed')
      }
    }

    watch(
      () => props.value,
      () => {
        if (props.value) {
          getData()
        }
      }
    )
    return {
      info
    }
  }
})

export default WatchNotification
</script>

<style lang="sass">
.title-color
  background-color: beige !important
.padding
  padding: 0 !important
.v-input__slot
  display: block !important
.msg
  font-size: 17px
  color: #111111
</style>
