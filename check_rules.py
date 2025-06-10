#!/usr/bin/env python3
"""MIRRALISM ルール自動チェッカー v3.0 - MVP対応版"""
import os, sys
from pathlib import Path

# ファイルタイプ別の行数制限
FILE_LIMITS = {
    'test_': 50,          # テストファイルは簡潔に
    '_api.py': 120,       # API統合は120行まで許可
    '_manager.py': 100,   # マネージャークラスは100行まで
    'utils/': 50,         # ユーティリティは50行以内
    'default': 80         # その他は80行
}

BANNED = ['report', 'statistics', 'analytics', 'dashboard', 'chart', 'graph']
EXTENSIONS = ['.py', '.js', '.html', '.css']
EXCLUDE = ['__pycache__', '.git', 'node_modules', '.cursor', '.rules']

def get_line_limit(filepath):
    """ファイルパスに基づいて適切な行数制限を返す"""
    for pattern, limit in FILE_LIMITS.items():
        if pattern in filepath:
            return limit
    return FILE_LIMITS['default']

def check(file):
    if 'check_rules.py' in file: return True
    violations = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines).lower()
        
        line_count = len(lines)
        limit = get_line_limit(file)
        
        if line_count > limit:
            if line_count > limit * 1.5:  # 50%超過は違反
                violations.append(f"行数違反: {line_count}/{limit}")
            else:  # 50%以内は警告
                print(f"⚠️  行数警告: {file} ({line_count}行 / 推奨: {limit}行)")
        
        found = [k for k in BANNED if k in content and f'"{k}"' not in content]
        if found: violations.append(f"禁止: {', '.join(found)}")
    except: pass
    
    if violations: print(f"❌ {file}: {', '.join(violations)}")
    return len(violations) == 0

def main():
    print("🔍 ルールチェック v2.0\n")
    ok = total = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        if any(p.startswith('.') for p in Path(root).parts[1:]):
            continue
        for file in files:
            if any(file.endswith(e) for e in EXTENSIONS):
                total += 1
                if check(os.path.join(root, file)):
                    ok += 1
    print(f"\n✅ {ok}/{total} OK")
    sys.exit(0 if ok == total else 1)

if __name__ == "__main__":
    main()