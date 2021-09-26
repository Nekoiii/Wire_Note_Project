import React, { Component, useState, useReducer, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import LoginPage from '../../../pages/LoginPage/LoginPage';
import './Navbar.scss';
import '../../../design/design.scss';
const home_icon = require('../../../resources/imgs/my_icon.png').default;

const Navbar = (props: any) => {
  // @ts-ignore   ts忽视单行报错的方法
  const dispatch = useDispatch();
  const userManager = useSelector((state: any) => state.userManager); //*这里加上:any才不会出ts的类型警告
  const initState = {};
  const [state, setState] = useState(initState);

  useEffect(() => {}, []);

  return (
    <div className={'navbar '.concat(props.className)}>
      <div className='navbar_content'>
        <Link to='/home-page'>
          <img className='home_icon' src={home_icon} alt='' />
        </Link>

        <div className='title' style={{ fontFamily: 'SetoFont' }}>
          猫草摆摊
        </div>
        <div>xxx</div>
        {/* {userManager && userManager.userId && userManager.userId.length > 0 ? (
        <div>{userManager.userName}</div>
      ) : (
        <Link to="/login">登录/注册</Link>
      )}
      <Link to="/create-products">创作新周边</Link> */}
      </div>
      <div className='line_horizontal_bold' />
    </div>
  );
};
Navbar.defaultProps = {};
export default Navbar;
