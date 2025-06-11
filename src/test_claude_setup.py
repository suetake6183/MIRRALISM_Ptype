#!/usr/bin/env python3
"""Claude Code セットアップテスト"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from claude_setup import ClaudeSetup


def test_basic_setup():
    """基本的なセットアップテスト"""
    print("🧪 Claude Code セットアップテスト開始\n")
    
    setup = ClaudeSetup()
    
    # 環境チェック
    checks = setup.check_environment()
    print("📋 環境チェック結果:")
    for check, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {check}")
    
    return all(checks.values())


def test_claude_api():
    """Claude API接続テスト"""
    print("\n🔌 Claude API テスト:")
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your-claude-api-key-here':
        print("  ⚠️  API キーが設定されていません")
        print("  → .envファイルでANTHROPIC_API_KEYを設定してください")
        return False
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[{
                "role": "user", 
                "content": "「MIRRALISM テスト成功」と日本語で返答してください"
            }]
        )
        
        result = response.content[0].text
        print(f"  ✓ API応答: {result}")
        return True
        
    except Exception as e:
        print(f"  ✗ API エラー: {e}")
        return False


def test_conversation_structuring():
    """会話構造化テスト"""
    print("\n📊 会話構造化テスト:")
    
    try:
        from test_claude_api import structure_conversation
        
        test_text = "新しいWebアプリを開発する。React、Node.js使用。予算300万円、期間6ヶ月。"
        result = structure_conversation(test_text)
        
        if result:
            print("  ✓ 構造化成功:")
            for key, value in result.items():
                print(f"    {key}: {value}")
            return True
        else:
            print("  ✗ 構造化失敗")
            return False
            
    except Exception as e:
        print(f"  ✗ 構造化エラー: {e}")
        return False


def run_all_tests():
    """全テストの実行"""
    load_dotenv()
    
    tests = [
        ("基本セットアップ", test_basic_setup),
        ("Claude API", test_claude_api),
        ("会話構造化", test_conversation_structuring),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"🧪 {name} テスト")
        print('='*40)
        
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ テストエラー: {e}")
            results.append((name, False))
    
    # 結果まとめ
    print(f"\n{'='*40}")
    print("📊 テスト結果まとめ")
    print('='*40)
    
    success_count = 0
    for name, success in results:
        symbol = "✓" if success else "✗"
        print(f"{symbol} {name}: {'成功' if success else '失敗'}")
        if success:
            success_count += 1
    
    print(f"\n成功率: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
    
    if success_count == len(results):
        print("\n🎉 全てのテストが成功しました！")
        print("Claude Code の使用準備が完了しています。")
    else:
        print("\n⚠️  一部のテストが失敗しました。")
        print("設定を確認してください。")
    
    return success_count == len(results)


if __name__ == "__main__":
    exit(0 if run_all_tests() else 1) 