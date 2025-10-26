export let permissions = {
  'role': 'ロール管理',
  'account': 'アカウント管理',
  'warehouse': '入庫管理',
  'stock_location': 'ロケーション管理',
  'client': '接点単位',
  'unit': '単位管理',
  'material': '商品管理',
  'material_batch': '商品ロット',
  'stock_in': '入庫',
  'stock_out': '入庫から出た',
  'stock_check': '棚卸',
  'stock_transfer': '在庫振替',
  'config': '機能設定',
  'order_prefix': '伝票ヘッダー',
  'inventory': '在庫情報',
  'flow': '入出庫履歴',
  'stock_check':'棚卸業務'
}

export let permissionsTree = [
  {
    title: 'システム管理',
    value: '0',
    key: '0',
    children: [
      {
        title: 'ロール管理',
        value: 'role',
        key: 'role',
      },
      {
        title: 'アカウント管理',
        value: 'account',
        key: 'account',
      },
      {
        title: '機能設定',
        value: 'config',
        key: 'config',
      },
      {
        title: '伝票ヘッダー',
        value: 'order_prefix',
        key: 'order_prefix',
      },
    ],
  },
  {
    title: 'マスターデータ管理',
    value: '1',
    key: '1',
    children: [
      {
        title: '入庫管理',
        value: 'warehouse',
        key: 'warehouse',
      },
      {
        title: 'ロケーション管理',
        value: 'stock_location',
        key: 'stock_location',
      },
      {
        title: '接点単位',
        value: 'client',
        key: 'client',
      },
      {
        title: '単位管理',
        value: 'unit',
        key: 'unit',
      },
      {
        title: '商品管理',
        value: 'material',
        key: 'material',
      },
      {
        title: '商品ロット',
        value: 'material_batch',
        key: 'material_batch',
      },
    ],
  },
  {
    title: '入出庫作業',
    value: '2',
    key: '2',
    children: [
      {
        title: '入庫から出た',
        value: 'stock_out',
        key: 'stock_out',
      },
      {
        title: '入庫',
        value: 'stock_in',
        key: 'stock_in',
      },
    ],
  },
  {
    title: 'そのその他宿題',
    value: '3',
    key: '3',
    children: [
      {
        title: '棚卸',
        value: 'stock_check',
        key: 'stock_check',
      },
      {
        title: '在庫振替',
        value: 'stock_transfer',
        key: 'stock_transfer',
      },
    ],
  },
  {
    title: 'レポート',
    value: '4',
    key: '4',
    children: [
      {
        title: '在庫情報',
        value: 'inventory',
        key: 'inventory',
      },
      {
        title: '入出庫履歴',
        value: 'flow',
        key: 'flow',
      },
    ],
  },
]


export let permission_groups = [
  {
      "id": 1,
      "name": "データダッシュボード",
      "permission_items": [
          {
              "id": 1,
              "name": "販売動向",
              "code": "sales_trend"
          },
          {
              "id": 2,
              "name": "売上上位10商品",
              "code": "sales_hot_goods"
          },
          {
              "id": 3,
              "name": "注文の支払いいい詳細",
              "code": "stock_in_reminder"
          }
      ]
  },
  {
      "id": 2,
      "name": "レポートデータデータ統計",
      "permission_items": [
          {
              "id": 6,
              "name": "販売レポート",
              "code": "sales_report"
          },
          {
              "id": 7,
              "name": "購買レポート",
              "code": "purchase_report"
          },
          {
              "id": 8,
              "name": "在庫レポート",
              "code": "inventory"
          },

          {
              "id": 10,
              "name": "収支データデータ統計",
              "code": "finance_statistic"
          }
      ]
  },
  {
      "id": 3,
      "name": "基本ファイル",
      "permission_items": [
          {
              "id": 11,
              "name": "顧客管理",
              "code": "client"
          },
          {
              "id": 12,
              "name": "仕入先管理",
              "code": "supplier"
          },
          {
              "id": 13,
              "name": "入庫管理",
              "code": "warehouse"
          },
          {
              "id": 14,
              "name": "決済口座",
              "code": "account"
          },
          {
              "id": 15,
              "name": "決済口座",
              "code": "charge_item"
          }
      ]
  },
  
  {
      "id": 5,
      "name": "購買管理",
      "permission_items": [
          {
              "id": 19,
              "name": "購買伝票",
              "code": "purchase_order"
          },
          {
              "id": 20,
              "name": "購買返品",
              "code": "purchase_return_order"
          }
      ]
  },
  {
      "id": 6,
      "name": "販売管理",
      "permission_items": [
          {
              "id": 21,
              "name": "販売注文",
              "code": "sales_order"
          },
          {
              "id": 22,
              "name": "販売返品",
              "code": "sales_return_order"
          }
      ]
  },

  {
      "id": 8,
      "name": "在庫管理",
      "permission_items": [
          {
              "id": 25,
              "name": "入庫業",
              "code": "stock_in"
          },
          {
              "id": 26,
              "name": "出庫業務",
              "code": "stock_out"
          },
          {
              "id": 27,
              "name": "棚卸業務",
              "code": "stock_check"
          },
          {
              "id": 28,
              "name": "在庫振替業務",
              "code": "stock_transfer"
          },
          {
            "id": 29,
            "name": "在庫残高",
            "code": "inventory_flow"
        },
      ] 
  },
  {
      "id": 9,
      "name": "取引管理",
      "permission_items": [
          {
              "id": 30,
              "name": "買掛金",
              "code": "supplier_arrears"
          },
          {
              "id": 31,
              "name": "支払い業務",
              "code": "payment_order"
          },
          {
              "id": 32,
              "name": "売掛金",
              "code": "client_arrears"
          },
          {
              "id": 33,
              "name": "入金業務",
              "code": "collection_order"
          },

          {
              "id": 36,
              "name": "資金明細",
              "code": "finance_flow"
          }
      ]
  }
]