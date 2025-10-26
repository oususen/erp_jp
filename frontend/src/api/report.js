import request from '@/utils/request';

// 販売レポート
export function salesReportStatistics(params) {
  return request({ url: `/sales_reports/statistics/`, method: 'get', params })
}
// 販売レポート明細
export function salesReportDetialsList(params) {
  return request({ url: `/sales_reports/detials/`, method: 'get', params })
}
// 商品ごとの販売レポートの概要
export function salesReportByGoodsList(params) {
  return request({ url: `/sales_reports/group_by_goods/`, method: 'get', params })
}

// 購買レポート
export function purchaseReportStatistics(params) {
  return request({ url: `/purchase_reports/statistics/`, method: 'get', params })
}
// 購買レポート明細
export function purchaseReportDetialsList(params) {
  return request({ url: `/purchase_reports/detials/`, method: 'get', params })
}
// 商品ごとにまとめた購買レポート
export function purchaseReportByGoodsList(params) {
  return request({ url: `/purchase_reports/group_by_goods/`, method: 'get', params })
}

// 在庫レポート
export function inventoryReportList(params) {
  return request({ url: `/inventories/`, method: 'get', params })
}

// 収支データデータ統計
export function financialStatistics(params) {
  return request({ url: `/finance_statistics/`, method: 'get', params })
}

// 注文の支払いいい詳細
export function salesPaymentRecord(params) {
  return request({ url: `/sales_collection_detials/`, method: 'get', params })
}

// 販売返金明細
export function salesReturnPaymentRecord(params) {
  return request({ url: `/sales_return_payment_detials/`, method: 'get', params })
}

// 購買支出明細
export function purchasePaymentRecord(params) {
  return request({ url: `/purchase_payment_detials/`, method: 'get', params })
}

// 購買返金明細
export function purchaseReturnPaymentRecord(params) {
  return request({ url: `/purchase_return_collection_detials/`, method: 'get', params })
}

// ロットレポート
export function batchsReportList(params) {
  return request({ url: `/batchs/`, method: 'get', params })
}
