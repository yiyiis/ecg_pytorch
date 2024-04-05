import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve:{
    alias:{
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      '/api': { // 获取请求中带 /api 的请求
        // target: 'http://localhost:8080',  // 后台服务器的源
        // target:'http://192.168.137.67:8080',
        target: "http://127.0.0.1:4523/m1/4230279-0-default",
        changeOrigin: true,   // 修改源
        rewrite: (path) => path.replace(/^\/api/, "")   //  /api 替换为空字符串
      }
    }
  }
})
