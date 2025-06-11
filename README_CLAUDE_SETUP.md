# MIRRALISM Claude Code セットアップガイド

MIRRALISM プロトタイプでClaude Codeを使用するためのセットアップ手順です。

## 📋 事前準備

### 1. Anthropic API キーの取得
1. [Anthropic Console](https://console.anthropic.com/)にアクセス
2. アカウント作成またはログイン
3. API キーを生成
4. 課金設定を確認（使用量に応じて課金されます）

### 2. Python環境の確認
```bash
python --version  # Python 3.8以上が必要
pip --version     # pipが利用可能であること
```

## 🚀 自動セットアップ（推奨）

### 1. セットアップスクリプトの実行
```bash
# プロジェクトディレクトリに移動
cd /Users/suetakeshuuhei/MIRRALISM_PROTOTYPE

# セットアップ実行
python src/claude_setup.py
```

セットアップでは以下が実行されます：
- 必要ディレクトリの作成
- 環境設定ファイル（.env）の作成
- Pythonパッケージのインストール
- 環境チェック

### 2. API キーの設定
セットアップ完了後、生成された`.env`ファイルを編集：

```bash
# .envファイルを開く
nano .env

# 以下の行を編集
ANTHROPIC_API_KEY=your-actual-api-key-here
```

### 3. 動作確認
```bash
# テストの実行
python src/test_claude_setup.py
```

## 🔧 手動セットアップ

自動セットアップがうまくいかない場合の手動手順：

### 1. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 2. 環境ファイルの作成
```bash
# テンプレートをコピー
cp config.env.example .env

# API キーを設定
nano .env
```

### 3. 必要ディレクトリの作成
```bash
mkdir -p output process tmp data logs tests
```

### 4. 設定ファイルの確認
`config/config.yaml`が存在し、適切に設定されていることを確認。

## 🧪 テストの実行

### 基本テスト
```bash
# 全体テスト
python src/test_claude_setup.py

# 個別API テスト
python src/test_claude_api.py

# 統合テスト
python src/integration_test.py
```

### 期待される結果
```
🧪 基本セットアップ テスト
========================================
  ✓ config_file
  ✓ env_file
  ✓ claude_api_key
  ✓ anthropic_package
  ✓ dotenv_package

🔌 Claude API テスト
  ✓ API応答: MIRRALISM テスト成功

📊 会話構造化テスト
  ✓ 構造化成功:
    目標: 新しいWebアプリを開発する
    課題: React、Node.js技術習得
    解決策: 段階的開発とチーム体制
    コスト: 300万円
    時間: 6ヶ月
    パフォーマンス: 高性能UI実装

📊 テスト結果まとめ
========================================
✓ 基本セットアップ: 成功
✓ Claude API: 成功
✓ 会話構造化: 成功

成功率: 3/3 (100.0%)

🎉 全てのテストが成功しました！
Claude Code の使用準備が完了しています。
```

## 🔍 トラブルシューティング

### 問題1: API キーエラー
```
✗ Claude API: No API key
```
**解決策：**
1. `.env`ファイルが存在するか確認
2. `ANTHROPIC_API_KEY`が正しく設定されているか確認
3. API キーが有効で課金設定が完了しているか確認

### 問題2: パッケージエラー
```
✗ anthropicパッケージが必要です
```
**解決策：**
```bash
pip install anthropic python-dotenv
```

### 問題3: ファイルが見つからない
```
✗ config.env.exampleファイルが見つかりません
```
**解決策：**
1. プロジェクトのルートディレクトリにいるか確認
2. `config.env.example`ファイルが存在するか確認
3. 手動で`.env`ファイルを作成

## 📁 ファイル構造

セットアップ完了後のファイル構造：
```
MIRRALISM_PROTOTYPE/
├── .env                    # API キー設定（Git除外）
├── config.env.example      # 環境設定テンプレート
├── requirements.txt        # Python依存パッケージ
├── config/
│   └── config.yaml         # アプリケーション設定
├── src/
│   ├── claude_setup.py     # セットアップマネージャー
│   ├── test_claude_setup.py # セットアップテスト
│   ├── test_claude_api.py  # Claude API テスト
│   └── ...
├── output/                 # 処理結果出力
├── tmp/                    # 一時ファイル
└── logs/                   # ログファイル
```

## 🎯 次のステップ

1. **会話構造化の実行**
   ```bash
   python src/test_claude_api.py
   ```

2. **TaskMaster統合の確認**
   ```bash
   python src/test_taskmaster_api.py
   ```

3. **本格的な開発開始**
   - MIRRALISM_Ptype_V3.mdの設計書に従って開発
   - 設定ファイルのカスタマイズ
   - 追加機能の実装

## 📞 サポート

問題が発生した場合：
1. エラーメッセージの詳細を確認
2. テストログを確認
3. `test_claude_setup.py`の詳細結果を確認
4. 必要に応じて設定を見直し

---
**注意:** API キーは絶対にGitにコミットしないでください。`.env`ファイルは自動的に`.gitignore`で除外されています。 