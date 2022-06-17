<template lang="pug" xmlns="">
  v-dialog(:value="value" max-width="400" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Lấy Id
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      v-card-text
        v-text-field.p-0(:label="'tên'" v-model="name")
        v-list-item-content(v-for="student in students" :key="student.id")
          v-row
            v-col.pa-0(cols="2")
              span {{ student.id }}
            v-col.pa-0(cols="10")
              span {{ student.name }}

      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="onSearch()"
        )
          span Tra cứu
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase } from 'utils'

const GetIdDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    }
  },
  setup(props, { root }) {
    const { $toast } = root
    const name = ref('')
    const students = ref<any[]>([])

    const onSearch = async () => {
      try {
        const { data } = await api.get(`${endpoints.ACCOUNT}?name=${name.value}`)
        students.value = toCamelCase(data)
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    return {
      name,
      onSearch,
      students
    }
  }
})

export default GetIdDialog
</script>

<style lang="sass"></style>
