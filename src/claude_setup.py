#!/usr/bin/env python3
"""
Claude Code セットアップマネージャー
MIRRALISM プロトタイプ v3.0準拠
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict


class ClaudeSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_path = self.project_root / "config" / "config.yaml"
        self.env_path = self.project_root / ".env"
        load_dotenv(self.env_path)
    
    def check_environment(self) -> Dict[str, bool]:
        """環境設定の確認"""
        checks = {
            "config_file": self.config_path.exists(),
            "env_file": self.env_path.exists(),
            "claude_api_key": bool(os.getenv('ANTHROPIC_API_KEY')),
            "anthropic_package": self._check_package("anthropic"),
            "dotenv_package": self._check_package("python-dotenv")
        }
        return checks
    
    def _check_package(self, package_name: str) -> bool:
        """パッケージの存在確認"""
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
    
    def create_env_file(self) -> bool:
        """環境ファイルの作成"""
        if self.env_path.exists():
            print("✓ .envファイルは既に存在します")
            return True
        
        example_path = self.project_root / "config.env.example"
        if not example_path.exists():
            print("✗ config.env.exampleファイルが見つかりません")
            return False
        
        try:
            with open(example_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(self.env_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✓ .envファイルを作成しました")
            print("  → API キーを設定してください")
            return True
        except Exception as e:
            print(f"✗ .envファイル作成エラー: {e}")
            return False
    
    def test_claude_connection(self) -> bool:
        """Claude API接続テスト"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or api_key == 'your-claude-api-key-here':
            print("✗ ANTHROPIC_API_KEYが設定されていません")
            return False
        
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            
            # 簡単なテストリクエスト
            client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "テスト"}]
            )
            
            print("✓ Claude API接続成功")
            return True
        except Exception as e:
            print(f"✗ Claude API接続エラー: {e}")
            return False
    
    def setup_directories(self) -> bool:
        """必要ディレクトリの作成"""
        directories = [
            "input", "output", "process", "tmp", "data",
            "logs", "config", "src", "tests"
        ]
        
        created = []
        for dir_name in directories:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                created.append(dir_name)
        
        if created:
            print(f"✓ ディレクトリを作成: {', '.join(created)}")
        else:
            print("✓ 必要ディレクトリは全て存在します")
        
        return True
    
    def install_packages(self) -> bool:
        """必要パッケージのインストール"""
        requirements_path = self.project_root / "requirements.txt"
        if not requirements_path.exists():
            print("✗ requirements.txtファイルが見つかりません")
            return False
        
        print("📦 パッケージをインストール中...")
        import subprocess
        try:
            result = subprocess.run([
                "pip", "install", "-r", str(requirements_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ パッケージインストール完了")
                return True
            else:
                print(f"✗ インストールエラー: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ インストール実行エラー: {e}")
            return False
    
    def run_full_setup(self) -> bool:
        """フルセットアップの実行"""
        print("🚀 MIRRALISM Claude Code セットアップ開始\n")
        
        steps = [
            ("ディレクトリ作成", self.setup_directories),
            ("環境ファイル作成", self.create_env_file),
            ("パッケージインストール", self.install_packages),
        ]
        
        success_count = 0
        for name, func in steps:
            print(f"📋 {name}...")
            if func():
                success_count += 1
            print()
        
        print("🔍 最終確認...")
        checks = self.check_environment()
        
        # 結果表示
        print("\n" + "="*40)
        print("📊 セットアップ結果")
        print("="*40)
        
        for check, status in checks.items():
            symbol = "✓" if status else "✗"
            print(f"{symbol} {check}: {'OK' if status else 'NG'}")
        
        all_success = all(checks.values())
        
        if all_success:
            print("\n🎉 Claude Code セットアップ完了！")
            print("次のステップ:")
            print("1. .envファイルに実際のAPI キーを設定")
            print("2. test_claude_api.pyでテスト実行")
        else:
            print("\n⚠️  セットアップに問題があります")
            print("上記のNGエラーを修正してください")
        
        return all_success


def main():
    """メイン実行関数"""
    setup = ClaudeSetup()
    setup.run_full_setup()


if __name__ == "__main__":
    main() 