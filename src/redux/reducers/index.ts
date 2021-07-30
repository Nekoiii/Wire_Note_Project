import {
  combineReducers
} from "redux"
import userManager from './userManager'

const rootReducer =combineReducers({
  userManager,
})

export default rootReducer

export type RootState = ReturnType<typeof rootReducer>
export type DefaultRootState = ReturnType<typeof rootReducer>
