"""
全ての Python ファイルで import pendulum を修正するスクリプト
"""
import os
import re

def fix_pendulum_import(file_path):
    """ファイル内の import pendulum を修正"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # パターン1: import pendulum（単独行）
        if re.search(r'^import pendulum\s*$', content, re.MULTILINE):
            new_content = re.sub(
                r'^import pendulum\s*$',
                'from extensions.common.base import pendulum',
                content,
                flags=re.MULTILINE
            )

            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
    except Exception as e:
        print(f"エラー: {file_path} - {e}")

    return False

def main():
    """全ての .py ファイルを処理"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fixed_count = 0

    print("pendulum のインポート文を修正中...")
    print(f"対象ディレクトリ: {base_dir}")
    print()

    for root, dirs, files in os.walk(base_dir):
        # venv フォルダはスキップ
        if 'venv' in dirs:
            dirs.remove('venv')

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_pendulum_import(file_path):
                    rel_path = os.path.relpath(file_path, base_dir)
                    print(f"✓ 修正: {rel_path}")
                    fixed_count += 1

    print()
    print(f"完了！ {fixed_count} ファイルを修正しました。")

if __name__ == '__main__':
    main()
