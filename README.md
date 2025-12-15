# ERP 管理システム（Django + Vue2）

ERP のデモ実装です。バックエンドは Django/DRF、フロントエンドは Vue2（ant-design-vue）で、購買・生産・販売・在庫・帳票・権限管理などのモジュールを含みます。

## 必要環境
- Python 3.9 以上
- Node.js 12.x / npm 6.x（Vue CLI 4 系に合わせる）
- MySQL 8.0+
- Docker / Docker Compose（コンテナで動かす場合）

## クイックスタート（Docker）
```bash
docker-compose up --build -d
```
- ポート: nginx 8081、backend 8000、MySQL 3307→3306（ローカル）
- DB 初期化は `mysql/init.sql`、接続情報は `mysql/.env` で調整できます。
- フロントの API エンドポイントは nginx 経由で `/api/` を backend にプロキシする構成です。

## 手動セットアップ

### バックエンド（Django）
```bash
cd django
python -m venv venv
venv\Scripts\activate   # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
# DB 接続は django/configs/django.py を必要に応じて修正
python manage.py migrate
python manage.py createsuperuser   # 管理ユーザー作成
python manage.py runserver 0.0.0.0:8000
```

### フロントエンド（Vue2）
```bash
cd frontend
npm config set registry https://registry.npmmirror.com/   # 必要な場合
npm install
# API エンドポイントは src/utils/config.js の baseURL で設定（デフォルトは /api/）
npm run serve   # 開発
npm run build   # 本番ビルド
```
※ `npm run serve/build` は `NODE_OPTIONS=--openssl-legacy-provider` を自動付与しています（OpenSSL 互換対策）。

## ディレクトリ構成
- `frontend/` … Vue2 クライアント（ant-design-vue）
- `django/` … Django/DRF バックエンド
- `mysql/` … MySQL 初期化スクリプトと設定
- `nginx/` … nginx リバースプロキシ（フロント配信・API ルーティング）
- `img/` … 画面キャプチャ

## 運用メモ
- 本番運用では DEBUG を無効化し、uwsgi/nginx などの本番設定に切り替えてください。
- 権限や初期データが必要な場合は、Django 管理画面や独自スクリプトで投入してください。
