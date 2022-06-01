<template lang="pug">
  v-dialog(:value="value" max-width="500" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span {{ mode==='add' ? 'Gửi Thông Báo' : 'Xem Thông Báo' }}
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close
      v-card-text.mt-4(v-if="mode==='see'")
        div(v-if="student.notification.length > 0" v-for="notification in student.notification" :key="notification.id")
          h1 {{ notification.date }}
          p.msg {{ notification.notification }}
          v-divider
        div(v-if="student.notification.length === 0")
          p.msg Không có thông báo nào

      .p-4(v-if="mode==='add'")
        h1 {{ isAll ? 'Gửi cho tất cả' : student.name }}
        v-select(
          :label="'Kiểu'"
          :items="selectItemsVN"
          v-model="selectedItem"
        )
        v-container.padding(fluid)
          v-text-field(
            autocomplete="Mess"
            label="Mess"
            height="100px"
            v-model="msg"
          )

      v-divider
      v-card-actions(v-if="mode==='add'")
        v-spacer
        v-btn.title-color(@click="postNoti()") Gửi

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints } from 'utils'
import jwtDecode from 'jwt-decode'
import moment from 'moment'

const NotificationDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    mode: {
      type: String,
      required: false,
      default: 'add'
    },
    isAll: {
      type: Boolean,
      required: false,
      default: false
    },
    classroom: {
      type: Object,
      required: true
    },
    student: {
      type: Object || null,
      required: true
    },
    students: {
      type: Array,
      required: false,
      default: () => []
    },
    notifications: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  setup(props, { emit, root }) {
    const { $toast } = root
    const msg = ref('')
    const teacher: any = jwtDecode(String(localStorage.getItem('token')))
    const selectItemsVN = ['Thông báo', 'Tiến độ']
    const selectItems = ['info', 'progress']
    const selectedItem = ref('Tiến độ')

    const postNotiAPI = async () => {
      const body = {
        classroom: props.classroom.id,
        student: props.student.id,
        teacher: teacher.id,
        notification: msg.value,
        date: moment(new Date()).format('YYYY-MM-DD'),
        type: selectItems[selectItemsVN.indexOf(selectedItem.value)]
      }

      try {
        if (msg.value !== '') {
          await api.post(`${endpoints.NOTIFICATION}`, body)
          $toast.success('Save data successful')
          emit('on-close')
          emit('reload')
        } else {
          $toast.error('Chưa nhập tin nhắn')
        }
      } catch {
        $toast.error('Save msg failed')
      }
    }

    const postMultipleNotiAPI = async () => {
      const body = props.students?.map((e: any) => {
        return {
          classroom: props.classroom.id,
          student: e.id,
          teacher: teacher.id,
          notification: msg.value,
          date: moment(new Date()).format('YYYY-MM-DD')
        }
      })

      try {
        if (msg.value !== '') {
          await api.post(`${endpoints.NOTIFICATION}multiple_notifications`, body)
          $toast.success('Save data successful')
          emit('on-close')
          emit('reload')
        } else {
          $toast.error('Chưa nhập tin nhắn')
        }
      } catch {
        $toast.error('Save msg failed')
      }
    }

    const postNoti = async () => {
      if (props.isAll) {
        await postMultipleNotiAPI()
      } else {
        await postNotiAPI()
      }
    }

    return {
      msg,
      postNoti,
      selectItemsVN,
      selectedItem
    }
  }
})
export default NotificationDialog
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
