import * as actionsTypes from '../constants/userManager'
import { Dispatch } from 'redux';

export const doRegister=()=>{
  return (dispatch:Dispatch)=>{
    dispatch({
      type:actionsTypes.DO_REGISTER,
    })
  }
}