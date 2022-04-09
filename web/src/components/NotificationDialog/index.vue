<template lang="pug">
  v-dialog(:value="value" max-width="500" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Privacy Policy
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close
      .p-4(v-if="mode==='see'")
        p Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

      .p-4(v-if="mode==='add'")
        h1 Tran xuan banh
        v-container.padding(fluid)
          v-text-field(
            autocomplete="Mess"
            label="Mess"
            height="100px"
            v-model="msg"
          )

      v-divider
      v-card-actions
        v-spacer
        v-btn.title-color(@click="postNotiAPI()") Gửi

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
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
    studentId: {
      type: Number,
      required: true
    }
  },
  setup(props, { emit, root }) {
    const { $toast } = root
    const msg = ref('')
    const teacher: any = jwtDecode(String(localStorage.getItem('token')))

    const postNotiAPI = async () => {
      const body = {
        classroom: props.classroom.id,
        student: props.studentId,
        teacher: teacher.id,
        notification: msg.value,
        date: moment(new Date()).format('YYYY-MM-DD')
      }

      try {
        await api.post(`${endpoints.NOTIFICATION}`, body)

        $toast.success('Save data successful')
        emit('on-close')
      } catch {
        $toast.error('Save msg failed')
      }
    }

    return {
      msg,
      postNotiAPI
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
</style>
