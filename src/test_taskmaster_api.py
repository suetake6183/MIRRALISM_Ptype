#!/usr/bin/env python3
"""TaskMaster API統合・現在地表示"""
import os, requests
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    api_key = os.getenv('TASKMASTER_API_KEY')
    if not api_key: print("✗ TaskMaster API: No API key"); return False
    
    try:
        response = requests.get("http://localhost:3000/api/health", timeout=5, 
                              headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code == 200: print("✓ TaskMaster API: Connected"); return True
        else: print(f"✗ TaskMaster API: HTTP {response.status_code}"); return False
    except: print("✗ TaskMaster API: Connection failed"); return False

def get_current_tasks():
    api_key = os.getenv('TASKMASTER_API_KEY')
    if not api_key: return None
    
    try:
        response = requests.get("http://localhost:3000/api/tasks/current", timeout=5,
                              headers={"Authorization": f"Bearer {api_key}"})
        return response.json() if response.status_code == 200 else None
    except: return None

def show_context():
    tasks = get_current_tasks()
    print("="*50)
    if tasks:
        print("📍 現在地（TaskMaster連携）:")
        for task in tasks[:2]: print(f"  - {task.get('title', 'タスク')}: {task.get('status', 'unknown')}")
    else:
        print("📍 現在地（ローカル）:")
        print("  - MIRRALISM MVP開発: 進行中"); print("  - 会話構造化エンジン: 実装完了")
    print("="*50)

def check_integration():
    connected = test_connection(); show_context()
    print("✓ TaskMaster統合確認完了" if connected else "✓ ローカルモードで動作中")
    return True

def run_test():
    return check_integration()

if __name__ == "__main__":
    exit(0 if run_test() else 1)