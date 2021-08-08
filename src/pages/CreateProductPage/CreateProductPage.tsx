import React, { Component, useState, useReducer, useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import axios from 'axios';
import Layout from '../../components/Layout/Layout';

import './CreateProductPage.scss';

// import * as cv from 'opencv4nodejs';
// var cv = require('opencv.js');
// console.log('cv', cv);

const CreateProductPage = (props: any) => {
  const initState = {};
  const [state, setState] = useState(initState);
  const [imgs, setImgs] = useState<{
    plain: string;
    sketch: string;
    contours: string;
    anime: string;
  }>({
    plain: '', //未修的图
    sketch: '', //素描风
    contours: '', //线稿
    anime: '', //动画风
  });
  const ref_inputImg = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let path = 'http://127.0.0.1:5000/get-imgs';
    axios
      .get(path)
      .then(function (res) {
        console.log('res-', res);
      })
      .catch(function (error) {
        console.log(error);
      });
  }, []);

  const handleClick = (way: string, e?: any) => {
    switch (way) {
      case 'UPLOAD_IMG':
        ref_inputImg && ref_inputImg.current && ref_inputImg.current.click();
        break;

      default:
        break;
    }
  };

  const loadImg = async (e: any) => {
    if (!(e && e.target && e.target.files && e.target.files.length > 0)) {
      return;
    }

    // //多图的方法：
    // const files = [...e.target.files];
    // let result = await Promise.all(
    //   files.map(file => {
    //      let url = window.URL.createObjectURL(file);
    //      return {
    //       name: file.name,
    //       url: url,
    //     };
    //   })
    // );

    let file = e.target.files[0];
    console.log('file', file);
    let objUrl = window.URL.createObjectURL(file);

    console.log('objUrl', objUrl);

    await setImgs({
      ...imgs,
      plain: objUrl,
    });

    let formData = new FormData();
    formData.append('file', file);
    console.log('formData', formData.get('file')); //*console.log FormData() 时要用.get() 否则输出会为空
    // result.forEach((it) => {
    // axios({
    //   method: 'post',
    //   url: 'http://127.0.0.1:5000/post-imgs',
    //   data: {
    //     name: it.name,
    //     url: it.ur,l
    //   },
    // })
    axios
      .post('http://127.0.0.1:5000/post-imgs', formData)
      .then(function (response) {
        console.log('response', response);
      })
      .catch(function (error) {
        console.log(error);
      });
    // });

    // console.log('img_url', result);
  };

  console.log('t', imgs.plain);

  return (
    <Layout className={'create_product_page '.concat(props.className)}>
      <div className='mc_button upload_button' onClick={() => handleClick('UPLOAD_IMG')}>
        上传图片
      </div>
      <input type='file' ref={ref_inputImg} style={{ visibility: 'hidden' }} onChange={e => loadImg(e)} />
      <div className='img_gallery'>
        <div className='an_img'>
          <div>原图：</div>
          {imgs.plain.length > 0 && <img src={imgs.plain} alt='' />}
        </div>
        <div className='an_img'>
          <div>素描风：</div>
          {imgs.sketch.length > 0 && <img src={imgs.sketch} alt='' />}
        </div>
        <div className='an_img'>
          <div>线稿：</div>
          {imgs.contours.length > 0 && <img src={imgs.contours} alt='' />}
        </div>
        <div className='an_img'>
          <div>动画风：</div>
          {imgs.anime.length > 0 && <img src={imgs.anime} alt='' />}
        </div>
      </div>
    </Layout>
  );
};
CreateProductPage.defaultProps = {};
export default CreateProductPage;
