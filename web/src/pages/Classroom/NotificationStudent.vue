<template lang="pug">
  #main.main-content.flex-1.py-20(class='md:pb-5')
    .px-4.text-gray-700(class='md:px-8')
      .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
          path(stroke-linecap='round' stroke-linejoin='round' d='M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9')
        div Thông báo ({{ notifications.length }})
        v-select.ml-2(
          :label="'Kiểu'"
          :items="selectItemsVN"
          v-model="selectedItem"
          @change="onSelectItem()"
        )
      div
        .mt-6(v-for="notification in notificationsSearched" :key="notification.id")
          .mb-2 {{ notification.date }}
          .rounded-lg.py-5.px-6.mb-4.text-base.text-blue-700.mb-3(
            role='alert'
            :class="colors[Math.floor(Math.random() * colors.length)]"
          )
            p {{ notification.notification }}

</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase } from 'utils'
import jwtDecode from 'jwt-decode'

interface Student {
  id: number
  name: string
  notification?: string[]
}

interface Notification {
  id: number
  date: string
  student: Student
  notification: string
}

const NotificationStudent = defineComponent({
  props: {
    classroom: {
      type: Object,
      required: true
    }
  },
  setup(props, { root }) {
    const { $toast } = root
    const colors = ['bg-blue-100', 'bg-purple-100', 'bg-green-100', 'bg-red-100', 'bg-yellow-100']
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    const notifications = ref<Notification[]>([])
    const notificationsSearched = ref<Notification[]>([])

    const selectItemsVN = ['All', 'Thông báo', 'Tiến độ']
    const selectItems = ['All', 'info', 'progress']
    const selectedItem = ref('Tiến độ')

    const getData = async () => {
      try {
        const { data } = await api.get(
          `${endpoints.NOTIFICATION}?class_room=${props.classroom.id}&student_id=${member.id}`
        )
        notifications.value = toCamelCase(data)
        notificationsSearched.value = notifications.value.filter((e: any) => e.type === 'progress')
      } catch {
        $toast.error('Get data failed')
      }
    }

    const onSelectItem = () => {
      if (selectedItem.value !== 'All') {
        notificationsSearched.value = notifications.value.filter(
          (e: any) => e.type === selectItems[selectItemsVN.indexOf(selectedItem.value)]
        )
      } else notificationsSearched.value = notifications.value
    }

    onMounted(async () => {
      await getData()
    })

    return {
      colors,
      notifications,
      selectItemsVN,
      selectedItem,
      notificationsSearched,
      onSelectItem
    }
  }
})

export default NotificationStudent
</script>

<style lang="sass">
.v-input
  max-width: 150px !important
</style>
