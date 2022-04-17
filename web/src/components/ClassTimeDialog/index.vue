<template lang="pug">
  v-dialog(:value="value" max-width="400" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Giờ Học
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      v-card-text
        v-select.p-0(
          :label="'Ngày'"
          :items="selectDateOfWeek"
          v-model="date"
        )
        v-row
          v-col(cols="6")
            v-dialog.title-color(
              ref="dialogStart"
              persistent
              max-width="400"
              :return-value.sync="startTime"
              v-model="modalStart"
            )
              template(v-slot:activator="{ on, attrs }")
                v-text-field.pa-0.pr-1(
                  :label="'Bắt đầu'"
                  readonly
                  hide-details
                  append-outer-icon="mdi-calendar"
                  v-bind="attrs"
                  v-on="on"
                  :value="startTime"
                  @click:append-outer="modalStart = true"
                )
              v-time-picker(
                v-model="startTime"
                type="month"
                width="290"
              )
                v-spacer
                v-btn(text color="light_red" @click="modalStart = false")
                  span Cancel
                v-btn(text color="rough_black" @click="$refs.dialogStart.save(startTime)")
                  span Ok
          v-col(cols="6")
            v-dialog.title-color(
              ref="dialogStop"
              persistent
              max-width="400"
              :return-value.sync="stopTime"
              v-model="modalStop"
            )
              template(v-slot:activator="{ on, attrs }")
                v-text-field.stop.pr-1(
                  :label="'Kết thúc'"
                  readonly
                  hide-details
                  append-outer-icon="mdi-calendar"
                  v-bind="attrs"
                  v-on="on"
                  :value="stopTime"
                  @click:append-outer="modalStop = true"
                )
              v-time-picker(
                v-model="stopTime"
                type="month"
                width="290"
              )
                v-spacer
                v-btn(text color="light_red" @click="modalStop = false")
                  span Cancel
                v-btn(text color="rough_black" @click="$refs.dialogStop.save(stopTime)")
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
import { api } from 'plugins'
import { endpoints, toSnakeCase } from 'utils'
import moment from 'moment'

const ClassTimeDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const modalStart = ref(false)
    const modalStop = ref(false)
    const startTime = ref(moment(new Date()).format('HH:MM'))
    const stopTime = ref(moment(new Date()).format('HH:MM'))

    const dateOfWeek = [
      { id: 1, name: 'Thứ 2' },
      { id: 2, name: 'Thứ 3' },
      { id: 3, name: 'Thứ 4' },
      { id: 4, name: 'Thứ 5' },
      { id: 5, name: 'Thứ 6' },
      { id: 6, name: 'Thứ 7' },
      { id: 7, name: 'Chủ nhật' }
    ]
    const selectDateOfWeek = dateOfWeek.map((e: any) => e.name)

    const date = ref('')

    const onSave = async () => {
      const body = {
        dateOfWeek: dateOfWeek.find((e: any) => e.name === date.value)?.id,
        stopTime: stopTime.value,
        startTime: startTime.value
      }
      try {
        await api.post(`${endpoints.CLASS_TIME}`, toSnakeCase(body))
        emit('reload')
        emit('on-close')
        $toast.success('Save data successful')
      } catch {
        $toast.error('Save data failed')
      }
    }

    return {
      date,
      dateOfWeek,
      selectDateOfWeek,
      modalStart,
      startTime,
      modalStop,
      stopTime,
      onSave
    }
  }
})

export default ClassTimeDialog
</script>

<style lang="sass">
.v-picker__title__btn
  color: #111111
.stop
  margin-top: 5px !important
</style>
