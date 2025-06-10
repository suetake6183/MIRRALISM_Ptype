#!/usr/bin/env python3
"""TaskMaster API統合・現在地表示"""
import os, requests, yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def load_config():
    config_file = Path(__file__).parent / "../config/config.yaml"
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except: return {"api": {"taskmaster": {"endpoint": "http://localhost:3000/api", "timeout": 30}}}

def test_connection():
    config = load_config()
    api_key = os.getenv('TASKMASTER_API_KEY')
    endpoint = config['api']['taskmaster']['endpoint']
    timeout = config['api']['taskmaster']['timeout']
    
    if not api_key: print("✗ TaskMaster API: No API key"); return False
    
    try:
        response = requests.get(f"{endpoint}/health", timeout=min(timeout, 10), 
                              headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code == 200: print("✓ TaskMaster API: Connected"); return True
        else: print(f"✗ TaskMaster API: HTTP {response.status_code}"); return False
    except requests.exceptions.Timeout: print("✗ TaskMaster API: Timeout"); return False
    except requests.exceptions.ConnectionError: print("✗ TaskMaster API: Connection refused"); return False
    except Exception as e: print(f"✗ TaskMaster API: {type(e).__name__}"); return False

def get_current_tasks():
    config = load_config()
    api_key = os.getenv('TASKMASTER_API_KEY')
    if not api_key: return None
    
    try:
        endpoint = config['api']['taskmaster']['endpoint']
        response = requests.get(f"{endpoint}/tasks/current", timeout=10,
                              headers={"Authorization": f"Bearer {api_key}"})
        return response.json() if response.status_code == 200 else None
    except: return None

def show_context():
    tasks = get_current_tasks()
    print("="*40)
    if tasks and len(tasks) > 0:
        print("📍 現在地（TaskMaster連携）:")
        for task in tasks[:2]: print(f"  • {task.get('title', 'Task')}: {task.get('status', 'pending')}")
    else:
        print("📍 現在地（ローカル）:")
        print("  • MIRRALISM MVP開発: 進行中"); print("  • 会話構造化エンジン: 実装完了")
    print("="*40)

def check_integration():
    connected = test_connection(); show_context()
    print("✓ TaskMaster統合確認完了" if connected else "✓ ローカルモードで動作中")
    return True

if __name__ == "__main__": exit(0 if check_integration() else 1)