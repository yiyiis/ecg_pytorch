import request from '@/utils/request'


export const userRegisterService = (registerData)=>{

    delete registerData.rePassword
    return request.post('/user/register', registerData)
}



export const userLoginService = async (loginData)=>{

    delete loginData.rePassword
    return request.post('/user/login', loginData)
}

