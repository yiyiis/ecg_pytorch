const {contextBridge, ipcRenderer} = require('electron')

const sendUrl = async (url) =>{
    let result = await ipcRenderer.invoke('on-url-event', url)
    console.log(result)
}

const sendU = async(url) =>{
    await ipcRenderer.invoke('getu', url)
}

contextBridge.exposeInMainWorld('myApi',{
    sendUrl,
    sendU
})

