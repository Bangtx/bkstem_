<template lang="pug">
  v-dialog(:value="value" max-width="400" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Đk Tự học
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      v-card-text
        v-dialog.title-color(
          ref="dialog"
          persistent
          max-width="400"
          :return-value.sync="dates"
          v-model="modal"
        )
          template(v-slot:activator="{ on, attrs }")
            v-text-field.pa-0.pr-1(
              :label="'Ngày'"
              readonly
              hide-details
              append-outer-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
              :value="data.dates"
              @click:append-outer="modal = true"
            )
          v-date-picker(multiple full-width scrollable color="rough_black" header-color="rough_black" v-model="data.dates")
            v-spacer
            v-btn(text color="light_red" @click="modal = false")
              span Cancel
            v-btn(text color="rough_black" @click="$refs.dialog.save(data.dates)")
              span Ok

      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="onSave()"
        )
          span Lưu

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import moment from 'moment'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'

const RegisterSelfLearningDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      requires: true
    },
    data: {
      type: Object,
      requires: true
    }
  },
  setup(props, { root }) {
    const { $toast } = root
    const modal = ref(false)
    const dates = ref([])
    const onSave = async () => {
      try {
        await api.post(`${endpoints.SELF_LEARNING}`, toSnakeCase(props.data))
        // selfLearnings.value = toCamelCase(data)
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    return {
      onSave,
      modal,
      dates
    }
  }
})

export default RegisterSelfLearningDialog
</script>
