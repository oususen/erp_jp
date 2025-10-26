import request from '@/utils/request';

// 購買伝票作成
export function purchaseOrderCreate(data) {
  return request({ url: `/purchase_orders/`, method: 'post', data })
}

// 購買記録
export function purchaseOrderList(params) {
  return request({ url: `/purchase_orders/`, method: 'get', params })
}

// 購買記録詳細
export function purchaseOrderDetail(params) {
  return request({ url: `/purchase_orders/${params.id}/`, method: 'get', params })
}

// 購買記録無効
export function purchaseOrdersVoid(data) {
  return request({ url: `/purchase_orders/${data.id}/void/`, method: 'post', data })
}

// 購買返品伝票
export function purchaseReturnOrderCreate(data) {
  return request({ url: `/purchase_return_orders/`, method: 'post', data })
}

// 返品記録
export function purchaseReturnOrdersList(params) {
  return request({ url: `/purchase_return_orders/`, method: 'get', params })
}

// 返品記録詳細
export function purchaseReturnOrderDetail(params) {
  return request({ url: `/purchase_return_orders/${params.id}/`, method: 'get', params })
}

// 返品記録無効
export function purchaseReturnOrdersVoid(data) {
  return request({ url: `/purchase_return_orders/${data.id}/void/`, method: 'post', data })
}

