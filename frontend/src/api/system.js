import request from '@/utils/request';

// Permission
export function permissionList(params) {
  return request({ url: `/permission_groups/`, method: 'get', params })
}

// システム設定
export function configInfo(params) {
  return request({ url: `/system/configs/`, method: 'get', params })
}

// システム設定-更新
export function configUpdate(data) {
  return request({ url: `/system/set_configs/`, method: 'post', data })
}

// 在庫アラート
export function inventoryWarningsList(params) {
  return request({ url: `/inventory_warnings/`, method: 'get', params })
}

// 入庫作業リマインダー
export function stockInList(params) {
  return request({ url: `/stock_in_order_reminders/`, method: 'get', params })
}
// 出庫タスク通知
export function stockOutList(params) {
  return request({ url: `/stock_out_order_reminders/`, method: 'get', params })
}
// 売上上位10商品
export function salesTopTenList(params) {
  return request({ url: `/sales_hot_goods/`, method: 'get', params })
}
// 販売動向
export function salesTrendList(params) {
  return request({ url: `/sales_trends/`, method: 'get', params })
}
