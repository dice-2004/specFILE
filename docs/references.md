# テンプレートのもとにした外部の作法と出典

入口：[AGENTS.md](../AGENTS.md)

2026-11-15 に調べ、テンプレートに取り入れたものと見送ったものを記録する。閲覧日はすべて 2026-11-15。「確かめ方」の列は、原典を読んだか、解説で確かめたかを示す。

## 取り入れたもの

| 作法 | 出典 | 確かめ方 | 取り入れた場所 |
|---|---|---|---|
| 確かめ方の種類（Test／Demonstration／Inspection／Analysis） | ISO/IEC/IEEE 29148:2018、INCOSE Guide to Writing Requirements v4 | 解説・要約（規格の本文は未確認） | 本体の 11 の「種類」の列、[要件の文型](../templates/requirement-patterns.md) |
| 要件の 5 つの文型（EARS） | Mavin ほか（2009）。[Wikipedia の解説](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax)。Kiro も採用 | 解説（原論文は未確認） | [要件の文型](../templates/requirement-patterns.md) |
| 検討した案と選ばなかった理由 | [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)、[MADR](https://adr.github.io/madr)、Kubernetes KEP | 原典 | 本体の 13 |
| 公開の段取り、移行、戻し方、監視 | Kubernetes KEP のテンプレート、Volere | KEP は見出しだけ確認 | [足す節 F](../templates/sections/release.md) |
| 脅威の点検（STRIDE）、個人情報の扱い | [Microsoft Learn の脅威モデル](https://learn.microsoft.com/en-us/azure/well-architected/security/threat-model)、Design Docs at Google | 原典 | [足す節 G](../templates/sections/security.md) |
| 品質特性による抜けの点検 | ISO/IEC 25010:2023 | 解説 | 本体の 8 の注記 |
| 既存の振る舞いのうち変えないもの、実装する AI が決めてよい範囲 | O'Reilly Radar の記事（2026-08） | 原典 | 本体の 4 |
| 実装を終える前に実行するコマンドと完了の定義 | 「Writing an effective AGENTS.md」（2026-08） | 原典 | 本体の 11 |
| 最初に読む一文の要約、必要な文書だけを読ませる | Anthropic「Agent Skills」（2025-10） | 原典 | 本体の 1、AGENTS.md の文書一覧 |

## 見送ったもの

| 作法 | 出典 | 見送った理由 |
|---|---|---|
| 規範語（MUST／SHOULD／MAY） | RFC 2119 | 優先度（Must／Should／Could／Won't）と紛れるため。日本語の要件は「〜する」で言い切る |
| 要件ごとの関連要件（依存・衝突）の列 | INCOSE（R41） | 表が広くなる。依存は 10、矛盾は承認前のチェックで見る |
| 採算・想定問答（PR/FAQ） | Amazon（二次情報だけ確認） | 企画の文書の役割で、仕様書の範囲の外 |
| 設計（design）と作業の分割（tasks）を仕様書と対にする | Kiro、GitHub Spec Kit | 工房の成果は仕様書まで。実装の計画は実装する側が作る |
| 仕様書を実装後に捨てる（短い指示書にする） | O'Reilly Radar の記事 | 承認済みの版を残して改訂する工房の方針と合わない。長さの抑制は「短い形」で対応する |

## 確認できなかったもの

Rust RFC、Python PEP、Nygard の ADR、C4、WCAG、各社の PRD テンプレート、Planguage、ISO/IEC/IEEE 29148 の本文は、原典を読めていない。
