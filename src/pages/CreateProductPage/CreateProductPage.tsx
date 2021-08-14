import React, { Component, useState, useReducer, useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import axios from 'axios';
import Layout from '../../components/Layout/Layout';
import './CreateProductPage.scss';
import img_plain from '../../static/imgs_temp/plain.jpg';
import img_sketch from '../../static/imgs_temp/sketch.jpg';
import img_contours from '../../static/imgs_temp/contours.jpg';
import img_anime from '../../static/imgs_temp/anime.jpg';

// import * as cv from 'opencv4nodejs';
// var cv = require('opencv.js');
// console.log('cv', cv);

const CreateProductPage = (props: any) => {
  const initState = {};
  const [state, setState] = useState(initState);
  // const [t, setT] = useState<any>(null);
  const [imgs, setImgs] = useState<{
    plain: string;
    sketch: string;
    contours: string;
    anime: string;
  }>({
    // plain: '', //未修的图
    // sketch: '', //素描风
    // contours: '', //线稿
    // anime: '', //动画风
    plain: require('../../static/imgs_temp/plain.jpg').default,
    sketch: require('../../static/imgs_temp/sketch.jpg').default,
    contours: require('../../static/imgs_temp/sketch.jpg').default,
    anime: require('../../static/imgs_temp/sketch.jpg').default,
  });
  const ref_inputImg = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // let path = 'http://127.0.0.1:5000/get-imgs';
    // axios
    //   .get(path)
    //   .then(function (res) {
    //     console.log('res-', res);
    //   })
    //   .catch(function (error) {
    //     console.log(error);
    //   });
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
    /*//多图的方法：
    const files = [...e.target.files];
    let result = await Promise.all(
      files.map(file => {
         let url = window.URL.createObjectURL(file);
         return {
          name: file.name,
          url: url,
        };
      })
    );
    */

    let file = e.target.files[0];
    let objUrl = window.URL.createObjectURL(file);
    console.log('file', file, 'objUrl', objUrl);

    // await setImgs({
    //   ...imgs,
    //   plain: objUrl,
    // });

    //图片发到后端处理
    let formData = new FormData();
    formData.append('file', file);
    console.log('formData', formData.get('file')); //*console.log FormData() 时要用.get() 否则输出会为空
    axios
      // .post('http://127.0.0.1:5000/post-imgs', formData)
      .post('http://127.0.0.1:5000/upload', formData)
      .then(response => {
        console.log('response', response);
        if (!(response && response.data && response.data.img_paths)) {
          return;
        }
        let img_paths = response.data.img_paths;
        let base_path = '../../static/imgs_temp/';
        console.log('img_paths', img_paths);
        //*problem 这里是在手动等后端写入文件，否则会显示旧文件
        setTimeout(() => {
          setImgs({
            ...imgs,
            plain: objUrl,
            // sketch: require(base_path + response.data.img_paths.sketch.split('/').slice(-1)).default,
            // contours: base_path + response.data.img_paths.contours.split('/').slice(-1),
            // anime: base_path + response.data.img_paths.anime.split('/').slice(-1),
            sketch: require('../../static/imgs_temp/sketch.jpg').default,
            contours: require('../../static/imgs_temp/sketch.jpg').default,
            anime: require('../../static/imgs_temp/sketch.jpg').default,
          });
        }, 1000);
        // console.log('sketch_path', sketch_path);
        // setT(require('../../static/imgs_temp/sketch.jpg'));
        // setT(require('' + sketch_path));
      })
      .catch(err => {
        console.log(err);
      });
  };

  // const x = require('../../static/imgs_temp/sketch.jpg');
  // const x = require(`${imgs.sketch}`);
  // console.log('imgs.sketch', imgs.sketch);
  // console.log('t', t);

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
          {imgs.contours.length > 0 && <img src={img_contours} alt='' />}
        </div>
        <div className='an_img'>
          <div>动画风：</div>
          {imgs.anime.length > 0 && <img src={img_anime} alt='' />}
        </div>
      </div>
    </Layout>
  );
};
CreateProductPage.defaultProps = {};
export default CreateProductPage;
