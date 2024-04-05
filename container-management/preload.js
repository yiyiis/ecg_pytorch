// const fs = require('fs')

// console.log(fs)

// fs.writeFile('./text.txt', '123', ()=>{
//     console.log('done.')
// })

console.log(process.platform)



const { contextBridge, ipcRenderer, clipboard, nativeImage } = require('electron')

const handleSend = async ()=>{
    let fallback = await ipcRenderer.invoke('send-event', 'hahaha')
    console.log(fallback)
}

const copy=()=>{
    // console.log("???")
    clipboard.writeText('hello clipboard')
}

const show=()=>{
    const text = clipboard.readText()
    console.log(text)
}

const capture = async () =>  {
    let sources = await ipcRenderer.invoke('capture-event')
    for (const source of sources) {
        if (source.name === '整个屏幕') {
          console.log(source)
          let str = source.thumbnail.crop({x:0, y:0,width:100,height:100})
            const imgSrc = str.toDataURL()
          console.log(imgSrc)
          return imgSrc
          
        }
      }
}

const testNativeImage = () =>{
    const image = nativeImage.createFromPath('./1.png')
    console.log(image)
}

contextBridge.exposeInMainWorld('myApi', {
    platform: process.platform,
    handleSend,
    copy,
    show,
    capture,
    testNativeImage,
})

