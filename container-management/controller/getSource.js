const { ipcMain, BrowserWindow } = require('electron')

const getSource = ()=>{
    ipcMain.handle('on-url-event', (e, url)=>{
        console.log(url)
        return '我收到了'
    })
    return url
}


module.exports = getSource