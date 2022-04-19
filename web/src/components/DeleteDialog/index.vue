<template lang="pug">
  v-dialog(:value="value" max-width="400" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Xác Nhận Xóa
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      .p-4
        p Bạn có chắc chắn muốn xóa {{ data.name }}

      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          color="red"
          @click="onSave()"
        )
          span Xóa
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'

const DeleteDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    type: {
      type: String,
      required: true
    },
    data: {
      type: Object,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root

    const onSave = async () => {
      let url = ''
      if (props.type === 'giáo viên') {
        url = `${endpoints.TEACHER}${props.data.id}`
      }
      if (props.type === 'học sinh') {
        url = `${endpoints.STUDENT}${props.data.id}`
      }
      if (props.type === 'lớp học') {
        url = `${endpoints.CLASSROOM}${props.data.id}`
      }
      try {
        await api.delete(url)
        emit('reload')
        emit('on-close')
        $toast.success('Delete data successful')
      } catch {
        $toast.error('Delete data failed')
      }
    }
    return {
      onSave
    }
  }
})

export default DeleteDialog
</script>
