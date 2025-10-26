# 中国語→日本語 翻訳用語辞書

このドキュメントは、ERPシステムの翻訳で使用した用語のマッピング一覧です。

## 📦 商品・在庫関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 产品 | 商品 | Product/Goods | models, serializers, views全般 |
| 产品编号 | 商品コード | Product Number | label |
| 产品名称 | 商品名 | Product Name | label |
| 产品条码 | 商品バーコード | Product Barcode | label |
| 产品规格 | 商品規格 | Product Spec | label |
| 产品分类 | 商品カテゴリー | Product Category | label, filters |
| 产品单位 | 商品単位 | Product Unit | label |
| 产品信息 | 商品情報 | Product Info | permissions |
| 库存 | 在庫 | Inventory | models, views全般 |
| 库存数量 | 在庫数量 | Inventory Quantity | label |
| 库存不足 | 在庫が不足しています | Out of Stock | error messages |
| 批次 | ロット | Batch | models全般 |
| 批次控制 | ロット制御 | Batch Control | models |
| 批次编号 | ロット番号 | Batch Number | serializers |

## 🏢 施設・場所関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 仓库 | 倉庫 | Warehouse | models全般 |
| 仓库编号 | 倉庫コード | Warehouse Number | label |
| 仓库名称 | 倉庫名 | Warehouse Name | label |
| 仓库管理 | 倉庫管理 | Warehouse Management | permissions |
| 出库仓库 | 出庫倉庫 | Out Warehouse | stock_transfer |
| 入库仓库 | 入庫倉庫 | In Warehouse | stock_transfer |

## 👥 取引先関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 客户 | 顧客 | Client/Customer | models全般 |
| 客户编号 | 顧客コード | Client Number | label |
| 客户名称 | 顧客名 | Client Name | label |
| 客户管理 | 顧客管理 | Client Management | permissions |
| 供应商 | 仕入先 | Supplier | models全般 |
| 供应商编号 | 仕入先コード | Supplier Number | label |
| 供应商名称 | 仕入先名 | Supplier Name | label |
| 供应商管理 | 仕入先管理 | Supplier Management | permissions |

## 📋 業務・伝票関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 采购 | 購買 | Purchase | models全般 |
| 采购管理 | 購買管理 | Purchase Management | permissions |
| 采购开单 | 購買発行 | Purchase Issue | permissions |
| 采购单据 | 購買伝票 | Purchase Order | models |
| 采购单号 | 購買伝票番号 | Purchase Order Number | label |
| 采购退货 | 購買返品 | Purchase Return | models |
| 采购价 | 購買価格 | Purchase Price | label |
| 采购数量 | 購買数量 | Purchase Quantity | label |
| 采购金额 | 購買金額 | Purchase Amount | label |
| 采购报表 | 購買レポート | Purchase Report | schemas |
| 销售 | 販売 | Sales | models全般 |
| 销售管理 | 販売管理 | Sales Management | permissions |
| 销售开单 | 販売発行 | Sales Issue | permissions |
| 销售单据 | 販売伝票 | Sales Order | models |
| 销售单号 | 販売伝票番号 | Sales Order Number | label |
| 销售退货 | 販売返品 | Sales Return | models |
| 销售价 | 販売単価 | Sales Price | label |
| 销售数量 | 販売数量 | Sales Quantity | label |
| 销售金额 | 販売金額 | Sales Amount | label |
| 销售报表 | 販売レポート | Sales Report | schemas |
| 单据 | 伝票 | Document/Slip | models全般 |

## 📦 入出庫関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 入库 | 入庫 | Stock In | models全般 |
| 入库类型 | 入庫タイプ | Stock In Type | models |
| 入库产品 | 入庫商品 | Stock In Product | serializers |
| 入库数量 | 入庫数量 | Stock In Quantity | label |
| 入库通知单据 | 入庫通知伝票 | Stock In Notice | models |
| 入库任务提醒 | 入庫タスク通知 | Stock In Task Reminder | message |
| 出库 | 出庫 | Stock Out | models全般 |
| 出库类型 | 出庫タイプ | Stock Out Type | models |
| 出库产品 | 出庫商品 | Stock Out Product | serializers |
| 出库数量 | 出庫数量 | Stock Out Quantity | label |
| 出库通知单据 | 出庫通知伝票 | Stock Out Notice | models |
| 出库任务提醒 | 出庫タスク通知 | Stock Out Task Reminder | message |
| 盘点 | 棚卸 | Stock Check | models全般 |
| 盘点状态 | 棚卸ステータス | Stock Check Status | label |
| 盘点数量 | 棚卸数量 | Check Quantity | serializers |
| 盘点批次 | 棚卸ロット | Check Batch | label |
| 盘点产品 | 棚卸商品 | Check Product | label |
| 盘点单据 | 棚卸伝票 | Check Order | models |
| 调拨 | 在庫振替 | Stock Transfer | models全般 |
| 调拨数量 | 振替数量 | Transfer Quantity | models |
| 调拨单据 | 在庫振替伝票 | Transfer Order | views |

## 💰 財務関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 账户 | 口座 | Account | models全般 |
| 账户编号 | 口座コード | Account Number | label |
| 账户名称 | 口座名 | Account Name | label |
| 账户转账 | 口座振替 | Account Transfer | permissions |
| 结算账户 | 決済アカウント | Settlement Account | finance |
| 转出账户 | 振替元口座 | Out Account | finance models |
| 转入账户 | 振替先口座 | In Account | finance models |
| 付款 | 支払 | Payment | models全般 |
| 付款单据 | 支払伝票 | Payment Order | models |
| 付款账户 | 支払口座 | Payment Account | models |
| 付款金额 | 支払金額 | Payment Amount | label |
| 收款 | 入金 | Collection | models全般 |
| 收款单据 | 入金伝票 | Collection Order | models |
| 收款账户 | 入金口座 | Collection Account | models |
| 收款金额 | 入金金額 | Collection Amount | label |
| 收支 | 収支 | Income/Expense | finance |
| 收支单据 | 収支伝票 | Charge Order | finance |
| 收支项目 | 収支項目 | Charge Item | finance |
| 金额 | 金額 | Amount | label全般 |
| 总金额 | 総金額 | Total Amount | models |
| 余额 | 残高 | Balance | finance |
| 余额不足 | 残高が不足しています | Insufficient Balance | error messages |

## 🏭 生産関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 生产 | 生産 | Production | models全般 |
| 工单 | 作業指示書 | Production Order | models, views |
| 生产数量 | 生産数量 | Production Quantity | serializers |
| 已生产数量 | 生産済数量 | Produced Quantity | models |
| 生产总数 | 生産総数 | Total Production | models |

## 📊 レポート・統計関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 报表统计 | レポートデータ統計 | Report Statistics | - |
| 销售走势 | 販売推移 | Sales Trend | permissions |
| 销售前十产品 | 販売トップ10商品 | Top 10 Sales Products | permissions |
| 批次报表 | ロットレポート | Batch Report | permissions |
| 流水类型 | フロータイプ | Flow Type | flow models |

## 👤 ユーザー・権限関連

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 用户 | ユーザー | User | system models |
| 用户数量 | ユーザー数 | User Quantity | schemas |
| 经手人 | 担当者 | Handler | models全般 |
| 经手人名称 | 担当者名 | Handler Name | label |
| 创建人 | 作成者 | Creator | models全般 |
| 创建人名称 | 作成者名 | Creator Name | label |
| 管理者 | 管理者 | Manager | data models |
| 公司编号 | チームコード | Team Number | manage |

## ⚙️ システム・共通用語

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 编号 | 番号/コード | Number/Code | models全般 |
| 名称 | 名称 | Name | models全般 |
| 数量 | 数量 | Quantity | models全般 |
| 获取编号 | 番号取得 | Get Number | views docstring |
| 已作废 | 廃棄済み | Voided | models, errors |
| 作废 | 廃棄 | Void | TextChoices |
| 已完成 | 完了済み | Completed | models, errors |
| 完成状态 | 完了状態 | Completion Status | models |
| 未激活 | 有効化されていません | Not Active | error messages |
| 激活状态 | 有効状態 | Active Status | models |
| 不存在 | が存在しません | Does Not Exist | error messages |
| 已存在 | は既に存在します | Already Exists | error messages |
| 错误 | エラー/間違っています | Error | error messages |
| 为空 | が空です | Is Empty | error messages |
| 不足 | が不足しています | Insufficient | error messages |
| 重复 | が重複しています | Duplicate | error messages |
| 小于或等于零 | ゼロ以下です | Less Than or Equal to Zero | error messages |
| 小于零 | ゼロ未満です | Less Than Zero | error messages |
| 同步 | 同期 | Sync | comments |
| 默认 | デフォルト | Default | test data |

## 📝 その他

| 中国語 | 日本語 | 英語 | 使用箇所 |
|--------|--------|------|---------|
| 备注 | 備考 | Remark | models全般 |
| 手机号 | 携帯番号 | Mobile Number | system models |
| 邮箱 | メールアドレス | Email | system models |
| 地址 | 住所 | Address | models |
| 电话 | 電話 | Phone | models |
| 联系人 | 連絡先 | Contact | models |
| 期限 | 有効期限 | Expiry | permissions |
| 到期 | 期限切れ | Expired | error messages |

---

## 使用上の注意

### 翻訳の一貫性
- 同じ中国語は常に同じ日本語に翻訳
- frontend_translation_cache.json と整合性を保つ

### 文脈による使い分け
- **编号**: フィールド名では「番号」、画面表示では「コード」
- **名称**: 基本的にそのまま「名称」（日本語でも通用）
- **数量**: そのまま「数量」（日本語）

### エラーメッセージパターン
```
中国語: [名称]不存在
日本語: [名称]が存在しません

中国語: [名称]已存在
日本語: [名称]は既に存在します

中国語: [名称]未激活
日本語: [名称]は有効化されていません

中国語: [数値]小于或等于零
日本語: [数値]がゼロ以下です
```

---

**総用語数**: 約150語  
**参照元**: frontend_translation_cache.json (924ペア)  
**更新日**: 2025年10月26日
