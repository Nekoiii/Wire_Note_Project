import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import rootReducer from '../../redux/reducers'

const middlewares = [
    thunkMiddleware,
    createLogger()
]

export default function configStore() {
    const store = createStore(rootReducer, applyMiddleware(...middlewares));
    return store;
}

