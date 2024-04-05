import { createRouter, createWebHistory} from 'vue-router'

import LoginVue from '@/views/Login.vue';
import LayoutVue from '@/views/Layout.vue'

import ManageVue from '@/views/Management.vue'

// import Home 
import ManagementHomeVue from '@/views/ManagementHome.vue'
import ContainHomeVue from '@/views/container/ContainHome.vue'
import ImageHomeVue from '@/views/image/ImageHome.vue'





const routes=[
    // {path: '/', component:LoginVue,},
    {path: '/login', component:LoginVue},
    {path: '/', component:LayoutVue, children:[
        {path: '/manage/home', component:ManagementHomeVue},
        {path: '/manage', component:ManageVue},
        {path: '/manage/container', component:ContainHomeVue},
        {path: '/manage/image', component:ImageHomeVue}
    ]},
    // {path: '/manage', component:ManageVue}
]

const router = createRouter({
    history:createWebHistory(),
    routes:routes
})

export default router