<script lang="ts" setup>
import {
    Management,
    Promotion,
    UserFilled,
    User,
    Crop,
    EditPen,
    SwitchButton,
    CaretBottom
} from '@element-plus/icons-vue'


import { ref } from 'vue'

const activeIndex = ref('1')



import {useRouter} from 'vue-router'
const router = useRouter();

</script>

<template>
    <el-container class="layout-container">
        <!-- 左侧菜单 -->
        <el-aside width="200px">
            <div class="el-aside__logo"></div>
            
            <el-menu active-text-color="#ffd04b" background-color="#545C64"  text-color="#fff" close-on-click-outside router>
                
                <el-menu-item index="/manage/home">
                    <el-icon>
                        <Management />
                    </el-icon>
                    <span>首页</span>
                </el-menu-item>

                <el-menu-item index="/manage/image">
                    <el-icon>
                        <Promotion />
                    </el-icon>
                    <span>镜像管理</span>
                </el-menu-item>

                <el-menu-item index="/manage/container">
                    <el-icon>
                        <Promotion />
                    </el-icon>
                    <span>容器管理</span>
                </el-menu-item>
                
            </el-menu>
        </el-aside>
        <!-- 右侧主区域 -->
        <el-container>
    <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    router
  >
        <el-menu-item index="/manage/container">首页</el-menu-item>
        <el-menu-item index="/login">退出</el-menu-item>
    </el-menu>


            <!-- 中间区域 -->
            <el-main>
                <router-view></router-view>
            </el-main>
            <!-- 底部区域 -->
            <el-footer>国产操作系统容器桌面 ©2024 Created by Forward</el-footer>
        </el-container>
    </el-container>
</template>

<style lang="scss" scoped>
.layout-container {
    height: 100vh;

    .el-aside {
        background-color: #545C64;

        &__logo {
            height: 120px;
            background: url('@/assets/logo.png') no-repeat center / 120px auto;
            
        }

        .el-menu {
            border-right: none;
        }
    }

    .el-header {
        background-color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;

        .el-dropdown__box {
            display: flex;
            align-items: center;

            .el-icon {
                color: #999;
                margin-left: 10px;
            }

            &:active,
            &:focus {
                outline: none;
            }
        }
    }

    .el-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: #666;
    }
}
</style>