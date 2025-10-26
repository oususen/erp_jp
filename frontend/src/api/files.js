import Cookies from 'js-cookie'
import axios from 'axios'

// 商品画像をアップロードする
export function contractOriginalFiles(data) {
  return axios({
    url: '/api/goods_images/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// // 原本をアップロード
// export function contractOriginalFiles(data) {
//   return axios({
//     url: '/api/contract_original_files/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

// // コピーをアップロードする
// export function contractCopyFiles(data) {
//   return axios({
//     url: '/api/contract_copy_files/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

// // 図面をアップロードする
// export function contractDrawingFiles(data) {
//   return axios({
//     url: '/api/drawing_files/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }