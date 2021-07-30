import React, {
  Component,
  useState,
  useReducer,
  useEffect,
  useRef,
} from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Layout from '../../components/Layout/Layout';

import './CreateProductPage.scss';

// import * as cv from 'opencv4nodejs';
// var cv = require('opencv.js');
// console.log('cv', cv);

const CreateProductPage = (props: any) => {
  const initState = {};
  const [state, setState] = useState(initState);
  const [imgs, setImgs] = useState<any>({
    original: [], //用户传的图
  });
  const ref_inputImg = useRef<HTMLInputElement>(null);

  useEffect(() => {}, []);

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
    if (!(e && e.target && e.target.files)) {
      return;
    }
    const files = [...e.target.files];
    console.log('files', files);

    let result = await Promise.all(
      files.map((file) => {
        let url = null;
        // @ts-ignore
        if (window.createObjectURL != undefined) {
          // @ts-ignore
          url = window.createObjectURL(file);
        } else if (window.URL != undefined) {
          url = window.URL.createObjectURL(file);
        } else if (window.webkitURL != undefined) {
          url = window.webkitURL.createObjectURL(file);
        }
        return url;
      })
    );
    await setImgs({
      ...imgs,
      original: result,
    });
    console.log('img_url-t');
    console.log('img_url', result);
  };

  return (
    <Layout className={'create_product_page '.concat(props.className)}>
      <div
        className="mc_button upload_button"
        onClick={() => handleClick('UPLOAD_IMG')}
      >
        上传图片
      </div>
      <input
        type="file"
        ref={ref_inputImg}
        style={{ visibility: 'hidden' }}
        onChange={(e) => loadImg(e)}
      />
      <div className="img_gallery">
        {imgs.original && imgs.original.length > 0 && (
          <img src={imgs.original[0]} alt="" />
        )}
      </div>
    </Layout>
  );
};
CreateProductPage.defaultProps = {};
export default CreateProductPage;
