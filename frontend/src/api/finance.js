import request from '@/utils/request';

// 支払いい
export function paymentOrdersList(params) {
  return request({ url: `/payment_orders/`, method: 'get', params })
}
// 支払いい記録が無効です
export function paymentOrdersVoid(data) {
  return request({ url: `/payment_orders/${data.id}/void/`, method: 'post', data })
}
// 支払い新規登録い
export function paymentOrderCreate(data) {
  return request({ url: `/payment_orders/`, method: 'post', data })
}
// お支払いいい詳細
export function paymentOrderDetail(params) {
  return request({ url: `/payment_orders/${params.id}/`, method: 'get', params })
}

// 入金
export function collectionOrdersList(params) {
  return request({ url: `/collection_orders/`, method: 'get', params })
}
// 支払いい記録が無効です
export function collectionOrdersVoid(data) {
  return request({ url: `/collection_orders/${data.id}/void/`, method: 'post', data })
}
// 新しい支払いいいの徴収
export function collectionOrderCreate(data) {
  return request({ url: `/collection_orders/`, method: 'post', data })
}
// お支払いいい詳細
export function collectioOrderDetail(params) {
  return request({ url: `/collection_orders/${params.id}/`, method: 'get', params })
}

// 買掛金
export function arrearsPayableList(params) {
  return request({ url: `/supplier_arrears/`, method: 'get', params })
}
// 売掛金
export function arrearsReceivableList(params) {
  return request({ url: `/client_arrears/`, method: 'get', params })
}

// 振出元口座
export function accountTransferOrdersList(params) {
  return request({ url: `/account_transfer_records/`, method: 'get', params })
}
// 振出元口座記録無効
export function accountTransferOrdersVoid(data) {
  return request({ url: `/account_transfer_records/${data.id}/void/`, method: 'post', data })
}
// 振出元口座新規登録しました
export function accountTransferOrderCreate(data) {
  return request({ url: `/account_transfer_records/`, method: 'post', data })
}

// 日常収支
export function chargeOrdersList(params) {
  return request({ url: `/charge_orders/`, method: 'get', params })
}
// 日常収支記録無効
export function chargeOrdersVoid(data) {
  return request({ url: `/charge_orders/${data.id}/void/`, method: 'post', data })
}
// 日常収支新規登録
export function chargeOrderCreate(data) {
  return request({ url: `/charge_orders/`, method: 'post', data })
}

// 資金明細
export function financeFlowsList(params) {
  return request({ url: `/finance_flows/`, method: 'get', params })
}
// 資金明細詳細
export function financeFlowDetail(params) {
  return request({ url: `/finance_flows/${params.id}/`, method: 'get', params })
}

// // 購買記録無効
// export function purchaseOrdersVoid(data) {
//   return request({ url: `/purchase_orders/${data.id}/void/`, method: 'post', data })
// }

// // 購買返品伝票
// export function purchaseReturnOrderCreate(data) {
//   return request({ url: `/purchase_return_orders/`, method: 'post', data })
// }

// // 返品記録
// export function purchaseReturnOrdersList(params) {
//   return request({ url: `/purchase_return_orders/`, method: 'get', params })
// }