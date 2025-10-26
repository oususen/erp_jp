import request from '@/utils/request';

// 販売伝票作成
export function saleOrderCreate(data) {
  return request({ url: `/sales_orders/`, method: 'post', data })
}

// 販売記録
export function saleOrderList(params) {
  return request({ url: `/sales_orders/`, method: 'get', params })
}

// 販売記録詳細
export function saleOrderDetail(params) {
  return request({ url: `/sales_orders/${params.id}/`, method: 'get', params })
}

// 販売記録無効
export function saleOrdersVoid(data) {
  return request({ url: `/sales_orders/${data.id}/void/`, method: 'post', data })
}

// 販売返品
export function saleReturnOrderCreate(data) {
  return request({ url: `/sales_return_orders/`, method: 'post', data })
}

// 販売返品記録
export function saleReturnOrderList(params) {
  return request({ url: `/sales_return_orders/`, method: 'get', params })
}

// 販売返品詳細
export function saleReturnOrderDetail(params) {
  return request({ url: `/sales_return_orders/${params.id}/`, method: 'get', params })
}

// 販売タスク
export function saleTaskList(params) {
  return request({ url: `/sales_tasks/`, method: 'get', params })
}

// 新しい販売タスク
export function saleTaskCreate(data) {
  return request({ url: `/sales_tasks/`, method: 'post', data })
}


// 販売タスクを削除する
export function saleTaskDestroy(data) {
  return request({ url: `/sales_tasks/${data.id}/`, method: 'delete', data })
}