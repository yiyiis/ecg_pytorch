<script setup>
import {
    Delete,
    VideoPlay,
    SwitchButton,
    Folder,
    Files,
} from '@element-plus/icons-vue'

import { ref } from 'vue'

//文章分类数据模型
const images = ref([
    {
      "id": "11111",
      "name": "kylinos_image",
      "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load"
    },
    {
      "id": "22222",
      "name": "uos_image",
      "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load"
    }
  ])

//用户搜索时选中的镜像id
const imageId=ref('')

//用户搜索时选中的容器状态
const state=ref('')

const containerList_slice = ref([])
//文章列表数据模型
const containerList = ref([
    // {
    //   "id": "11111_11111",
    //   "name": "kylinos_container",
    //   "create_image": "11111",
    //   "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load",
    //   "state": "运行中"
    // },
    // {
    //   "id": "11111_22222",
    //   "name": "uos_container",
    //   "create_image": "22222",
    //   "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load",
    //   "state": "暂停"
    // },
    // {
    //   "id": "11111_33333",
    //   "name": "uos_container",
    //   "create_image": "22222",
    //   "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load",
    //   "state": "暂停"
    // },
    // {
    //   "id": "11111_11111",
    //   "name": "kylinos_container",
    //   "create_image": "11111",
    //   "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load",
    //   "state": "运行中"
    // },
    // {
    //   "id": "11111_22222",
    //   "name": "uos_container",
    //   "create_image": "22222",
    //   "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load",
    //   "state": "暂停"
    // },
    // {
    //   "id": "11111_33333",
    //   "name": "uos_container",
    //   "create_image": "22222",
    //   "icon": "https://images.pexels.com/photos/7381200/pexels-photo-7381200.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load",
    //   "state": "暂停"
    // },
    

  ])

  import {Plus} from '@element-plus/icons-vue'
    //控制抽屉是否显示
    const visibleDrawer = ref(false)
    //添加容器数据模型
    const containerModel = ref({
        name: '',
        icon: '',
        cpu: '',
        create_image: '',
        disk: '',
        memory: '',
    })

    const cpuNum = ref(0)
    const diskSize = ref(0)
    const memorySize = ref(0)



    import { containerListService, containerRunService, containerAddService, containerDeleteService, containerStopService, containerSearchService } from '@/api/container.js'
    import { imageListService } from '@/api/image.js'
    import { postPhoto } from '@/api/photo.js'

    // 获取镜像 后续测试要加
    const getImageList = async ()=>{
        let result = await imageListService()
        images.value = result.data
        // alert(result.msg)
    }
    getImageList()

    // 获取容器列表
    const getContainerList = async()=>{
        let result = await containerListService()
        containerList.value = result.data
        // console.log(containerList.value.length)
        // total.value = containerList.value.length
        getTableData()
    }
    // 添加容器
    const addContainer = async (state)=>{
        let result = await containerAddService(containerModel.value)

        let uuid = result.data.icon


        let _formData = new FormData();
        _formData.append("image", _fileObj);     

        console.log(uuid)
        // http://dummyimage.com/100x100
        let result2 = await postPhoto(uuid, _formData)
        // console.log(result2)
        await runContainer(result.data.id, result.data.vnc)
        getContainerList()
        
    }

    const url = ref('')
    //启动容器
    const runContainer = async (containerId, vnc)=>{

        let result = await containerRunService(containerId)

        url.value = vnc.ip + ':' + vnc.port
        myApi.sendU(url.value)
        window.open("https://" + url.value,'blank_', 'height=800, width=1000')
        
       //更新数据 后续测试要加
       getContainerList()
    }
    // 暂停容器
    const stopContainer = async (row)=>{
        // 操作 
        let result = await containerStopService(row.id)
        console.log(result)
        //更新数据 后续测试要加
        getContainerList()
    }
    // 删除容器
    import {ElMessageBox} from 'element-plus'
    import { ElMessage } from 'element-plus'
    const deleteContainer = async (row)=>{
            //提示用户  确认框
    ElMessageBox.confirm(
        '你确认要删除该分类信息吗?',
        '温馨提示',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            //调用接口
            let result = await containerDeleteService(row.id)
            ElMessage({
                type: 'success',
                message: '删除成功',
            })
                //更新数据 后续测试要加
                getContainerList()
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '用户取消了删除',
            })
        })

    }

    getContainerList()

    const transfile = (row)=>{

    }

    const searchModel = ref({
        name: '',
        state: '',
        image_id: ''
    })
    //搜索容器
    const searchContainer = async ()=>{
        let result = await containerSearchService(searchModel.value)
        console.log(result)
        // ToDO
        containerList.value = result.data
        getTableData()
    }

//分页条数据模型
const pageNum = ref(1)//当前页
const total = ref(6)//总条数
const pageSize = ref(3)//每页条数
//当每页条数发生了变化，调用此函数
const onSizeChange = (size) => {
    pageSize.value = size
    getTableData()
}
//当前页码发生变化，调用此函数
const onCurrentChange = (num) => {
    pageNum.value = num
    getTableData()
}
const getTableData = ()=>{
    if(containerList.value.length === 0){
        containerList_slice.value = []
    }
    else{
    containerList_slice.value = containerList.value.slice(
        (pageNum.value - 1) * pageSize.value,
        pageNum.value * pageSize.value
    )
    total.value = containerList.value.length
    }

}

// 这是路径
const fi = ref('')
// 这是file
let _fileObj

const showImg =()=>{
     
    var file = document.getElementById('fileImage').files[0];
    _fileObj = file;
    console.log(_fileObj)
    if (window.FileReader) {    
            var reader = new FileReader();    
            reader.readAsDataURL(file);    
            //监听文件读取结束后事件    
            reader.onloadend = function (e) {
            //e.target.result就是最后的路径地址
            fi.value = e.target.result
            };    
        }
    }



</script>
<template>
    <el-card class="page-container">
        <template #header>
            <div class="header">
                <span>容器</span>
                <div class="extra">
                    <el-button type="primary" @click="visibleDrawer = true">添加容器</el-button>
                </div>
            </div>
        </template>
        <!-- 搜索表单 -->
        <el-form :inline="true"  class="demo-form-inline">
        <el-form-item label="容器名：">
            <el-input v-model="searchModel.name" placeholder="请输入容器名"></el-input>
        </el-form-item>

            <el-form-item label="镜像类别：">
                <el-select placeholder="请选择" v-model="searchModel.image_id">
                    <el-option 
                        v-for="image in images" 
                        :key="image.id" 
                        :label="image.name"
                        :value="image.id">
                    </el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="容器状态：">
                <el-select placeholder="请选择" v-model="searchModel.state">
                    <el-option label="运行中" value="运行中"></el-option>
                    <el-option label="暂停" value="暂停"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="searchContainer">搜索</el-button>
                <el-button @click="searchModel.name = '';searchModel.image_id = '' ; searchModel.state = ''">重置</el-button>
            </el-form-item>
        </el-form>

        
        <!-- 文章列表 -->
        <el-table :data="containerList_slice" style="width: 100%">
            <el-table-column label="图标" width="200px">
                <template v-slot="scope">
                    <img :src="scope.row.icon" alt="" style="width: 150px;height: 150px">
                </template>
            </el-table-column>
            <el-table-column label="容器名" width="200px" prop="name"></el-table-column>
            <el-table-column label="镜像类别" prop="create_image_name"></el-table-column>
            <el-table-column label="状态" prop="state"></el-table-column>
            <!-- 不需要手动去修改状态了 -->
            <el-table-column label="操作" width="200px">
                <template v-slot="scope">
                    <el-button class="delete-btn" type="danger" :icon="Delete" @click="deleteContainer(scope.row)" circle />
                    <el-button class="on-btn" type="success" :icon="VideoPlay"  @click="runContainer(scope.row.id, scope.row.vnc)" circle />
                    <el-button class="off-btn" type="danger" :icon="SwitchButton"  @click="stopContainer(scope.row)" circle />
                    <el-button class="trans-btn" type="warning" :icon="Folder"  @click="transfile(scope.row); " circle />
                </template>
            </el-table-column>
            <template #empty>
                <el-empty description="没有数据" />
            </template>
        </el-table>


        <!-- 分页条 -->
        <el-pagination v-model:current-page="pageNum" v-model:page-size="pageSize" :page-sizes="[3, 5, 10, 15]"
            layout="jumper, total, sizes, prev, pager, next" background :total="total" @size-change="onSizeChange"
            @current-change="onCurrentChange" style="margin-top: 20px; justify-content: flex-end" />



                <!-- 抽屉 -->
        <el-drawer v-model="visibleDrawer" title="添加容器" direction="rtl" size="50%">
            <!-- 添加文章表单 -->
            <el-form :model="containerModel" label-width="120px">
                    <el-form-item label="容器标题">
                        <el-input v-model="containerModel.name" placeholder="请输入标题"></el-input>
                    </el-form-item>
                    <el-form-item label="镜像类型">
                        <el-select placeholder="请选择" v-model="containerModel.create_image">
                            <el-option v-for="image in images" :key="image.id" :label="image.name" :value="image.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="容器封面" >
                        <!-- <el-upload class="avatar-uploader" @change="showImg" id="fileImage" name="fileImage"
                        >
                            <img :src="fi" class="avatar" id='img1' width="120px" height="120px" />
                        </el-upload> -->
                        <img :src="fi" class="avatar" id='img1' width="120px" height="120px" />

                        <input type="file" class="avatar-uploader"  @change="showImg" id="fileImage" name="fileImage" style="display:none;"/>

                        <label for="fileImage">
                            <div class="lBut"><span>选择文件</span></div>
                        </label>
                        
                    </el-form-item>
                    
                    <el-form-item label="cpu数量 /个">
                        <el-slider v-model="containerModel.cpu" show-input :max="20"/>
                    </el-form-item>
                    <el-form-item label="磁盘大小 /G">
                        <el-slider v-model="containerModel.disk" show-input :max="20"/>
                    </el-form-item>
                    <el-form-item label="内存大小 /Mb">
                        <el-slider v-model="containerModel.memory" show-input :max="4*1024"/>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" @click="addContainer('运行中')">创建并运行</el-button>
                        <el-button type="info" @click="addContainer('暂停')">创建</el-button>
                    </el-form-item>

            </el-form>
        </el-drawer>
    </el-card>
</template>

<style lang="scss" scoped>


.lBut{
	width: 87px;
	height: 32px;
	font-size: 14px;
	line-height: 1.15;
	display: flex;
	justify-content: center;
	align-items: center;
	border-radius: 4px;
	padding: 8px 10px;
	margin-left: 28px;
	transition: all 0.5s;
	white-space: nowrap;
	background-color: #409eff;
	color: white;
	border: 1px solid #409eff;

}


.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}
.page-container {
    min-height: 100%;
    box-sizing: border-box;

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
}

/* 抽屉样式 */
.avatar-uploader {
    :deep() {
        .avatar {
            width: 178px;
            height: 178px;
            display: block;
        }

    }
}

.editor {
    width: 100%;

    :deep(.ql-editor) {
        min-height: 200px;
    }
}

</style>