<script setup lang="ts">


    import Container from './container/ContainHome.vue'
    import Image from './image/ImageHome.vue'
    
    import { ref } from 'vue'


    const size = ref<"image" | "container">('image')



</script>

<template>
    <el-radio-group v-model="size" label="control">
        <el-radio-button value="image" >镜像管理</el-radio-button>
        <el-radio-button value="container" >容器管理</el-radio-button>
    </el-radio-group>


  
    <Container v-if="size==='container'"></Container>
    <Image v-else-if="size==='image'"></Image>

    
    


</template>
  
<style lang="scss" scoped>


</style>


