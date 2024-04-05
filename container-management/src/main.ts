// main.ts
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import locale from 'element-plus/dist/locale/zh-cn'
import 'element-plus/dist/index.css'
import App from './App.vue'
import './assets/common.css'

import router from '@/router'

import {createPinia} from 'pinia'
import { createPersistedState } from 'pinia-persistedstate-plugin'


const app = createApp(App)
const pinia = createPinia()
const persist = createPersistedState()
app.use(ElementPlus, {locale})
app.use(router)
app.use(pinia)
app.mount('#app')