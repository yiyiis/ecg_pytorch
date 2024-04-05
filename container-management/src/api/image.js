import request from '@/utils/request'

export const imageListService = ()=>{
    return request.get('/image')
}

export const imageDetailService = (id) => {
    // console.log('/container/run/${id}')
    return request.get(`/image/${id}`);
}

export const imageDeleteService = (id) => {
    // console.log('/container/${id}')
    return request.delete(`/image/${id}`);
}

export const imageAddService = (imageData) => {
    return request.post(`/image`, imageData);
}