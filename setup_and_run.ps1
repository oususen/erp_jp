<# 
  初回セットアップ & 起動スクリプト
  - venv の有効化（存在すれば）
  - manage.py の自動検出（./django またはカレント直下。見つからなければ再帰検索）
  - migrate を実行
  - （任意）createsuperuser を実行（対話）
  - runserver を起動
#>

param(
  [string]$VenvPath = ".\venv",
  [switch]$CreateSuperuser,     # 付けると createsuperuser を実行
  [string]$Addr = "127.0.0.1:8000" # 変えたい場合は --Addr で指定
)

function Fail($msg) { Write-Host "ERROR: $msg" -ForegroundColor Red; exit 1 }

# --- venv をアクティブ化（任意） ---
if (Test-Path "$VenvPath\Scripts\Activate.ps1") {
  Write-Host "Activating venv: $VenvPath"
  . "$VenvPath\Scripts\Activate.ps1"
} else {
  Write-Host "venv が見つかりませんでした（$VenvPath）。グローバルの python を使用します。" -ForegroundColor Yellow
}

# --- manage.py の場所を特定 ---
$managePy = $null
if (Test-Path ".\django\manage.py") {
  $managePy = (Resolve-Path ".\django\manage.py").Path
} elseif (Test-Path ".\manage.py") {
  $managePy = (Resolve-Path ".\manage.py").Path
} else {
  Write-Host "manage.py を再帰検索中..."
  $found = Get-ChildItem -Recurse -Filter "manage.py" -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($found) { $managePy = $found.FullName }
}

if (-not $managePy) { Fail "manage.py が見つかりません。スクリプトをプロジェクトルートで実行しているか確認してください。" }

$manageDir = Split-Path $managePy -Parent
Write-Host "Using manage.py at: $managePy"
Push-Location $manageDir

# --- Python 実行確認 ---
try {
  $pyver = & python -c "import sys; print(sys.version)"
  Write-Host "Python: $pyver"
} catch {
  Pop-Location
  Fail "python コマンドが見つかりません。PATH か venv を確認してください。"
}

# --- Django チェック（任意） ---
Write-Host "Django 構成チェック中..."
& python manage.py check
if ($LASTEXITCODE -ne 0) {
  Pop-Location
  Fail "Django チェックに失敗しました。settings の誤り等を確認してください。"
}

# --- migrate ---
Write-Host "Applying migrations..."
& python manage.py migrate
if ($LASTEXITCODE -ne 0) {
  Pop-Location
  Fail "migrate に失敗しました。"
}

# --- createsuperuser（指定時のみ・対話） ---
if ($CreateSuperuser) {
  Write-Host "Creating superuser（対話形式）..."
  & python manage.py createsuperuser
  if ($LASTEXITCODE -ne 0) {
    Pop-Location
    Fail "createsuperuser に失敗しました。"
  }
}

# --- runserver ---
Write-Host "Starting development server at http://$Addr ..."
& python manage.py runserver $Addr

Pop-Location
