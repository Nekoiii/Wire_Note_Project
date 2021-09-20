import React, { Component, useState, useReducer, useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import axios from 'axios';
import Layout from '../../components/Layout/Layout';
import './CoronaPredictPage.scss';

// import * as cv from 'opencv4nodejs';
// var cv = require('opencv.js');
// console.log('cv', cv);

const CoronaPredictPage = (props: any) => {
  const initState = {};
  const [state, setState] = useState(initState);

  useEffect(() => {}, []);

  return (
    <Layout className={'corona_predict_page '.concat(props.className)}>
      <div>今日新增:</div>
    </Layout>
  );
};

CoronaPredictPage.defaultProps = {};
export default CoronaPredictPage;
