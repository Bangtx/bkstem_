<template lang="pug">
  v-dialog(:value="value" max-width="500" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span {{ title }}
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      .p-4(v-if="type !== 'lớp học'")
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

      v-card-text(v-if="type === 'lớp học'")
        v-list-item
          span Môn: {{ info.name }}
        v-divider
        v-list-item
          span Ngày tạo: {{ info.startDate }}
        v-list-item
          span Giáo viên: {{ info.teacher? info.teacher.name : ''}}
        .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4
          .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
            table.w-full.whitespace-nowrap.rounded-lg.border
              thead
                tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                  th.px-4.py-3.text-center.border STT
                  th.px-4.py-3.border Mã HS
                  th.px-4.py-3.border Tên HS
                  th.px-4.py-3.border.text-center Xóa
              tbody.bg-white
                tr.text-gray-700(v-for="(student, index) in info.students" :key="student.id")
                  td.px-4.py-3.border.text-center {{ index + 1 }}
                  td.px-4.py-3.border {{ student.id }}
                  td.px-4.py-3.text-sm.border {{ student.name }}
                  td.px-4.py-3.text-sm.border
                    .flex.justify-center
                      button.bg-red-500.text-white.px-4.py-2.rounded.mt-6(class='hover:bg-red-400 md:mt-0') Xóa

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
      if (props.type === 'lớp học') {
        url = `${endpoints.CLASSROOM}${props.data}`
      }
      try {
        const { data } = await api.get(url)
        info.value = toCamelCase(data)
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
