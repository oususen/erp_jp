import request from '@/utils/request';


// 入庫
export function getWarehouseNumber(params) {
  return request({ url: `/warehouses/number/`, method: 'get', params })
}

// 仕入先
export function getSupplierNumber(params) {
  return request({ url: `/suppliers/number/`, method: 'get', params })
}

// 顧客
export function getClientNumber(params) {
  return request({ url: `/clients/number/`, method: 'get', params })
}

// 決済口座
export function getSettlementAccountNumber(params) {
  return request({ url: `/accounts/number/`, method: 'get', params })
}

// 商品情報
export function getGoodsNumber(params) {
  return request({ url: `/goods/number/`, method: 'get', params })
}


// 日常購買
export function getPurchaseNumber(params) {
  return request({ url: `/purchase_requisitions/number/`, method: 'get', params })
}

// 購買伝票
export function getPurchaseOrderNumber(params) {
  return request({ url: `/purchase_orders/number/`, method: 'get', params })
}

// 購買返品伝票
export function getPurchaseReturnOrderNumber(params) {
  return request({ url: `/purchase_return_orders/number/`, method: 'get', params })
}

// 販売伝票作成
export function getSaleOrderNumber(params) {
  return request({ url: `/sales_orders/number/`, method: 'get', params })
}

// 販売返品
export function getSaleReturnOrderNumber(params) {
  return request({ url: `/sales_return_orders/number/`, method: 'get', params })
}

// 在庫振替伝票
export function getStockTransferOrderNumber(params) {
  return request({ url: `/stock_transfer_orders/number/`, method: 'get', params })
}

// 棚卸伝票
export function getStockCheckOrderNumber(params) {
  return request({ url: `/stock_check_orders/number/`, method: 'get', params })
}

// 支払いいい命令
export function getPaymentOrderNumber(params) {
  return request({ url: `/payment_orders/number/`, method: 'get', params })
}

// 入金伝票
export function getCollectionOrderNumber(params) {
  return request({ url: `/collection_orders/number/`, method: 'get', params })
}

// 日常収支
export function getChargeOrderNumber(params) {
  return request({ url: `/charge_orders/number/`, method: 'get', params })
}

// // 梱包明細書
// export function getPackingNumber(params) {
//   return request({ url: `/packing_orders/number/`, method: 'get', params })
// }

// // 原料入庫
// export function getMaterialStockInNumber(params) {
//   return request({ url: `/material_stock_in_orders/number/`, method: 'get', params })
// }

// // 原料出庫
// export function getMaterialStockOutNumber(params) {
//   return request({ url: `/material_stock_out_orders/number/`, method: 'get', params })
// }

// // 完成品入庫
// export function getProductStockInNumber(params) {
//   return request({ url: `/product_stock_in_orders/number/`, method: 'get', params })
// }

// // 商品出庫
// export function getProductStockOutNumber(params) {
//   return request({ url: `/product_stock_out_orders/number/`, method: 'get', params })
// }

// // 原料マスタ
// export function getmaterialDictNumber(params) {
//   return request({ url: `/materials/number/`, method: 'get', params })
// }

// // 商品マスタ
// export function getproductsDictNumber(params) {
//   return request({ url: `/products/number/`, method: 'get', params })
// }


// // Client
// export function clientList(params) {
//   return request({ url: `/clients/`, method: 'get', params })
// }

// export function clientCreate(data) {
//   return request({ url: `/clients/`, method: 'post', data })
// }

// export function clientUpdate(data) {
//   return request({ url: `/clients/${data.id}/`, method: 'put', data })
// }

// export function clientDestroy(data) {
//   return request({ url: `/clients/${data.id}/`, method: 'delete', data })
// }

// // Unit
// export function unitList(params) {
//   return request({ url: `/units/`, method: 'get', params })
// }

// export function unitCreate(data) {
//   return request({ url: `/units/`, method: 'post', data })
// }

// export function unitUpdate(data) {
//   return request({ url: `/units/${data.id}/`, method: 'put', data })
// }

// export function unitDestroy(data) {
//   return request({ url: `/units/${data.id}/`, method: 'delete', data })
// }
