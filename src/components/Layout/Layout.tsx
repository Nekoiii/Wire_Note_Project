import React, { Component, useState, useReducer, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Navbar from './Navbar/Navbar';

import './Layout.scss';

const Layout = (props: any) => {
  const initState = {};
  const [state, setState] = useState(initState);

  useEffect(() => {}, []);

  return (
    <div className={' '.concat(props.className)}>
      <Navbar />
      {props.children}
    </div>
  );
};
Layout.defaultProps = {};
export default Layout;
