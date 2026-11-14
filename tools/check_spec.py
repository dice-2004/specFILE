#!/usr/bin/env python3
"""仕様書の形を確かめる。使い方は tools/README.md を参照。

  python3 tools/check_spec.py            リポジトリ全体
  python3 tools/check_spec.py FILE...    指定した仕様書だけ
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRY = ROOT / "AGENTS.md"

FULL = list(range(14))
SMALL = [0, 1, 2, 3, 4, 5, 7, 9, 11, 12, 13]
STATES = ("骨子", "たたき台", "レビュー済み", "承認済み")
PRIORITIES = ("Must", "Should", "Could", "Won't", "Won’t")
VAGUE = ("適切に", "速やかに", "使いやすく", "など")
ID_RE = re.compile(r"^N?FR(-[A-Z][A-Z0-9]*)?-\d{3}$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

errors, warnings = [], []


def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def err(path, msg):
    errors.append(f"{rel(path)}: {msg}")


def warn(path, msg):
    warnings.append(f"{rel(path)}: {msg}")


def clean(text):
    """コードブロックと HTML コメントを除く。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def links(path):
    """相対リンクの先（存在するもの）を返し、ないものをエラーにする。"""
    found = []
    for target in LINK_RE.findall(clean(path.read_text(encoding="utf-8"))):
        if re.match(r"^(https?:|mailto:|#)", target) or target.startswith("<"):
            continue
        dest = (path.parent / target.split("#")[0]).resolve()
        if dest.exists():
            found.append(dest)
        else:
            err(path, f"リンクの先がない: {target}")
    return found


def check_repo_links():
    files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    graph = {p.resolve(): links(p) for p in files}
    seen, queue = set(), [ENTRY.resolve()]
    while queue:
        cur = queue.pop()
        if cur in seen:
            continue
        seen.add(cur)
        queue.extend(graph.get(cur, []))
    for p in files:
        if p.resolve() not in seen:
            err(p, "AGENTS.md からリンクでたどれない")
    return files


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def requirement_rows(text):
    """「ID」と「優先度」の列を持つ表の行を、列名つきで返す。"""
    rows, header = [], None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            header = None
            continue
        row = cells(line)
        if header is None:
            header = row if "ID" in row and "優先度" in row else []
            continue
        if not header or set("".join(row)) <= set("-: "):
            continue
        rows.append(dict(zip(header, row)))
    return rows


def check_spec(path):
    text = clean(path.read_text(encoding="utf-8"))

    # 節
    nums = [int(n) for n in re.findall(r"^## (\d+)\. ", text, flags=re.M)]
    head = text.split("\n## 1. ")[0]
    required = SMALL if re.search(r"形式\s*\|\s*短い形", head) else FULL
    missing = [n for n in required if n not in nums]
    if missing:
        err(path, f"節がない: {missing}")
    if nums != sorted(nums):
        err(path, f"節の順番が違う: {nums}")

    # 状態と版
    m = re.search(r"\|\s*状態\s*\|\s*([^|]+?)\s*\|", head)
    state = m.group(1) if m else None
    if state not in STATES:
        err(path, f"0 の状態が {'／'.join(STATES)} のいずれでもない: {state}")
    m = re.search(r"\|\s*版\s*\|\s*(\d+)\.(\d+)\s*\|", head)
    if not m:
        err(path, "0 に版（例：0.1）がない")
    elif state == "承認済み" and int(m.group(1)) < 1:
        err(path, "承認済みなのに版が 1.0 未満")
    outline = state == "骨子"

    # 要件
    sec11 = re.search(r"^## 11\. .*?(?=^## 12\. |\Z)", text, flags=re.M | re.S)
    sec11 = sec11.group(0) if sec11 else ""
    seen = set()
    for row in requirement_rows(text):
        rid = row.get("ID", "")
        if not rid:
            continue
        if not ID_RE.match(rid):
            err(path, f"要件 ID の形が違う: {rid}")
            continue
        if rid in seen:
            err(path, f"要件 ID が重複している: {rid}")
        seen.add(rid)
        body = row.get("要件", "")
        if body.startswith("削除"):
            continue
        done = row.get("完了の条件", "")
        for word in VAGUE:
            if word in body or word in done:
                warn(path, f"{rid}: 判定できない言葉「{word}」がある")
        if outline:
            continue
        if row.get("優先度") not in PRIORITIES:
            err(path, f"{rid}: 優先度が Must／Should／Could／Won't のいずれでもない")
        if done in ("", "-", "—", "―"):
            err(path, f"{rid}: 完了の条件がない")
        if not re.search(r"(?<![A-Z0-9-])" + re.escape(rid) + r"(?!\d)", sec11):
            warn(path, f"{rid}: 11（完了の条件）に確かめ方がない")
    if not seen and 7 in nums:
        warn(path, "要件が 1 件もない")

    # 未決・仮定
    open_tags = len(re.findall(r"【(?:未決|仮定)[:：]", text))
    if state == "承認済み" and open_tags:
        warn(path, f"承認済みなのに【未決】【仮定】が {open_tags} か所残っている")
    return state, len(seen), open_tags


def is_spec(path):
    return re.search(r"^## 0\. 状態", path.read_text(encoding="utf-8"), flags=re.M)


def main(argv):
    if argv:
        targets = [Path(a).resolve() for a in argv]
        for p in targets:
            if not p.is_file():
                err(p, "ファイルがない")
        targets = [p for p in targets if p.is_file()]
        for p in targets:
            links(p)
    else:
        files = check_repo_links()
        targets = [p for p in files
                   if p.parts[len(ROOT.parts)] in ("templates", "specs") and is_spec(p)]
    for p in sorted(targets):
        state, n, tags = check_spec(p)
        print(f"{rel(p)}: 状態={state} 要件={n} 件 【未決】【仮定】={tags} か所")
    for w in warnings:
        print(f"警告: {w}")
    for e in errors:
        print(f"エラー: {e}")
    print(f"エラー {len(errors)} 件、警告 {len(warnings)} 件")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
