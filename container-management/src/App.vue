<script setup lang="ts">
  import { provide, ref } from 'vue'
  import Home from './views/Home.vue'
  import Manageme from '@/views/Management.vue';
  import Login from '@/views/Login.vue'

  const isShow = ref(false)
  const setIsShow = (value) =>{
      isShow.value = value
  }


  provide('dialog-visible', {
    isShow,
    setIsShow
  })
  

</script>

<template>
  <!-- <Home></Home> -->
  <!-- <Manageme></Manageme> -->
  <!-- <Login></Login> -->
  <router-view></router-view>
</template>


