#!/usr/bin/env python3
"""情報一元管理システム v3.0準拠"""
import os, shutil, hashlib
from datetime import datetime, timedelta
from pathlib import Path

def check_duplicate(filepath):
    if not os.path.exists(filepath): return False
    file_hash = hashlib.md5(Path(filepath).read_bytes()).hexdigest()
    
    for dir_name in ["input", "output", "process"]:
        if os.path.exists(dir_name):
            for root, _, files in os.walk(dir_name):
                for file in files:
                    check_path = os.path.join(root, file)
                    if check_path != filepath:
                        try:
                            if hashlib.md5(Path(check_path).read_bytes()).hexdigest() == file_hash:
                                print(f"✗ 重複: {check_path}"); return True
                        except: pass
    print("✓ 重複なし"); return False

def cleanup_tmp(days=7):
    tmp_path = "tmp/daily"
    if not os.path.exists(tmp_path): return
    cutoff = datetime.now() - timedelta(days=days); cleaned = 0
    for item in os.listdir(tmp_path):
        path = os.path.join(tmp_path, item)
        if os.path.getmtime(path) < cutoff.timestamp():
            try:
                if os.path.isdir(path): shutil.rmtree(path)
                else: os.remove(path)
                cleaned += 1
            except: pass
    print(f"✓ {cleaned}個整理")

def ensure_dirs():
    for d in ["input", "process", "output", "tmp/daily"]: os.makedirs(d, exist_ok=True)
    print("✓ ディレクトリ確認完了")


def run_test():
    ensure_dirs(); cleanup_tmp()
    Path("test.txt").write_text("test"); check_duplicate("test.txt"); os.remove("test.txt")
    print("✓ テスト完了"); return True

if __name__ == "__main__": exit(0 if run_test() else 1)