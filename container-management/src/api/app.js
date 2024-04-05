import request from '@/utils/request'

export const appListService = ()=>{
    return request.get('/app')
}