"""
フロントエンド (Vue.js) の中国語を日本語に一括変換するスクリプト
"""
import os
import re

# 中国語→日本語の翻訳マッピング（拡張版）
TRANSLATION_MAP = {
    # 基本操作
    '添加': '追加',
    '删除': '削除',
    '编辑': '編集',
    '修改': '変更',
    '保存': '保存',
    '取消': 'キャンセル',
    '确定': '確定',
    '提交': '送信',
    '搜索': '検索',
    '查询': '照会',
    '导出': 'エクスポート',
    '导入': 'インポート',
    '打印': '印刷',
    '下载': 'ダウンロード',
    '新增': '新規追加',
    '关闭': '閉じる',
    '返回': '戻る',
    '刷新': '更新',
    '重置': 'リセット',
    '清空': 'クリア',
    '选择': '選択',
    '上传': 'アップロード',

    # モジュール名
    '数据看板': 'データダッシュボード',
    '基础数据': '基礎データ',
    '产品管理': '製品管理',
    '采购管理': '購買管理',
    '销售管理': '販売管理',
    '库存管理': '在庫管理',
    '财务管理': '財務管理',
    '系统管理': 'システム管理',
    '报表统计': 'レポート統計',

    # レポート
    '销售报表': '販売レポート',
    '采购报表': '購買レポート',
    '库存报表': '在庫レポート',
    '收支统计': '収支統計',
    '批次报表': 'バッチレポート',

    # データ項目
    '客户管理': '顧客管理',
    '供应商管理': 'サプライヤー管理',
    '仓库管理': '倉庫管理',
    '结算账户': '決済アカウント',
    '收支项目': '収支項目',
    '角色管理': 'ロール管理',
    '员工账号': '従業員アカウント',
    '系统配置': 'システム設定',

    # 製品関連
    '产品分类': '製品分類',
    '产品单位': '製品単位',
    '产品信息': '製品情報',
    '临期预警': '期限切れ警告',
    '产品图片': '製品画像',
    '产品': '製品',
    '商品': '商品',
    '批次': 'バッチ',
    '库存': '在庫',
    '新增产品': '製品追加',

    # 購買関連
    '采购开单': '購買伝票作成',
    '采购记录': '購買履歴',
    '采购退货': '購買返品',
    '退货记录': '返品履歴',
    '采购商品': '購買商品',
    '采购订单': '購買注文',
    '采购退货商品': '購買返品商品',
    '采购退货订单': '購買返品注文',

    # 販売関連
    '销售开单': '販売伝票作成',
    '销售记录': '販売履歴',
    '销售退货': '販売返品',
    '退货记录': '返品履歴',
    '销售商品': '販売商品',
    '销售订单': '販売注文',
    '销售退货商品': '販売返品商品',
    '销售退货订单': '販売返品注文',

    # 在庫関連
    '入库任务': '入庫タスク',
    '出库任务': '出庫タスク',
    '盘点': '棚卸',
    '调拨': '振替',
    '库存流水': '在庫履歴',
    '入库商品': '入庫商品',
    '入库订单': '入庫注文',
    '入库记录商品': '入庫記録商品',
    '入库记录': '入庫記録',
    '出库商品': '出庫商品',
    '出库订单': '出庫注文',
    '出库记录商品': '出庫記録商品',
    '出库记录': '出庫記録',

    # 財務関連
    '应付欠款': '買掛金',
    '付款': '支払い',
    '应收欠款': '売掛金',
    '收款': '入金',
    '账户转账': '口座振替',
    '日常收支': '日常収支',
    '资金流水': '資金履歴',

    # フィールド名
    '编号': '番号',
    '名称': '名称',
    '代码': 'コード',
    '数量': '数量',
    '单价': '単価',
    '金额': '金額',
    '备注': '備考',
    '状态': 'ステータス',
    '日期': '日付',
    '时间': '時間',
    '创建人': '作成者',
    '创建时间': '作成日時',
    '更新时间': '更新日時',
    '序号': '番号',
    '操作': '操作',

    # ステータス
    '待审核': '承認待ち',
    '已审核': '承認済み',
    '已完成': '完了',
    '已取消': 'キャンセル済み',
    '进行中': '進行中',
    '计划中': '計画中',
    '强制关闭': '強制終了',
    '激活': '有効',
    '冻结': '無効',

    # メッセージ
    '操作成功': '操作成功',
    '操作失败': '操作失敗',
    '请输入': '入力してください',
    '请选择': '選択してください',
    '必填项': '必須項目',
    '登录': 'ログイン',
    '退出': 'ログアウト',
    '账号': 'アカウント',
    '密码': 'パスワード',
    '确定删除吗': '削除してもよろしいですか',
    '模板下载': 'テンプレートダウンロード',
    '正在导入中, 请等待': 'インポート中です。お待ちください',

    # その他
    '权限组': '権限グループ',
    '权限': '権限',
    '角色': 'ロール',
    '团队': 'チーム',
    '用户': 'ユーザー',

    # プレースホルダー用（カンマ区切り）
    '编号, 名称, 备注': '番号、名称、備考',
    '请等待': 'お待ちください',
    '正在导入中': 'インポート中です',
}

def translate_file(file_path, dry_run=False):
    """ファイル内の中国語を日本語に変換"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = []

        # 各翻訳を適用
        for chinese, japanese in TRANSLATION_MAP.items():
            # エスケープ処理
            escaped_chinese = re.escape(chinese)

            # パターン1: title="中国語", placeholder="中国語" などの属性
            pattern1 = f'((?:title|placeholder|label)\\s*=\\s*")({escaped_chinese})(")'
            matches = re.finditer(pattern1, content)
            if any(matches):
                content = re.sub(pattern1, f'\\1{japanese}\\3', content)
                changes_made.append(f"  属性: {chinese} → {japanese}")

            # パターン2: >中国語< のようなテキストノード
            pattern2 = f'(>)({escaped_chinese})(<)'
            matches = re.finditer(pattern2, content)
            if any(matches):
                content = re.sub(pattern2, f'\\1{japanese}\\3', content)
                changes_made.append(f"  テキスト: {chinese} → {japanese}")

            # パターン3: '中国語' や "中国語" のような文字列リテラル
            pattern3 = f"(['\"])({escaped_chinese})\\1"
            matches = re.finditer(pattern3, content)
            if any(matches):
                content = re.sub(pattern3, f'\\1{japanese}\\1', content)
                changes_made.append(f"  文字列: {chinese} → {japanese}")

            # パターン4: name: '中国語' のようなオブジェクトプロパティ
            pattern4 = f"(name\\s*:\\s*')({escaped_chinese})(')"
            matches = re.finditer(pattern4, content)
            if any(matches):
                content = re.sub(pattern4, f'\\1{japanese}\\3', content)
                changes_made.append(f"  プロパティ: {chinese} → {japanese}")

            # パターン5: {{中国語}} のような補間
            pattern5 = f'(\\{{\\{{\\s*(?:value|item)?\\s*\\?\\s*")({escaped_chinese})(")'
            matches = re.finditer(pattern5, content)
            if any(matches):
                content = re.sub(pattern5, f'\\1{japanese}\\3', content)
                changes_made.append(f"  補間: {chinese} → {japanese}")

        if content != original_content and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        elif content != original_content:
            return True, changes_made

    except Exception as e:
        print(f"エラー: {file_path} - {e}")

    return False, []

def main(dry_run=True):
    """全ての Vue/JS ファイルを処理"""
    frontend_dir = r"D:\erp-main-updated\frontend\src"
    modified_count = 0

    print("="*80)
    if dry_run:
        print("[DRY RUN] Preview - No actual changes will be made")
    else:
        print("[EXECUTE] Translating files...")
    print("="*80)
    print()

    for root, dirs, files in os.walk(frontend_dir):
        # node_modules フォルダはスキップ
        if 'node_modules' in dirs:
            dirs.remove('node_modules')

        for file in files:
            if file.endswith(('.vue', '.js')):
                file_path = os.path.join(root, file)
                modified, changes = translate_file(file_path, dry_run)

                if modified and changes:
                    rel_path = os.path.relpath(file_path, frontend_dir)
                    try:
                        print(f"[OK] {rel_path} - {len(changes)} changes")
                    except UnicodeEncodeError:
                        print(f"[OK] {rel_path} - {len(changes)} changes")
                    modified_count += 1

    print("="*80)
    try:
        print(f"Complete! {modified_count} files will be modified.")
        if dry_run:
            print()
            print("To actually execute the translation:")
            print("  python translate_frontend_to_japanese.py --execute")
    except UnicodeEncodeError:
        print(f"Complete! {modified_count} files will be modified.")
    print("="*80)

if __name__ == '__main__':
    import sys

    # --execute オプションがある場合のみ実行
    dry_run = '--execute' not in sys.argv

    main(dry_run=dry_run)
