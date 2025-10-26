import request from '@/utils/request';


// RoleOption
export function roleOption(params) {
  return request({ url: `/roles/options/`, method: 'get', params })
}

// UserOption
export function userOption(params) {
  return request({ url: `/users/options/`, method: 'get', params })
}

// 商品
export function materialsOption(params) {
  return request({ url: `/materials/options/`, method: 'get', params })
}
// 仕入先
export function suppliersOption(params) {
  return request({ url: `/suppliers/options/`, method: 'get', params })
}

// 顧客
export function clientsOption(params) {
  return request({ url: `/clients/options/`, method: 'get', params })
}
// 入庫
export function warehousesOption(params) {
  return request({ url: `/warehouses/options/`, method: 'get', params })
}
// 商品カテゴリ
export function goodsClassificationOption(params) {
  return request({ url: `/goods_categories/options/`, method: 'get', params })
}
// 商品単位
export function goodsUnitOption(params) {
  return request({ url: `/goods_units/options/`, method: 'get', params })
}
// 商品オプション
export function inventoriesOption(params) {
  return request({ url: `/inventories/options/`, method: 'get', params })
}
// 商品オプション
export function goodsOption(params) {
  return request({ url: `/goods/options/`, method: 'get', params })
}
// 決済口座
export function accountsOption(params) {
  return request({ url: `/accounts/options/`, method: 'get', params })
}
// 購買伝票
export function purchaseOrdersOption(params) {
  return request({ url: `/purchase_orders/options/`, method: 'get', params })
}
// 販売伝票
export function saleOrdersOption(params) {
  return request({ url: `/sales_orders/options/`, method: 'get', params })
}
// ロット
export function batchsOption(params) {
  return request({ url: `/batchs/options/`, method: 'get', params })
}
// 仕入先
export function supplierArrearsOption(params) {
  return request({ url: `/supplier_arrears/options/`, method: 'get', params })
}
// 顧客
export function clientArrearsOption(params) {
  return request({ url: `/client_arrears/options/`, method: 'get', params })
}
// 決済項目
export function chargeItemsOption(params) {
  return request({ url: `/charge_items/options/`, method: 'get', params })
}
// // 営業マネージャー
// export function managerOption(params) {
//   return request({ url: `/users/options/`, method: 'get', params })
// }
// // 契約
// export function contractOption(params) {
//   return request({ url: `/contract_orders/options/`, method: 'get', params })
// }

// // 契約原料
// export function contractMaterialsOption(params) {
//   return request({ url: `/contract_materials/options/`, method: 'get', params })
// }

// // 購買伝票原料
// export function purchaseMaterialsOption(params) {
//   return request({ url: `/purchase_materials/options/`, method: 'get', params })
// }

// // 梱包明細書
// export function packingOrdersOption(params) {
//   return request({ url: `/packing_orders/options/`, method: 'get', params })
// }

// // 梱包明細書原料
// export function packingMaterialsOption(params) {
//   return request({ url: `/packing_materials/options/`, method: 'get', params })
// }
