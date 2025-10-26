import request from '@/utils/request';

// 入庫タスク
export function stockInOrdersList(params) {
  return request({ url: `/stock_in_orders/`, method: 'get', params })
}
// 入庫通知伝票
export function stockInOrderDetail(params) {
  return request({ url: `/stock_in_orders/${params.id}/`, method: 'get', params })
}
// 入庫記録
export function stockInRecordsList(params) {
  return request({ url: `/stock_in_records/`, method: 'get', params })
}
// 入庫
export function stockInCreate(data) {
  return request({ url: `/stock_in_records/`, method: 'post', data })
}
// 入庫記録詳細
export function stockInRecordDetail(params) {
  return request({ url: `/stock_in_records/${params.id}/`, method: 'get', params })
}

// 入庫レコードが無効です
export function stockInOrdersVoid(data) {
  return request({ url: `/stock_in_records/${data.id}/void/`, method: 'post', data })
}

// 出庫タスク
export function stockOutOrdersList(params) {
  return request({ url: `/stock_out_orders/`, method: 'get', params })
}
// 出庫通知文書
export function stockOutOrderDetail(params) {
  return request({ url: `/stock_out_orders/${params.id}/`, method: 'get', params })
}
// 入庫から出た
export function stockOutCreate(data) {
  return request({ url: `/stock_out_records/`, method: 'post', data })
}
// 出庫記録
export function stockOutRecordsList(params) {
  return request({ url: `/stock_out_records/`, method: 'get', params })
}
// 出庫記録詳細
export function stockOutRecordDetail(params) {
  return request({ url: `/stock_out_records/${params.id}/`, method: 'get', params })
}
// 出庫記録無効
export function stockOutOrdersVoid(data) {
  return request({ url: `/stock_out_records/${data.id}/void/`, method: 'post', data })
}

// 在庫振替
export function stockTransferOrdersList(params) {
  return request({ url: `/stock_transfer_orders/`, method: 'get', params })
}
// 在庫振替記録無効
export function stockTransferOrdersVoid(data) {
  return request({ url: `/stock_transfer_orders/${data.id}/void/`, method: 'post', data })
}
// 在庫振替
export function stockTransferCreate(data) {
  return request({ url: `/stock_transfer_orders/`, method: 'post', data })
}
// 在庫振替詳細
export function stockTransferDetail(params) {
  return request({ url: `/stock_transfer_orders/${params.id}/`, method: 'get', params })
}

// 棚卸
export function stockCheckOrdersList(params) {
  return request({ url: `/stock_check_orders/`, method: 'get', params })
}
// 棚卸記録無効
export function stockCheckOrdersVoid(data) {
  return request({ url: `/stock_check_orders/${data.id}/void/`, method: 'post', data })
}
// 棚卸
export function stockCheckCreate(data) {
  return request({ url: `/stock_check_orders/`, method: 'post', data })
}
// 在庫振替詳細
export function stockCheckDetail(params) {
  return request({ url: `/stock_check_orders/${params.id}/`, method: 'get', params })
}

// 在庫推移
export function inventoryFlowsList(params) {
  return request({ url: `/inventory_flows/`, method: 'get', params })
}
// 在庫推移詳細
export function inventoryFlowsDetail(params) {
  return request({ url: `/inventory_flows/${params.id}/`, method: 'get', params })
}
// export function materialStockInCreate(data) {
//   return request({ url: `/material_stock_in_orders/`, method: 'post', data })
// }

// export function materialStockInUpdate(data) {
//   return request({ url: `/material_stock_in_orders/${data.id}/`, method: 'put', data })
// }

// export function materialStockInDestroy(data) {
//   return request({ url: `/material_stock_in_orders/${data.id}/`, method: 'delete', data })
// }

// export function materialStockInDetail(params) {
//   return request({ url: `/material_stock_in_orders/${params.id}/`, method: 'get', params })
// }

// export function materialStockInConfirm(data) {
//   return request({ url: `/material_stock_in_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 原料出庫
// export function materialStockOutList(params) {
//   return request({ url: `/material_stock_out_orders/`, method: 'get', params })
// }

// export function materialStockOutCreate(data) {
//   return request({ url: `/material_stock_out_orders/`, method: 'post', data })
// }

// export function materialStockOutUpdate(data) {
//   return request({ url: `/material_stock_out_orders/${data.id}/`, method: 'put', data })
// }

// export function materialStockOutDestroy(data) {
//   return request({ url: `/material_stock_out_orders/${data.id}/`, method: 'delete', data })
// }

// export function materialStockOutDetail(params) {
//   return request({ url: `/material_stock_out_orders/${params.id}/`, method: 'get', params })
// }

// export function materialStockOutConfirm(data) {
//   return request({ url: `/material_stock_out_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 原料在庫
// export function materialInventoriesList(params) {
//   return request({ url: `/material_inventories/`, method: 'get', params })
// }

// // 原料入出庫明細
// export function materialInventoryFlowsList(params) {
//   return request({ url: `/material_inventory_flows/`, method: 'get', params })
// }

// // 完成品入庫
// export function productStockInList(params) {
//   return request({ url: `/product_stock_in_orders/`, method: 'get', params })
// }

// export function productStockInCreate(data) {
//   return request({ url: `/product_stock_in_orders/`, method: 'post', data })
// }

// export function productStockInUpdate(data) {
//   return request({ url: `/product_stock_in_orders/${data.id}/`, method: 'put', data })
// }

// export function productStockInDestroy(data) {
//   return request({ url: `/product_stock_in_orders/${data.id}/`, method: 'delete', data })
// }

// export function productStockInDetail(params) {
//   return request({ url: `/product_stock_in_orders/${params.id}/`, method: 'get', params })
// }

// export function productStockInConfirm(data) {
//   return request({ url: `/product_stock_in_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 商品出庫
// export function productStockOutList(params) {
//   return request({ url: `/product_stock_out_orders/`, method: 'get', params })
// }

// export function productStockOutCreate(data) {
//   return request({ url: `/product_stock_out_orders/`, method: 'post', data })
// }

// export function productStockOutUpdate(data) {
//   return request({ url: `/product_stock_out_orders/${data.id}/`, method: 'put', data })
// }

// export function productStockOutDestroy(data) {
//   return request({ url: `/product_stock_out_orders/${data.id}/`, method: 'delete', data })
// }

// export function productStockOutDetail(params) {
//   return request({ url: `/product_stock_out_orders/${params.id}/`, method: 'get', params })
// }

// export function productStockOutConfirm(data) {
//   return request({ url: `/product_stock_out_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 商品在庫
// export function productInventoriesList(params) {
//   return request({ url: `/product_inventories/`, method: 'get', params })
// }

// // 商品入出庫明細
// export function productInventoryFlowsList(params) {
//   return request({ url: `/product_inventory_flows/`, method: 'get', params })
// }