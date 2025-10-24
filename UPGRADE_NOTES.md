# ERP システム - Python 3.13.5 & Django 5.1 アップグレード版

このフォルダは元の `erp-main` を Python 3.13.5 と Django 5.1 に対応させたバージョンです。

## 主な変更点

### バージョンアップグレード

| パッケージ | 旧バージョン | 新バージョン |
|----------|------------|------------|
| Python | 3.9+ | **3.13.5** |
| Django | 3.2 | **5.1 LTS** |
| djangorestframework | 3.12.4 | **3.15.2** |
| mysqlclient | 2.2.0 | **2.2.6** |
| Pillow | 8.4.0 | **11.0.0** |
| pendulum | 2.1.2 | **3.0.0** |

### Django 設定の変更

**settings.py の変更:**
- `USE_L10N = True` → コメントアウト（Django 5.0で削除済み）
- Django 5.1では `USE_I18N = True` の場合、自動的にローカライゼーションが有効化されます

## セットアップ手順

### 1. 仮想環境の作成

```powershell
# erp-main-updated/django フォルダに移動
cd D:\erp-main-updated\django

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化（PowerShell）
.\venv\Scripts\Activate.ps1

# 仮想環境を有効化（Command Prompt）
venv\Scripts\activate.bat
```

### 2. 依存関係のインストール

```powershell
# 仮想環境が有効化された状態で実行
pip install -r requirements.txt
```

### 3. データベース設定

元のアプリと同じMySQLデータベースを使用できます：

**configs/django.py** の設定を確認：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'erp_user',
        'PASSWORD': 'daisofutu1470-3',
        'NAME': 'erp_db',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

### 4. データベースマイグレーション

```powershell
# マイグレーションファイルの作成
python manage.py makemigrations

# データベースに適用
python manage.py migrate
```

### 5. サーバー起動

```powershell
# 開発サーバーを起動
python manage.py runserver

# ブラウザで http://127.0.0.1:8000 にアクセス
```

## フロントエンド（Vue.js）

フロントエンドは変更していません。元のまま使用できます：

```powershell
cd D:\erp-main-updated\frontend

# 依存関係のインストール（初回のみ）
npm install

# 開発サーバー起動
npm run serve
```

## トラブルシューティング

### mysqlclient のインストールエラー

Windows環境で `mysqlclient` のインストールに失敗する場合：

1. MySQL Connector/C をインストール
2. または `pymysql` を代替として使用：
   ```python
   # settings.py の先頭に追加
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

### Pillow のインストールエラー

```powershell
# 最新版をインストール
pip install --upgrade Pillow
```

## 元のアプリとの互換性

- **データベース**: 同じデータベースを共有可能
- **API**: REST API エンドポイントは互換性あり
- **フロントエンド**: 変更なし、そのまま使用可能

## 注意事項

1. **元のアプリ（D:\erp-main）は保存されています**
2. このフォルダは独立して動作します
3. データベースを共有する場合は、同時に両方のサーバーを起動しないでください

## 更新日

2025-10-25

## 参考リンク

- [Django 5.1 リリースノート](https://docs.djangoproject.com/en/5.1/releases/5.1/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [元のREADME](../erp-main/README.md)
