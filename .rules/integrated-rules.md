# MIRRALISM 統合開発ルール

## TaskMaster使用時
1. 現在のタスクを確認: `task-master next`
2. タスク実装時は以下を遵守：
   - 各ファイル120行以内（API統合）
   - その他は50行以内
   - 新機能禁止

## 品質チェック
- タスク完了前: `python check_rules.py`
- TaskMaster完了: `task-master complete [task-id]`

## 作業フロー
1. TaskMasterで現在のタスクを確認
2. 実装時はこのルールに従う
3. check_rules.pyで品質確認
4. 合格したらTaskMasterでタスク完了