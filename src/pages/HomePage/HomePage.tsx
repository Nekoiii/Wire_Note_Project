import React from 'react';
import { BrowserRouter, Route, Switch, useHistory } from 'react-router-dom';
import Layout from '../../components/Layout/Layout';
import { Link } from 'react-router-dom';

import './HomePage.scss';

const home_icon = require('../../resources/imgs/my_icon.png').default;

/*
主页
*/
const HomePage = (props: any) => {
  const initState = {};
  const state = {};
  const history = useHistory();

  //跳转页面
  const redierectTo = (page: string) => {
    switch (page) {
      case 'CoronaPredict':
        history.push('corona-predict');
        break;

      default:
        break;
    }
  };

  return (
    <Layout className='home_page'>
      <div className='info_box'>
        <img className='my_icon' src={home_icon} alt='' />
        <div>猫草</div>
        <div className='platforms_box'>
          <div>bilili(主要驻地, 能找到所有视频作品): 东京打工人猫草</div>
          <div>抖音(只发手绘动画): 东京打工人猫草</div>
          <div>Youtube(只发部分手绘动画): 東京社会人猫草</div>
          <div>CSDN(只发IT相关): _猫草</div>
          <div>OpenSea(所有nft作品): https://opensea.io/collections</div>
        </div>
        <div className='menu-box'>
          <div className='mc_button' onClick={() => redierectTo('CoronaPredict')}>
            新冠预测
          </div>
        </div>
      </div>
    </Layout>
  );
};
HomePage.defaultProps = {};
export default HomePage;
