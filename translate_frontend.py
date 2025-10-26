"""
Helper script to translate the Vue frontend from Chinese to Japanese.

Workflow:
1. Read the source (Chinese) code from the original repository.
2. Detect Chinese text segments and build a translation map.
3. Apply the translations and write the Japanese version into the current repo.

The script caches translations in JSON so repeated runs are quick.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Dict, Iterable

import requests

# Root directories
SOURCE_ROOT = Path(r"d:\erp_main_1\frontend\src")
TARGET_ROOT = Path(r"d:\erp_jp\frontend\src")
CACHE_PATH = Path(r"d:\erp_jp\frontend_translation_cache.json")

# Regex to capture contiguous Chinese text (including typical punctuation)
CJK_PATTERN = re.compile(
    r"[\u4e00-\u9fff][\u4e00-\u9fff\u3000-\u303f\uff00-\uffefA-Za-z0-9·•—（）()、，。！？：；“”‘’《》〈〉……· \t]*"
)

FILE_SUFFIXES = {
    ".vue",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
}

# Manual overrides for domain terms where machine translation is not ideal.
CUSTOM_TRANSLATIONS: Dict[str, str] = {
    "报表统计": "レポートデータ統計",
    "销售报表": "販売レポート",
    "采购报表": "購買レポート",
    "库存报表": "在庫レポート",
    "收支统计": "収支データ統計",
    "批次报表": "ロットレポート",
    "基础数据": "基本データ",
    "客户管理": "顧客管理",
    "供应商管理": "仕入先管理",
    "仓库管理": "入庫管理",
    "结算账户": "決済口座",
    "收支项目": "収支項目",
    "产品管理": "商品管理",
    "产品分类": "商品カテゴリ",
    "产品单位": "商品単位",
    "产品信息": "商品情報",
    "临期预警": "期限切れ間近警告",
    "采购管理": "購買管理",
    "采购开单": "購買伝票作成",
    "采购记录": "購買記録",
    "采购退货": "購買返品",
    "退货记录": "返品記録",
    "销售管理": "販売管理",
    "销售开单": "販売伝票作成",
    "销售记录": "販売記録",
    "销售退货": "販売返品",
    "入库任务": "入庫タスク",
    "出库任务": "出庫タスク",
    "盘点": "棚卸",
    "调拨": "在庫振替",
    "库存流水": "在庫推移",
    "财务管理": "財務管理",
    "应付欠款": "買掛金",
    "付款": "支払い",
    "应收欠款": "売掛金",
    "收款": "入金",
    "账户转账": "振出元口座",
    "日常收支": "日常収支",
    "资金流水": "資金明細",
    "系统管理": "システム管理",
    "角色管理": "ロール管理",
    "员工账号": "従業員アカウント",
    "系统配置": "システム設定",
    "项目名称": "プロジェクト名",
    "拥有者": "所有者",
    "备注": "備考",
    "编号": "コード",
    "编码": "コード",
    "条形码": "バーコード",
    "状态": "状態",
    "请选择状态": "状態を選択してください",
    "请选择": "選択してください",
    "客户": "顧客",
    "供应商": "仕入先",
    "供应商管理": "仕入先管理",
    "手机号": "携帯コード",
    "联系电话": "連絡先電話コード",
    "查询": "検索",
    "导入": "インポート",
    "导出": "エクスポート",
    "删除": "削除",
    "添加": "追加",
    "新增": "新規登録",
    "新增客户": "顧客新規登録",
    "新增供应商": "仕入先新規登録",
    "新增仓库": "入庫を追加",
    "新增角色": "ロール新規登録",
    "新增单位": "単位新規登録",
    "新增产品": "商品を追加",
    "新增产品信息": "商品情報を追加",
    "新增产品分类": "商品カテゴリを追加",
    "新增产品单位": "商品単位新規登録",
    "新增分类": "カテゴリを追加",
    "新增结算账户": "決済口座新規登録",
    "新增账户转账": "振出元口座新規登録",
    "新增收支项目": "収支項目新規登録",
    "新增收款单": "入金伝票新規登録",
    "新增付款单": "支払い伝票を追加",
    "新增日常收支": "日常収支新規登録",
    "新增生产计划": "生産計画新規登録",
    "新增生产任务": "生産タスク新規登録",
    "新增盘点": "棚卸新規登録",
    "新增调拨": "在庫振替新規登録",
    "新增附件": "添付ファイル新規登録",
    "新增采购订单": "購買注文新規登録",
    "新增采购退货": "購買返品新規登録",
    "新增销售订单": "販売注文新規登録",
    "新增销售退货": "販売返品新規登録",
    "新增入库单": "入庫伝票新規登録",
    "新增出库单": "出庫伝票新規登録",
    "模板": "テンプレート",
    "下载模板": "テンプレートダウンロード",
    "导入模板": "インポートテンプレート",
    "导出模板": "テンプレートをエクスポート",
    "保存成功": "保存成功",
}


def collect_strings(paths: Iterable[Path]) -> Dict[Path, set[str]]:
    """Collect Chinese strings for each file."""
    per_file_strings: Dict[Path, set[str]] = {}
    for path in paths:
        if path.suffix not in FILE_SUFFIXES or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        matches = {m.strip() for m in CJK_PATTERN.findall(text) if m.strip()}
        if matches:
            per_file_strings[path] = matches
    return per_file_strings


def load_cache() -> Dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: Dict[str, str]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def translate_text(text: str) -> str:
    url = "https://translate.googleapis.com/translate_a/single"
    params = {"client": "gtx", "sl": "zh-CN", "tl": "ja", "dt": "t", "q": text}
    for attempt in range(3):
        response = requests.get(url, params=params, timeout=15)
        if response.ok:
            data = response.json()
            return "".join(segment[0] for segment in data[0])
        time.sleep(1 + attempt)
    raise RuntimeError(f"Translation failed for: {text}")


def build_translation_map(strings: set[str], cache: Dict[str, str]) -> Dict[str, str]:
    updated = False
    for text in sorted(strings, key=len, reverse=True):
        if text in cache:
            continue
        if text in CUSTOM_TRANSLATIONS:
            cache[text] = CUSTOM_TRANSLATIONS[text]
            updated = True
            continue
        cache[text] = translate_text(text)
        updated = True
        time.sleep(0.2)
    if updated:
        save_cache(cache)
    return cache


def translate_file(source_path: Path, target_path: Path, translation_map: Dict[str, str]) -> bool:
    text = source_path.read_text(encoding="utf-8")
    translated_text = text
    # Replace longer strings first to avoid partial replacements.
    for src_text in sorted(translation_map, key=len, reverse=True):
        if src_text in translated_text:
            translated_text = translated_text.replace(src_text, translation_map[src_text])
    if translated_text != text:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(translated_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    if not SOURCE_ROOT.exists():
        raise SystemExit(f"Source directory not found: {SOURCE_ROOT}")

    source_files = list(SOURCE_ROOT.rglob("*"))
    per_file_strings = collect_strings(source_files)

    all_strings = set().union(*per_file_strings.values()) if per_file_strings else set()
    cache = load_cache()

    # Always prefer custom translations
    cache.update(CUSTOM_TRANSLATIONS)
    save_cache(cache)
    translation_map = build_translation_map(all_strings, cache)

    modified_files = []
    for source_path, strings in per_file_strings.items():
        target_path = TARGET_ROOT / source_path.relative_to(SOURCE_ROOT)
        local_map = {s: translation_map[s] for s in strings if s in translation_map}
        if translate_file(source_path, target_path, local_map):
            modified_files.append(target_path)

    print(f"Translated {len(modified_files)} files.")


if __name__ == "__main__":
    main()
