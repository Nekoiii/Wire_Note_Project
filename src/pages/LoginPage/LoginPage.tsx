import React, { Component, useState, useReducer, useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Layout from '../../components/Layout/Layout';

import './LoginPage.scss';

/*
登录页。
*/
const LoginPage = (props: any) => {
  const [tab, setTab] = useState('LOGIN'); //'LOGIN','REGISTER'
  const initUser = {
    userId: '',
    userName: '',
  };
  const [user, setUser] = useState(initUser);

  const changeInput = (way: string, v: any) => {
    switch (way) {
      case 'USER_ID':
        setUser({
          ...user,
          userId: v.target.value,
        });
        break;
      case 'USER_NAME':
        setUser({
          ...user,
          userName: v.target.value,
        });
        break;

      default:
        break;
    }
  };

  return (
    <Layout className={'login_page '.concat(props.className)}>
      <div className="login_box">
        <div className="login_box_title">
          {tab === 'LOGIN' ? '登录' : '注册'}
        </div>
        <div className="input_form">
          <div className="input_item">
            <div className="input_item_title">ID:</div>
            <input
              type="text"
              value={user.userId}
              onChange={(v) => changeInput('USER_ID', v)}
            />
          </div>
          <div className="input_item">
            <div className="input_item_title">用户名:</div>
            <input
              type="text"
              value={user.userName}
              onChange={(v) => changeInput('USER_NAME', v)}
            />
          </div>
        </div>
      </div>
    </Layout>
  );
};
LoginPage.defaultProps = {};
export default LoginPage;
