# ERP システム - セットアップスクリプト (PowerShell)
# Python 3.13.5 & Django 5.1 対応版

Write-Host "========================================" -ForegroundColor Green
Write-Host "ERP システム セットアップ開始" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Python バージョン確認
Write-Host "Python バージョン確認中..." -ForegroundColor Cyan
python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "エラー: Python が見つかりません" -ForegroundColor Red
    exit 1
}

# 仮想環境の作成
Write-Host ""
Write-Host "仮想環境を作成中..." -ForegroundColor Cyan

if (Test-Path "venv") {
    Write-Host "仮想環境は既に存在します (venv)" -ForegroundColor Yellow
    $response = Read-Host "削除して再作成しますか？ (y/n)"
    if ($response -eq "y") {
        Remove-Item -Path "venv" -Recurse -Force
        python -m venv venv
        Write-Host "仮想環境を再作成しました" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "仮想環境を作成しました (venv)" -ForegroundColor Green
}

# 仮想環境の有効化
Write-Host ""
Write-Host "仮想環境を有効化中..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "エラー: 仮想環境の有効化に失敗しました" -ForegroundColor Red
    Write-Host "PowerShell の実行ポリシーを確認してください:" -ForegroundColor Yellow
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# 依存関係のインストール
Write-Host ""
Write-Host "依存関係をインストール中..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "エラー: 依存関係のインストールに失敗しました" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "セットアップ完了！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Cyan
Write-Host "1. データベース設定を確認: configs/django.py" -ForegroundColor White
Write-Host "2. マイグレーション実行: python manage.py migrate" -ForegroundColor White
Write-Host "3. サーバー起動: python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "詳細は UPGRADE_NOTES.md を参照してください" -ForegroundColor Yellow
