<template lang="pug">
  v-dialog(:value="value" max-width="400" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span {{ title.toUpperCase() }}
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      v-card-text
        v-text-field.p-0(:label="'tên'" v-model="student.name")
        v-text-field.p-0(v-if="mode==='add'" :label="'password'" v-model="password")
        v-text-field.p-0(:label="'mail'" v-model="student.mail")
        v-text-field.p-0(:label="'điện thoại'" v-model="student.phone")
        v-select.p-0(
          :label="'giới tính'"
          :items="['Nam', 'Nữ']"
          v-model="student.gender"
        )

        v-select.p-0(
          multiple
          :label="'lớp'"
          :items="classrooms.map(e => e.name)"
          v-model="classroomsSelected"
        )

        v-dialog.title-color(
          ref="dialog"
          persistent
          max-width="400"
          :return-value.sync="student.dateOfBirth"
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
              :value="student.dateOfBirth"
              @click:append-outer="modal = true"
            )
          v-date-picker(full-width scrollable color="rough_black" header-color="rough_black" v-model="date")
            v-spacer
            v-btn(text color="light_red" @click="modal = false")
              span Cancel
            v-btn(text color="rough_black" @click="$refs.dialog.save(date)")
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
import { endpoints, toSnakeCase } from 'utils'

const StudentDialog = defineComponent({
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
    student: {
      type: Object,
      required: true
    },
    classrooms: {
      type: Array,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const modal = ref(false)
    const password = ref('')
    const date = moment(new Date()).format('YYYY-MM-DD')
    const className = ref('')
    const classroomsSelected = ref<string[]>([])

    const onSave = async () => {
      const classIds = classroomsSelected.value
        .map((name: string) => {
          return props.classrooms.find((classroom: any) => classroom.name === name)
        })
        .map((classroom: any) => classroom.id)
      try {
        if (props.mode === 'add') {
          const body = {
            name: props.student.name,
            gender: props.student.gender,
            mail: props.student.mail,
            phone: props.student.phone,
            dateOfBirth: props.student.dateOfBirth,
            password: password.value,
            classrooms: classIds
          }
          await api.post(`${endpoints.STUDENT}`, toSnakeCase(body))
        } else {
          const body = {
            name: props.student.name,
            gender: props.student.gender,
            mail: props.student.mail,
            phone: props.student.phone,
            dateOfBirth: props.student.dateOfBirth,
            classrooms: classIds
          }
          await api.put(`${endpoints.STUDENT}${props.student.id}`, toSnakeCase(body))
        }
        emit('reload')
        emit('on-close')
        $toast.success('Save data successful')
      } catch {
        $toast.error('Save data failed')
      }
    }

    return {
      modal,
      date,
      onSave,
      password,
      className,
      classroomsSelected
    }
  }
})

export default StudentDialog
</script>

<style lang="sass">
.v-picker__title
  background-color: beige !important
  color: #343f4b !important
.v-date-picker-table .v-btn.v-btn--active
  background-color: beige !important
  color: #343f4b !important
</style>
