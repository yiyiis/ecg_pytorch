import request from '@/utils/request'

export const postPhoto = (id, _formData)=>{
    console.log(`/icon/${id}`)
    console.log(_formData)
    return request.post(`/icon/${id}`, _formData)
}
