import React, { Component, useState, useReducer, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import words_obj from './words';

import './ChatRecordPage.scss';

interface chatRecords {
  char: string;
  words: string;
}

const ChatRecordPage = (props: any) => {
  const initState = {};
  const [state, setState] = useState<any>(initState);

  useEffect(() => {}, []);

  //拆分台词, 做成{char:'',words:''}放到list中
  //台词格式为: [角色id]#[台词]$
  const split_chat_record = (words: string, records_list: chatRecords[]) => {
    const split_words = words.split('$');
    split_words.map(it => {
      const [char, words] = it.split('#');
      char &&
        words &&
        records_list.push({
          char: char,
          words: words,
        });
    });
    return records_list;
  };
  /*
  char: 0:♀-猫草, 1:♀-被盗当事人, 2:♂-爱凑热闹,说话比较幼稚, 3:♂-程序员,理性派,
   4:♂-东北大哥,曾被骗过,容易冲动, 5:偶尔出现的群友, 6:偶尔出现的群友
  */
  const records_list_1: chatRecords[] = [];
  const records_list_2: chatRecords[] = [];
  split_chat_record(words_obj.words_1.words, records_list_1);
  split_chat_record(words_obj.words_2.words, records_list_2);

  /*
  char: 0:♀-被盗当事人, 1:♀-土豪朋友
  */

  /*
  获取头像
  id：角色id, me_id: 现在在哪个角色的视角
   */
  const id_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'z'];
  const get_icon_src = (id: number | string) => {
    let icon_src: string = '';
    //require好像不能用变量作为路径,只能写死?
    let icon_name = './icons/' + id + '.png';
    icon_src = require(icon_name).default;
    /*switch (id) { 
      case 'a':
        icon_src = require('./icons/a.png').default;
        break;
      case 'b':
        icon_src = require('./icons/b.png').default;
        break;
      case 'c':
        icon_src = require('./icons/c.png').default;
        break;
      case 'd':
        icon_src = require('./icons/d.png').default;
        break;
      case 'e':
        icon_src = require('./icons/e.png').default;
        break;
      case 'f':
        icon_src = require('./icons/f.png').default;
        break;
      case 'g':
        icon_src = require('./icons/g.png').default;
        break;
      case 'h':
        icon_src = require('./icons/h.png').default;
        break;
      default:
        break;
    }*/
    return icon_src;
  };

  const get_chat_div = (list: chatRecords[], me_id: string) => {
    return list.map(it => {
      return it.char === 'date' ? (
        <div className='chat_date border_none'>{it.words}</div>
      ) : (
        <div className={'word_item '.concat(it.char == me_id ? 'chat_box_right' : '').concat()}>
          <img src={get_icon_src(it.char)} className='icon' />
          {it.words[0] === '\t' || <img src={require('./icons/horn.png').default} className='icon_horn' />}
          <div className={'words '.concat(it.words[0] === '\t' ? 'border_none' : '')}>{it.words}</div>
        </div>
      );
    });
  };

  return (
    <div className={'chat_record_page '.concat(props.className)}>
      <div className='word_list'>{get_chat_div(records_list_1, words_obj.words_1.me_id)}</div>
      <div>Part -- 2</div>
      <div className='word_list'>{get_chat_div(records_list_2, words_obj.words_2.me_id)}</div>
    </div>
  );
};
ChatRecordPage.defaultProps = {};
export default ChatRecordPage;
