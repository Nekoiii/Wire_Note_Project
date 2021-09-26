import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Layout from '../../components/Layout/Layout';

import './StrollPage.scss';
/*
逛街页。index页后进去后的第一页。
*/
const StrollPage = (props: any) => {
  const initState = {};
  const state = {};

  return (
    <Layout className='stroll_page'>
      <BrowserRouter>
        StrollPage
        {/* <Route path="/" component={} /> */}
      </BrowserRouter>
    </Layout>
  );
};
StrollPage.defaultProps = {};
export default StrollPage;
