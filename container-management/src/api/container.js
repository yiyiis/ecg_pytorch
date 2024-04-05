import request from '@/utils/request'

/**@type { import('axios').AxiosInstance } req */
let req = request

export const containerListService = ()=>{
    return request.get('/container')
}


export const containerRunService = (id) => {
    // console.log('/container/run/${id}')
    return request.post(`/container/run/${id}`);
}


export const containerAddService = (containerData) => {
    return request.post(`/container/create`, containerData);
}

export const containerDeleteService = (id) => {
    // console.log('/container/${id}')
    return request.delete(`/container/${id}`);
}


export const containerStopService = (id) => {
    // console.log('/container/pause/${id}')
    return request.post(`/container/pause/${id}`);
}

export const containerSearchService = (containerData) => {
    // console.log('/container/pause/${id}')
    return req.get(`/container/search`, {
        params: containerData
    });
}