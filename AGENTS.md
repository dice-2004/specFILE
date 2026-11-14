# AGENTS.md（入口）

このリポジトリは、仕様書工房（Claude のプロジェクト）で仕様書を作るための道具と成果物を置く場所である。このファイルが入口で、ここからすべての文書へリンクでたどれる。

## 規則の正

- 書き方の規則（進め方、構成、要件の書き方、版と ID、承認前のチェック）の正は、プロジェクト「仕様書工房」の指示（プロジェクト設定）である。
- このリポジトリの文書は、その規則を使いやすい形にしたものである。規則の文章は写さず、テンプレートの形と手順の対応だけを持つ。食い違いを見つけたら指示に従い、[ワークフロー](docs/workflow.md) の「工房の整備」の手順で直しを提案する。

## 文書一覧

| 文書 | 役割 | 読む人 |
|---|---|---|
| [docs/workflow.md](docs/workflow.md) | 仕様書を作る手順と、各段で使うテンプレートの対応。工房の整備の手順 | 仕様書を作る人・AI |
| [templates/README.md](templates/README.md) | テンプレートの一覧と選び方 | 仕様書を作る人・AI |
| [templates/spec.md](templates/spec.md) | 仕様書の本体（0〜13 の全節） | 仕様書を作る人・AI |
| [templates/spec-small.md](templates/spec-small.md) | 小さな機能追加用の短い形 | 仕様書を作る人・AI |
| [templates/spec-child.md](templates/spec-child.md) | 大きな対象を分けた子の仕様書 | 仕様書を作る人・AI |
| [templates/sections/screens.md](templates/sections/screens.md) | 足す節 A：画面 | 仕様書を作る人・AI |
| [templates/sections/api.md](templates/sections/api.md) | 足す節 B：API | 仕様書を作る人・AI |
| [templates/sections/data.md](templates/sections/data.md) | 足す節 C：データ | 仕様書を作る人・AI |
| [templates/sections/batch.md](templates/sections/batch.md) | 足す節 D：バッチ・外部連携 | 仕様書を作る人・AI |
| [templates/sections/operations.md](templates/sections/operations.md) | 足す節 E：業務・運用手順 | 仕様書を作る人・AI |
| [templates/hearing.md](templates/hearing.md) | 聞き取りの質問票 | 仕様書を作る人・AI |
| [templates/review-request.md](templates/review-request.md) | レビュワーへの依頼文と指摘の記録 | 仕様書を作る人・AI |
| [specs/README.md](specs/README.md) | 承認済みの仕様書の一覧 | 実装する人・AI、承認者 |
| [tools/README.md](tools/README.md) | 検証スクリプトの使い方 | 仕様書を作る人・AI |
| [README.md](README.md) | リポジトリの紹介 | 初めて来た人 |

## このリポジトリで作業する AI への決まり

1. 文書を足したら、この文書一覧に行を足す。入口からたどれない文書は置かない。
2. 承認済みの仕様書（`specs/` の下にあるものも、Claude Docs にあるものも）の要件の追加・削除・優先度の変更は、ユーザーの承認を得てから行う。
3. 変更したら `python3 tools/check_spec.py` を実行し、エラーが 0 件であることを確かめてから PR にする。
4. 用語・要件は 1 か所にだけ書き、ほかからは要件 ID とリンクで参照する。
