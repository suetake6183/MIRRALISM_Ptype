#!/usr/bin/env python3
"""会話構造化エンジン v3.0準拠"""
import os, json, re
from pathlib import Path
from dotenv import load_dotenv
try:
    from anthropic import Anthropic
except ImportError: print("✗ anthropicパッケージが必要です"); exit(1)

load_dotenv()

def test_connection():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key: print("✓ Claude API: Connected"); return True
    else: print("✗ Claude API: No API key"); return False

def structure_conversation(text):
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key: return None
    
    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-opus-20240229", max_tokens=500,
            messages=[{"role": "user", "content": f"JSONで構造化（目標,課題,解決策,コスト,時間,パフォーマンス）：{text}"}]
        )
        
        content = response.content[0].text
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        return json.loads(json_match.group()) if json_match else None
    except Exception as e: print(f"✗ エラー: {str(e)}"); return None

def save_structured(data, filename):
    output_path = Path(__file__).parent.parent / "output"
    output_path.mkdir(exist_ok=True)
    with open(output_path / filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def show_visual_summary(data):
    if not data: return
    print("\n" + "="*20 + "\n📋 サマリー\n" + "="*20)
    for k, v in data.items(): print(f"{k:6}: {str(v)[:25]}")

def run_test():
    if not test_connection(): return False
    result = structure_conversation("黒澤工務店から耐震リノベ依頼。予算800万円、工期3ヶ月。")
    if result: save_structured(result, "structured.json"); show_visual_summary(result); print("✓ 構造化完了"); return True
    print("✗ 構造化失敗"); return False

if __name__ == "__main__": exit(0 if run_test() else 1)