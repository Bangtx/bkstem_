<template lang="pug">
  v-dialog(
    :value="value"
    max-width="700"
    persistent
    scrollable
  )
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span {{ title }}
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      v-card-text.p-0.my-card
        v-list-item-content.p-0(
          v-for="student in students" :key="student.id"
          @click="checkStudent(student)"
        )
          v-col.p-0(cols="12")
            v-row
              v-col(cols="2")
                v-icon.ml-2(
                  v-if="checks.indexOf(student.id) > -1"
                  color="primary"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="checks.indexOf(student.id) === -1"
                  color="primary"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="2")
                span.name {{ student.id }}
              v-col.p-1(cols="8")
                span.name {{ student.name }}

      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="onSave()"
        )
          span Lưu

</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from '@vue/composition-api'
import { api } from 'plugins'
import { toCamelCase, endpoints, toSnakeCase } from 'utils'

const ChooseProperty = defineComponent({
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: Boolean,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const students = ref<any>([])
    const checks = ref<number[]>([])

    const checkStudent = (student: any) => {
      const index = checks.value.indexOf(student.id)
      if (index === -1) checks.value.push(student.id)
      else checks.value.splice(index, 1)
    }

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.STUDENT}`)
        students.value = toCamelCase(data)
      } catch {
        $toast.error('Get data failed')
      }
    }

    const onSave = async () => {
      const body = {
        ...props.classroom,
        student_ids: checks.value,
        teacher: props.classroom.teacher.id
      }
      try {
        await api.put(`${endpoints.CLASSROOM}${props.classroom.id}`, toSnakeCase(body))
        emit('reload')
        emit('on-close')
      } catch (e) {
        $toast.error('Update failed')
      }
    }

    onMounted(async () => {
      await getData()
    })

    watch(
      () => props.value,
      () => {
        if (props.value) checks.value = props.classroom.students.map((e: any) => e.id)
      }
    )
    return {
      students,
      checks,
      checkStudent,
      onSave
    }
  }
})

export default ChooseProperty
</script>

<style>
.name {
  font-size: 16px;
}
.my-card {
  padding: 0 !important;
}
</style>
