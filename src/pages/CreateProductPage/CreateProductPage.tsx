import React, {
  Component,
  useState,
  useReducer,
  useEffect,
  useRef,
} from 'react';
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
  const [imgs, setImgs] = useState<any>({
    plain: [], //未修的图
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
        return {
          name: file.name,
          url: url,
        };
      })
    );
    await setImgs({
      ...imgs,
      plain: result.map((it) => {
        return it.url;
      }),
    });
    result.forEach((it) => {
      // axios({
      //   method: 'post',
      //   url: 'http://127.0.0.1:5000/post-imgs',
      //   data: {
      //     name: it.name,
      //     url: it.url,
      //   },
      // })
      axios
        .post('http://127.0.0.1:5000/post-imgs', {
          name: it.name,
          url: it.url,
        })
        .then(function (response) {
          console.log('response', response);
        })
        .catch(function (error) {
          console.log(error);
        });
    });

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
        {imgs.plain && imgs.plain.length > 0 && (
          <img src={imgs.plain[0]} alt="" />
        )}
      </div>
    </Layout>
  );
};
CreateProductPage.defaultProps = {};
export default CreateProductPage;
