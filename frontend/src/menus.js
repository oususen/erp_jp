const menus = [
  {
    key: '1', name: 'レポートデータデータ統計', icon: 'line-chart', submenus: [
      { key: '/report/sale_report', name: '販売レポート' },
      { key: '/report/purchase_report', name: '購買レポート' },
      { key: '/report/stock_report', name: '在庫レポート' },
      { key: '/report/income_expense_statistics', name: '収支データデータ統計' },
      { key: '/report/batch_report', name: 'ロットレポート' },
    ]
  },
  {
    key: '2', name: '基本データ', icon: 'table', submenus: [
      { key: '/basicData/client', name: '顧客管理'},
      { key: '/basicData/supplier', name: '仕入先管理'},
      { key: '/basicData/warehouse', name: '入庫管理'},
      { key: '/basicData/settlement_account', name: '決済口座'},
      { key: '/basicData/revenue_expenditure_items', name: '収支項目'},
    ]
  },
  {
    key: '3', name: '商品管理', icon: 'appstore', submenus: [
      { key: '/goods/classification', name: '商品カテゴリ' },
      { key: '/goods/unit', name: '商品単位' },
      { key: '/goods/information', name: '商品情報' },
      { key: '/goods/temporary_warning', name: '期限切れ間近警告' },
    ]
  },
  {
    key: '4', name: '購買管理', icon: 'shopping-cart', submenus: [
      { key: '/purchasing/purchase_create', name: '購買伝票作成' },
      { key: '/purchasing/purchase_record', name: '購買記録' },
      { key: '/purchasing/purchase_return_create', name: '購買返品' },
      { key: '/purchasing/return_record', name: '返品記録' },
    ]
  },
  {
    key: '5', name: '販売管理', icon: 'shopping', submenus: [
      { key: '/sale/sale_create', name: '販売伝票作成' },
      { key: '/sale/sale_record', name: '販売記録' },
      { key: '/sale/sale_return_create', name: '販売返品' },
      { key: '/sale/sale_return_record', name: '返品記録' },
    ]
  },
  {
    key: '7', name: '在庫管理', icon: 'database', submenus: [
      { key: '/warehouse/inStock', name: '入庫タスク' },
      { key: '/warehouse/outStock', name: '出庫タスク' },
      { key: '/warehouse/inventory', name: '棚卸' },
      { key: '/warehouse/allocation', name: '在庫振替' },
      { key: '/warehouse/flow', name: '在庫推移' },
    ]
  },
  {
    key: '8', name: '財務管理', icon: 'dollar', submenus: [
      { key: '/finance/arrears_payable', name: '買掛金' },
      { key: '/finance/payment', name: '支払いい' },
      { key: '/finance/arrears_receivable', name: '売掛金' },
      { key: '/finance/collection', name: '入金' },
      { key: '/finance/account_transfer', name: '振出元口座' },
      { key: '/finance/income_and_pay', name: '日常収支' },
      { key: '/finance/flow', name: '資金明細' },
    ]
  },
  {
    key: '9', name: 'システム管理', icon: 'team', submenus: [
      { key: '/role', name: 'ロール管理' },
      { key: '/account', name: '従業員アカウント' },
      { key: '/config', name: 'システム設定' },
    ]
  },
]

// 上位メニュー「販売管理」「財務管理」を非表示
// さらに「レポート」「基本データ」内の販売・財務関連サブメニューも非表示
const filteredMenus = menus
  .filter(menu => menu.name !== '販売管理' && menu.name !== '財務管理')
  .map(menu => {
    if (menu.name === 'レポートデータデータ統計') {
      const blocked = new Set(['販売レポート', '収支データデータ統計']);
      return { ...menu, submenus: menu.submenus.filter(sm => !blocked.has(sm.name)) };
    }
    if (menu.name === '基本データ') {
      const blocked = new Set(['決済口座', '収支項目']);
      return { ...menu, submenus: menu.submenus.filter(sm => !blocked.has(sm.name)) };
    }
    return menu;
  });

export default filteredMenus;