<template lang="pug">
  v-dialog(:value="value" max-width="400" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span {{ title.toUpperCase() }}
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      v-card-text
        v-text-field.p-0(:label="'tên'" v-model="teacher.name")
        v-text-field.p-0(:label="'mail'" v-model="teacher.mail")
        v-text-field.p-0(:label="'điện thoại'" v-model="teacher.phone")
        v-select.p-0(
          :label="'giới tính'"
          :items="['Nam', 'Nữ']"
          v-model="teacher.gender"
        )
        v-dialog.title-color(
          ref="dialog"
          persistent
          max-width="400"
          :return-value.sync="teacher.dateOfBirth"
          v-model="modal"
        )
          template(v-slot:activator="{ on, attrs }")
            v-text-field.pa-0.pr-1(
              :label="'Ngày sinh'"
              readonly
              hide-details
              append-outer-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
              :value="teacher.dateOfBirth"
              @click:append-outer="modal = true"
            )
          v-date-picker(full-width scrollable color="rough_black" header-color="rough_black" v-model="date")
            v-spacer
            v-btn(text color="light_red" @click="modal = false")
              span Cancel
            v-btn(text color="rough_black" @click="$refs.dialog.save(date), search()")
              span Ok

      v-card-actions
        v-btn.relative-btn(
          v-if="mode === 'add'"
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="create()"
        )
          span Lưu
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import moment from 'moment'

const TeacherDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    mode: {
      type: String,
      required: false,
      default: 'edit'
    },
    teacher: {
      type: Object,
      required: true
    }
  },
  setup() {
    const modal = ref(false)
    const date = moment(new Date()).format('YYYY-MM-DD')

    const create = () => {
      console.log('create')
    }

    return {
      modal,
      date,
      create
    }
  }
})

export default TeacherDialog
</script>

<style lang="sass">
.v-picker__title
  background-color: beige !important
  color: #343f4b !important
.v-date-picker-table .v-btn.v-btn--active
  background-color: beige !important
  color: #343f4b !important
</style>
