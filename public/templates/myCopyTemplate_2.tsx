import React, { Component, useState, useReducer, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import './XXX.scss';

const XXX = (props: any) => {
  const initState = {};
  const [state, setState] = useState<any>(initState);

  useEffect(() => {}, []);

  return (
    <div className={''.concat(props.className)}>
      <div></div>
    </div>
  );
};
XXX.defaultProps = {};
export default XXX;
