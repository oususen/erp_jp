import request from '@/utils/request';

// 顧客
export function clientList(params) {
  return request({ url: `/clients/`, method: 'get', params })
}

export function clientCreate(data) {
  return request({ url: `/clients/`, method: 'post', data })
}

export function clientUpdate(data) {
  return request({ url: `/clients/${data.id}/`, method: 'put', data })
}

export function clientDestroy(data) {
  return request({ url: `/clients/${data.id}/`, method: 'delete', data })
}

// 仕入先
export function supplierList(params) {
  return request({ url: `/suppliers/`, method: 'get', params })
}

export function supplierCreate(data) {
  return request({ url: `/suppliers/`, method: 'post', data })
}

export function supplierUpdate(data) {
  return request({ url: `/suppliers/${data.id}/`, method: 'put', data })
}

export function supplierDestroy(data) {
  return request({ url: `/suppliers/${data.id}/`, method: 'delete', data })
}

// 入庫
export function warehouseList(params) {
  return request({ url: `/warehouses/`, method: 'get', params })
}

export function warehouseCreate(data) {
  return request({ url: `/warehouses/`, method: 'post', data })
}

export function warehouseUpdate(data) {
  return request({ url: `/warehouses/${data.id}/`, method: 'put', data })
}

export function warehouseDestroy(data) {
  return request({ url: `/warehouses/${data.id}/`, method: 'delete', data })
}

// 決済口座
export function settlementAccountList(params) {
  return request({ url: `/accounts/`, method: 'get', params })
}

export function settlementAccountCreate(data) {
  return request({ url: `/accounts/`, method: 'post', data })
}

export function settlementAccountUpdate(data) {
  return request({ url: `/accounts/${data.id}/`, method: 'put', data })
}

export function settlementAccountDestroy(data) {
  return request({ url: `/accounts/${data.id}/`, method: 'delete', data })
}

// 収支項目
export function revenueExpenditureItemsList(params) {
  return request({ url: `/charge_items/`, method: 'get', params })
}

export function revenueExpenditureItemsCreate(data) {
  return request({ url: `/charge_items/`, method: 'post', data })
}

export function revenueExpenditureItemsUpdate(data) {
  return request({ url: `/charge_items/${data.id}/`, method: 'put', data })
}

export function revenueExpenditureItemsDestroy(data) {
  return request({ url: `/charge_items/${data.id}/`, method: 'delete', data })
}

// // 原料マスタ
// export function materialDictList(params) {
//   return request({ url: `/materials/`, method: 'get', params })
// }

// export function materialDictCreate(data) {
//   return request({ url: `/materials/`, method: 'post', data })
// }

// export function materialDictUpdate(data) {
//   return request({ url: `/materials/${data.id}/`, method: 'put', data })
// }

// export function materialDictDestroy(data) {
//   return request({ url: `/materials/${data.id}/`, method: 'delete', data })
// }

// // 商品マスタ
// export function productsDictList(params) {
//   return request({ url: `/products/`, method: 'get', params })
// }

// export function productsDictCreate(data) {
//   return request({ url: `/products/`, method: 'post', data })
// }

// export function productsDictUpdate(data) {
//   return request({ url: `/products/${data.id}/`, method: 'put', data })
// }

// export function productsDictDestroy(data) {
//   return request({ url: `/products/${data.id}/`, method: 'delete', data })
// }

