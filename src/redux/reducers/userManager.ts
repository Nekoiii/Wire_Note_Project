import * as actionsTypes from '../constants/userManager';

const INITIAL_STATE = {
  userId: '',
};
// const INITIAL_STATE = {
//   userId: '123',
//   userName: '猫草',
//   userIcon: '',
// };

const doRegister = (state: any, action: any) => {
  return {
    ...state,
  };
};

export default function userManager(state = INITIAL_STATE, action: any) {
  switch (action.type) {
    case actionsTypes.DO_REGISTER:
      return doRegister(state, action);
    default:
      return state;
  }
}
