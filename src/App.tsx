import React from 'react';
import logo from './logo.svg';
import { BrowserRouter, Router, Route, Switch, Redirect } from 'react-router-dom';
import { Provider } from 'react-redux';
import HomePage from './pages/HomePage/HomePage';
import StrollPage from './pages/StrollPage/StrollPage';
import LoginPage from './pages/LoginPage/LoginPage';
import CreateProductPage from './pages/CreateProductPage/CreateProductPage';
import CoronaPredictPage from './pages/CoronaPredictPage/CoronaPredictPage';

import configStore from './redux/store';

import './App.css';

const store = configStore();

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        {/* <Redirect to="/stroll" />
        <Redirect to="/login" /> */}
        {/* <Redirect to="/create-products" /> */}
        {/* <Redirect to='/corona-predict' /> */}
        <Redirect to='/home-page' />

        <Route path='/home-page' component={HomePage} />
        <Route path='/stroll' component={StrollPage} />
        <Route path='/login' component={LoginPage} />
        <Route path='/create-products' component={CreateProductPage} />
        <Route path='/corona-predict' component={CoronaPredictPage} />
      </BrowserRouter>
    </Provider>
  );
}

export default App;
