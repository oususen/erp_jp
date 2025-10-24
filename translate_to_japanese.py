"""
ERP システムの中国語を日本語に一括変換するスクリプト
"""
import os
import re

# 中国語→日本語の翻訳マッピング
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

    # データ項目
    '客户管理': '顧客管理',
    '供应商管理': 'サプライヤー管理',
    '仓库管理': '倉庫管理',
    '结算账户': '決済アカウント',
    '收支项目': '収支項目',

    # 製品関連
    '产品分类': '製品分類',
    '产品单位': '製品単位',
    '产品图片': '製品画像',
    '产品': '製品',
    '商品': '商品',
    '批次': 'バッチ',
    '库存': '在庫',

    # 購買関連
    '采购商品': '購買商品',
    '采购订单': '購買注文',
    '采购退货商品': '購買返品商品',
    '采购退货订单': '購買返品注文',

    # 販売関連
    '销售商品': '販売商品',
    '销售订单': '販売注文',
    '销售退货商品': '販売返品商品',
    '销售退货订单': '販売返品注文',

    # 在庫関連
    '入库商品': '入庫商品',
    '入库订单': '入庫注文',
    '入库记录商品': '入庫記録商品',
    '入库记录': '入庫記録',
    '出库商品': '出庫商品',
    '出库订单': '出庫注文',
    '出库记录商品': '出庫記録商品',
    '出库记录': '出庫記録',

    # システム関連
    '权限组': '権限グループ',
    '权限': '権限',
    '角色': 'ロール',
    '团队': 'チーム',
    '用户': 'ユーザー',

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

    # ステータス
    '待审核': '承認待ち',
    '已审核': '承認済み',
    '已完成': '完了',
    '已取消': 'キャンセル済み',
    '进行中': '進行中',
    '计划中': '計画中',
    '强制关闭': '強制終了',

    # メッセージ
    '操作成功': '操作成功',
    '操作失败': '操作失敗',
    '请输入': '入力してください',
    '请选择': '選択してください',
    '必填项': '必須項目',
    '登录': 'ログイン',
    '退出': 'ログアウ',
    '账号': 'アカウント',
    '密码': 'パスワード',

    # エラーメッセージ
    '未登陆验证': 'ログイン認証が必要です',
    '已到期': '期限切れです',
    '账号未激活': 'アカウントが有効化されていません',
    '无法执行任何操作': '操作を実行できません',
    '服务器错误': 'サーバーエラー',
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
            # 文字列リテラル内の中国語を検索して置換
            # verbose_name='中国語' のパターン
            pattern1 = f"(verbose_name\\s*=\\s*['\"]){re.escape(chinese)}(['\"])"
            if re.search(pattern1, content):
                content = re.sub(pattern1, f"\\1{japanese}\\2", content)
                changes_made.append(f"  {chinese} → {japanese}")

            # message='中国語' のパターン
            pattern2 = f"(message\\s*=\\s*['\"]){re.escape(chinese)}(['\"])"
            if re.search(pattern2, content):
                content = re.sub(pattern2, f"\\1{japanese}\\2", content)
                changes_made.append(f"  {chinese} → {japanese}")

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
    """全ての Python ファイルを処理"""
    django_dir = r"D:\erp-main-updated\django"
    modified_count = 0

    print("="*80)
    if dry_run:
        print("【ドライラン】変換プレビュー - 実際には変更しません")
    else:
        print("【本番実行】ファイルを変換します")
    print("="*80)
    print()

    for root, dirs, files in os.walk(django_dir):
        # venv フォルダはスキップ
        if 'venv' in dirs:
            dirs.remove('venv')

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                modified, changes = translate_file(file_path, dry_run)

                if modified and changes:
                    rel_path = os.path.relpath(file_path, django_dir)
                    print(f"✓ {rel_path}")
                    for change in changes[:5]:  # 最初の5つだけ表示
                        print(change)
                    if len(changes) > 5:
                        print(f"  ... 他 {len(changes) - 5} 件")
                    print()
                    modified_count += 1

    print("="*80)
    print(f"完了！ {modified_count} ファイルが対象です。")
    if dry_run:
        print()
        print("実際に変換するには:")
        print("  python translate_to_japanese.py --execute")
    print("="*80)

if __name__ == '__main__':
    import sys

    # --execute オプションがある場合のみ実行
    dry_run = '--execute' not in sys.argv

    main(dry_run=dry_run)
