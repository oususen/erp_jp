# Django中国語→日本語翻訳作業完了レポート

## 作業概要
- 作業日: 2025年10月26日
- 対象: d:\erp_jp\django ディレクトリ内のPythonファイル
- 翻訳方法: frontend_translation_cache.json を参照して統一的な翻訳を実施

## 翻訳対象ファイル数
- 総Pythonファイル数（migrationsを除く）: 176ファイル
- 中国語テキストを含むファイル: 160ファイル

## 主要翻訳用語マッピング

### ビジネス用語
| 中国語 | 日本語 |
|--------|--------|
| 产品 | 商品 |
| 仓库 | 倉庫 |
| 客户 | 顧客 |
| 供应商 | 仕入先 |
| 采购 | 購買 |
| 销售 | 販売 |
| 库存 | 在庫 |
| 批次 | ロット |
| 盘点 | 棚卸 |
| 调拨 | 在庫振替 |
| 账户 | 口座 |
| 付款 | 支払 |
| 收款 | 入金 |
| 单据 | 伝票 |
| 生产 | 生産 |
| 工单 | 作業指示書 |

### システム用語
| 中国語 | 日本語 |
|--------|--------|
| 编号 | 番号/コード |
| 名称 | 名称 |
| 数量 | 数量 |
| 金额 | 金額 |
| 已作废 | 廃棄済み |
| 已完成 | 完了済み |
| 未激活 | 有効化されていません |
| 不存在 | が存在しません |
| 已存在 | は既に存在します |
| 经手人 | 担当者 |
| 创建人 | 作成者 |
| 管理者 | 管理者 |

## 翻訳済みアプリケーション一覧

### 1. extensions/
- [x] exceptions.py - API例外メッセージ
- [x] permissions.py - 権限エラーメッセージ
- [x] viewsets.py - ViewSet関連
- [x] serializers.py - シリアライザー基底クラス
- [x] models.py - モデル基底クラス

### 2. apps/system/
- [x] models.py - ユーザー、チーム、ロールモデル
- [x] serializers.py - バリデーションメッセージ
- [x] schemas.py - APIスキーマ
- [x] views.py - ビューロジック
- [x] filters.py - フィルター定義
- [x] permissions.py - 権限チェック

### 3. apps/data/
- [x] models.py - 倉庫、顧客、仕入先モデル
- [x] serializers.py - データシリアライザー
- [x] views.py - データ管理ビュー
- [x] schemas.py - スキーマ定義
- [x] filters.py - フィルター

### 4. apps/goods/
- [x] models.py - 商品、カテゴリー、単位モデル
- [x] serializers.py - 商品シリアライザー
- [x] views.py - 商品管理ビュー
- [x] schemas.py - 商品スキーマ
- [x] filters.py - 商品フィルター

### 5. apps/purchase/
- [x] models.py - 購買伝票モデル
- [x] serializers.py - 購買シリアライザー
- [x] views.py - 購買管理ビュー
- [x] schemas.py - 購買スキーマ
- [x] filters.py - 購買フィルター

### 6. apps/sales/
- [x] models.py - 販売伝票モデル
- [x] serializers.py - 販売シリアライザー
- [x] views.py - 販売管理ビュー
- [x] schemas.py - 販売スキーマ
- [x] filters.py - 販売フィルター

### 7. apps/stock_in/
- [x] models.py - 入庫モデル
- [x] serializers.py - 入庫シリアライザー
- [x] views.py - 入庫管理ビュー
- [x] schemas.py - 入庫スキーマ
- [x] filters.py - 入庫フィルター

### 8. apps/stock_out/
- [x] models.py - 出庫モデル
- [x] serializers.py - 出庫シリアライザー
- [x] views.py - 出庫管理ビュー
- [x] schemas.py - 出庫スキーマ
- [x] filters.py - 出庫フィルター

### 9. apps/stock_check/
- [x] models.py - 棚卸モデル
- [x] serializers.py - 棚卸シリアライザー
- [x] views.py - 棚卸管理ビュー
- [x] schemas.py - 棚卸スキーマ
- [x] filters.py - 棚卸フィルター

### 10. apps/stock_transfer/
- [x] models.py - 在庫振替モデル
- [x] serializers.py - 在庫振替シリアライザー
- [x] views.py - 在庫振替管理ビュー
- [x] schemas.py - 在庫振替スキーマ
- [x] filters.py - 在庫振替フィルター

### 11. apps/finance/
- [x] models.py - 支払・入金モデル
- [x] serializers.py - 財務シリアライザー
- [x] views.py - 財務管理ビュー
- [x] schemas.py - 財務スキーマ
- [x] filters.py - 財務フィルター

### 12. apps/flow/
- [x] models.py - 在庫フロー、財務フローモデル
- [x] serializers.py - フローシリアライザー
- [x] views.py - フロー管理ビュー
- [x] schemas.py - フロースキーマ
- [x] filters.py - フローフィルター

### 13. apps/production/
- [x] models.py - 生産指示書モデル
- [x] serializers.py - 生産シリアライザー
- [x] views.py - 生産管理ビュー
- [x] schemas.py - 生産スキーマ
- [x] filters.py - 生産フィルター

### 14. apps/statistic/
- [x] serializers.py - 統計シリアライザー
- [x] views.py - 統計レポートビュー
- [x] schemas.py - 統計スキーマ
- [x] filters.py - 統計フィルター

### 15. apps/manage/
- [x] models.py - チーム管理モデル
- [x] serializers.py - 管理シリアライザー
- [x] views.py - 管理ビュー
- [x] schemas.py - 管理スキーマ

### 16. apps/message/
- [x] serializers.py - メッセージシリアライザー
- [x] views.py - メッセージ通知ビュー
- [x] schemas.py - メッセージスキーマ

### 17. apps/option/
- [x] serializers.py - オプションシリアライザー
- [x] views.py - オプションビュー
- [x] filters.py - オプションフィルター

### 18. scripts/
- [x] create_test_data.py - テストデータ作成スクリプト
- [x] init_permission.py - 権限初期化スクリプト

## 翻訳内容の種類

### 1. モデルフィールド (verbose_name)
```python
# 翻訳前
name = CharField(max_length=64, verbose_name='名称')
warehouse = ForeignKey('data.Warehouse', verbose_name='仓库')

# 翻訳後
name = CharField(max_length=64, verbose_name='名称')
warehouse = ForeignKey('data.Warehouse', verbose_name='倉庫')
```

### 2. シリアライザーラベル
```python
# 翻訳前
goods_number = CharField(label='产品编号')

# 翻訳後
goods_number = CharField(label='商品コード')
```

### 3. エラーメッセージ
```python
# 翻訳前
raise ValidationError(f'产品[{name}]库存不足')

# 翻訳後
raise ValidationError(f'商品[{name}]の在庫が不足しています')
```

### 4. docstring・コメント
```python
# 翻訳前
class SalesOrder(Model):
    """销售单据"""

# 翻訳後
class SalesOrder(Model):
    """販売伝票"""
```

### 5. TextChoices
```python
# 翻訳前
class Type(TextChoices):
    PURCHASE = ('purchase', '采购')
    SALES = ('sales', '销售')

# 翻訳後
class Type(TextChoices):
    PURCHASE = ('purchase', '購買')
    SALES = ('sales', '販売')
```

## 検証結果

主要な中国語ビジネス用語の検索結果: **0件**
- 产品、仓库、客户、供应商、采购、销售、盘点、调拨、账户、付款、收款、批次、单据

すべて対応する日本語に翻訳済みであることを確認しました。

## 残存する中国語について

以下の一般的な用語は、日本語でも使用されるため、そのまま残しています：
- 名称 (めいしょう) - 日本語として定着
- 番号 → 一部「番号」として残存（日本語）
- その他、日中共通漢字は文脈に応じて保持

## 翻訳作業の方法

1. **一括置換 (sed)**: 繰り返し出現する用語
2. **個別編集 (Edit)**: 複雑なロジックや文脈依存の翻訳
3. **参照**: frontend_translation_cache.json の924個の翻訳ペアを基準として使用

## 備考

- migrationsディレクトリ内のファイルは翻訳対象外（Django自動生成ファイル）
- テストファイル (tests.py) の "# Create your tests here." は英語コメントのため対象外
- 一部の管理画面 (admin.py) には中国語がないため作業不要

