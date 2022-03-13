<template lang="pug">
  div#slides.carousel.slide(data-ride="carousel")
    ul.carousel-indicators
      li.active(data-target="#slides" data-slide-to="0") 7F91F5
      //li(data-target="#slides" data-slide-to="1") 7F91F5
    div.carousel-inner
      div.carousel-item.active
        div.banner-1
        //img(src="https://cskh-ginnyhouse.easyedu.vn/sites/default/files/easyschool/logo/banner.png" width="100%")
        div.carousel-caption
          h1.display-2 Phạm Việt Hưng
          h3 Giáo Viên
          button.btn.btn-primary.btn-lg Get started
      //div.carousel-item
      //  div.banner-2
      //  img(src="http://bksteam.edu.vn/wp-content/uploads/2021/03/slide2-2048x636.jpg" width="100%")

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'

const Banner = defineComponent({
  setup() {
    const showHeaderText = ref(false)
    showHeaderText.value = window.innerWidth < 700
    window.addEventListener('resize', () => {
      showHeaderText.value = window.innerWidth < 700
    })
    const value = ref('hhi')
    return {
      value,
      showHeaderText
    }
  }
})
export default Banner
</script>

<style lang="sass">
.carousel-caption
  color: #0E5A84
.banner-1
  background-position: 50% 50%
  background-image: url("https://cskh-ginnyhouse.easyedu.vn/sites/default/files/easyschool/logo/banner.png")
  background-size: cover
  height: 350px
</style>
