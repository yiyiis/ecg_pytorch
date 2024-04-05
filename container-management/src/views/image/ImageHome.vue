<script setup>
    import {
        Edit,
        Delete
    } from '@element-plus/icons-vue'
    import { ref } from 'vue'

    const images_slice = ref([])
    const images = ref([
        {
        "id": "2edws3",
        "name": "kylinos镜像",
        "icon": "https://ts3.cn.mm.bing.net/th?id=OIP-C.ZkoPhpKfJwsvGmpm8RsragHaFp&w=286&h=218&c=8&rs=1&qlt=90&o=6&dpr=1.5&pid=3.1&rm=2"
        },
        {
        "id": "213fd",
        "name": "uos镜像",
        "icon": "https://ts3.cn.mm.bing.net/th?id=OIP-C.ZkoPhpKfJwsvGmpm8RsragHaFp&w=286&h=218&c=8&rs=1&qlt=90&o=6&dpr=1.5&pid=3.1&rm=2"
        }
    ])

    const apps = ref([
        {
            "name": "拉农好清表什",
            "icon": "http://dummyimage.com/100x100"
        },
        {
            "name": "第问去基国",
            "icon": "http://dummyimage.com/100x100"
        },
        {
            "name": "值直更党们华",
            "icon": "http://dummyimage.com/100x100"
        }
    ])


    import { imageListService, imageDetailService, imageDeleteService, imageAddService } from '@/api/image.js' 
    import { appListService } from '@/api/app.js'
    import { postPhoto } from '@/api/photo.js'

    // 获取app列表
    const getAppList = async ()=>{
        let result = await appListService()
        apps.value = result.data
        console.log(apps.value)
    }
    getAppList()

    // 获取镜像列表
    const getImageList = async ()=>{
        let result = await imageListService()
        images.value = result.data

        getTableData()
    }
    getImageList()

    const imageDetail = ref('')

    // 镜像详情
    const getImageDetail = async (row)=>{
        // console.log(row)
        let result = await imageDetailService(row.id)
        imageDetail.value = result.data
        // console.log(imageDetail.value)
    }

    import {ElMessageBox} from 'element-plus'
    import { ElMessage } from 'element-plus'
    // 删除镜像
    const deleteImage = async(row)=>{
        ElMessageBox.confirm(
            '你确认要删除该分类信息吗?',
            '温馨提示',
            {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning',
            }
        ).then(async () => {
            //调用接口
            let result = await imageDeleteService(row.id)
            ElMessage({
                type: 'success',
                message: '删除成功',
            })
                //更新数据 后续测试要加
                imageDetail.value = ''
                getImageList()
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '用户取消了删除',
            })
        })
    }

    const imageModel = ref({
        name: '',
        icon: '',
        app_id: [],
        create_image: ''
    })

    // 加载数据
    const isSending = ref(false)
    // 添加镜像
    const addImage = async ()=>{
        isSending.value = true
        let result = await imageAddService(imageModel.value)
        let uuid = result.data.icon
        console.log(uuid)

        let _formData = new FormData();
        _formData.append("image", _fileObj);        
        let result2 = await postPhoto(uuid, _formData)

        if (result2) {
        isSending.value = false;
        }

        clearData()

        //更新数据
        getImageList()
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
        images_slice.value = images.value.slice(
            (pageNum.value - 1) * pageSize.value,
            pageNum.value * pageSize.value
        )
        total.value = images.value.length
    }


    const rowClick=(row)=>{
        console.log(row)
    }
  
  const addSwitch = ref(true)

// 这是路径
const fi = ref('')
// 这是file
let _fileObj

const showImg =()=>{
     
    var file = document.getElementById('fileImage').files[0];
    _fileObj = file;
    // console.log(_fileObj)
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

    
    
    // 多选框选中数据
    const handleSelectionChange = (selection)=>{
        //获取所有选中项的name属性的值
        let app_arr = selection.map(item => item.name)
        imageModel.value.app_id = app_arr
        console.log(imageModel.value)
      }
      
    const clearData=()=>{
        imageModel.value = ref({
        name: '',
        icon: '',
        app_id: [],
        create_image: ''
    })
    }

</script>

<template>
    <el-card class="page-image">


        <div v-if="addSwitch">
            <div class="header">
                <span>镜像管理</span>
                <div class="extra">
                    <el-button type="primary" @click="addSwitch=false">添加镜像</el-button>
                </div>
            </div>
            <el-table :data="images_slice" style="width: 100%" @row-click="getImageDetail">
                <el-table-column label="序号" width="100" type="index"> </el-table-column>
                <el-table-column label="镜像名称" prop="name"></el-table-column>
                <el-table-column label="图标" width="150px">
                    <template v-slot="scope">
                        <img :src="scope.row.icon" alt="" style="width: 150px;height: 150px">
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="200px">
                    <template v-slot="scope">
                        <el-button class="delete-btn" type="danger" :icon="Delete" @click="deleteImage(scope.row)" circle />
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
        </div>


<!-- 添加应用表单 -->
        <div v-else>

            <div class="header">
                <span>镜像设置</span>
            </div>
            <el-form :model="imageModel" label-width="120px">
                    <el-form-item label="镜像名">
                        <el-input v-model="imageModel.name" placeholder="请输入镜像名"></el-input>
                    </el-form-item>
                    <el-form-item label="初始镜像">
                        <el-select placeholder="请选择" v-model="imageModel.create_image">
                            <el-option v-for="image in images" :key="image.id" :label="image.name" :value="image.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="容器封面" >
                        <img :src="fi" class="avatar" id='img1' width="120px" height="120px" />

                        <input type="file" class="avatar-uploader"  @change="showImg" id="fileImage" name="fileImage" style="display:none;"/>

                        <label for="fileImage">
                            <div class="lBut"><span>选择文件</span></div>
                        </label>
                        
                    </el-form-item>
                    
                    <el-form-item>
                        <el-button type="primary" @click="addImage()" :loading="isSending">创建</el-button>
                        <el-button type="info" @click="addSwitch=true; clearData()">取消</el-button>
                    </el-form-item>

            </el-form>

        </div>
    </el-card>


    
    <el-card class="page-app">
        <div v-if="addSwitch">
            <div class="header">
                <span>镜像详情</span>
            </div>

            <el-form-item label="图标">
                <el-image style="width: 150px; height: 150px" :src="imageDetail.icon" :fit="fit" />
            </el-form-item>

            <el-form-item label="镜像名称">
            <el-input v-model="imageDetail.name" disabled/>
            </el-form-item>

            <el-form-item label="父镜像镜像名称">
            <el-input v-model="imageDetail.parent_image_name" disabled/>
            </el-form-item>

            <el-form-item label="app组成">
                <div v-for="(app, index) in imageDetail.app" :key="index">
                    {{ app.name }}
                </div>
            </el-form-item>
        </div>

        <div v-else>
            <div class="header">
                <span>请在下表选择你所需添加的应用</span>
            </div>
            <el-table :data="apps" style="width: 100%" @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="55" align="center"/>
                <el-table-column label="应用名" prop="name"></el-table-column>
                <el-table-column label="图标" width="100px">
                    <template v-slot="scope">
                        <img :src="scope.row.icon" alt="" style="width: 80px;height:80px">
                    </template>
                </el-table-column>
                <template #empty>
                    <el-empty description="没有数据" />
                </template>
            </el-table>
        </div>


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

.el-input {
  --el-input-width: 220px;
}

.el-select {
  --el-select-width: 220px;
}

.page-image {
    min-height: 100%;
    width: 60%;
    float: left;
    box-sizing: border-box;
    .header {
    // margin-bottom: 100px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
}
.page-app {
    min-height: 100%;
    width: 39%;
    float: right;
    box-sizing: border-box;
    .header {
    // margin-bottom: 100px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    }
}

// .header {
//     display: flex;
//     align-items: center;
//     justify-content: space-between;
// }

</style>