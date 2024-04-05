const { app, BrowserWindow, session, ipcMain } = require('electron')
const { inject, ref } =  require('vue')
const path = require('path')

const Winstate = require('electron-win-state').default
const getSource = require('./controller/getSource.js')


// 忽略证书相关错误
app.commandLine.appendSwitch('ignore-certificate-errors')

const win_url = ref('')

const createWindow = ()=>{
    const winState = new Winstate({
        defaultWidth: 1000,
        defaultHeight: 800
    })


    const win = new BrowserWindow({
        ...winState.winOptions,
        webPreferences:{
            preload: path.join(__dirname, './preload/index.js'),
            // sandbox:false
        },



        show: false
    })

    win.loadURL("http://localhost:5173")

    win.webContents.openDevTools()

    winState.manage(win)

    win.on('ready-to-show', ()=>{
        win.show()
    })


    
    const getU = ()=>{
        ipcMain.handle('getu', (e, url)=>{
            win_url.value = url
            // console.log(win_url.value)
            // console.log('https://'+win_url.value+'/*')
            // console.log()
            session.defaultSession.webRequest.onBeforeSendHeaders(
                {urls: ['https://'+win_url.value+'/*', 'wss://' + win_url.value+'/websockify/*']}
              , (details, callback) => {
                details.requestHeaders['Authorization'] = 'Basic a2FzbV91c2VyOnBhc3N3b3Jk'
                callback({requestHeaders: details.requestHeaders})
              })
        })
    }
    

    getU()


}



app.whenReady().then(()=>{
    createWindow()

    app.on('activate', ()=>{
        if(BrowserWindow.getAllWindows().length === 0){
            createWindow()
        }
    })


})


app.on('window-all-closed', ()=>{
    if(process.platform === 'win32'){
        app.quit()
    }
})

// //当一个新的 webContents 被创建时触发。
// app.on('web-contents-created',function(event,webContents){
// 	webContents.setWindowOpenHandler((details) => {
// 		if (details.url) {
// 			return { 
// 				action: 'allow',//允许新窗口被创建
// 				overrideBrowserWindowOptions: {//允许自定义创建的窗口参数
// 					width: 1400,
// 					minWidth: 1400,
// 					minHeight: 800,
// 					height: 800,
// 					autoHideMenuBar: true,//自动隐藏菜单栏
// 					parent: null ,//指定父窗口
// 					// x: 0,
// 					// y: 0,
// 					resizable: true,
// 					webPreferences: {//网页功能设置。
// 						preload: path.join(__dirname, 'preload.js'),//在页面运行其他脚本之前预先加载指定的脚本 无论页面是否集成Node, 此脚本都可以访问所有Node API 脚本路径为文件的绝对路径。
// 						webSecurity: false,//禁用同源策略
// 						nodeIntegration: true,
// 						nodeIntegrationInWorker: true,
// 					},
// 				}
				
// 			}
// 	    }
// 	    return { action: 'deny' }//取消创建新窗口
// 	})
// })
