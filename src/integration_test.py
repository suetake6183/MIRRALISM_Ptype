#!/usr/bin/env python3
"""統合テストスイート v3.0準拠"""
import time, json, os
from pathlib import Path
from test_claude_api import test_connection as claude_test, structure_conversation
from test_taskmaster_api import test_connection as taskmaster_test
from file_manager import ensure_dirs

def integration_test():
    print("🔄 統合テスト開始")
    tm_ok = taskmaster_test(); claude_ok = claude_test()
    dataflow_ok = structure_conversation("テスト") is not None if claude_ok else False
    passed = sum([tm_ok, claude_ok, dataflow_ok])
    print(f"✓ 統合テスト: {passed}/3 合格")
    return passed == 3

def scenario_test():
    print("📋 シナリオテスト開始"); ensure_dirs()
    start = time.time()
    result = structure_conversation("リノベ相談。予算500万円、期間2ヶ月。")
    elapsed = time.time() - start
    
    if result:
        output_file = Path("output/test_scenario.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)
        print(f"✓ シナリオテスト完了 ({elapsed:.2f}秒)")
        os.remove(output_file); return True
    print("✗ シナリオテスト失敗"); return False

def performance_test():
    print("⚡ パフォーマンステスト開始")
    start = time.time()
    result = structure_conversation("パフォーマンステスト用データ")
    elapsed = time.time() - start
    target = 3.0; success = elapsed <= target and result is not None
    status = "✓" if success else "✗"
    print(f"{status} 処理時間: {elapsed:.2f}秒 (目標: {target}秒以内)")
    return success

def run_all_tests():
    print("🧪 MIRRALISM統合テストスイート v3.0"); tests = [integration_test, scenario_test, performance_test]; results = []
    for test in tests:
        try: results.append(test())
        except Exception as e: print(f"✗ エラー: {str(e)}"); results.append(False)
    passed = sum(results); print(f"📊 結果: {passed}/{len(results)} 合格"); return passed == len(results)

if __name__ == "__main__": exit(0 if run_all_tests() else 1)