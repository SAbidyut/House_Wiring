# -*- coding: utf-8 -*-
"""One-shot: pull each full-book chapter's MCQ bank + answer key, slice the
first N per the digest size map, and write smmcq.py for the digest chapters."""
import ast, re, os

HERE = os.path.dirname(os.path.abspath(__file__))

# digest MCQ count per chapter (big -> 10, small -> 6-8)
COUNT = {
    1: 10, 2: 8, 3: 8, 4: 6, 5: 9, 6: 7, 7: 6, 8: 7, 9: 6, 10: 6,
    11: 9, 12: 6, 13: 8, 14: 8, 15: 8, 16: 6, 17: 6, 18: 9, 19: 9, 20: 7,
    21: 8, 22: 10, 23: 9, 24: 8, 25: 7, 26: 8, 27: 7, 28: 8,
}

BN_DIGIT = {"০": 0, "১": 1, "২": 2, "৩": 3, "৪": 4, "৫": 5, "৬": 6,
            "৭": 7, "৮": 8, "৯": 9}
LET = ["ক", "খ", "গ", "ঘ", "ঙ"]


def bn2int(s):
    return int("".join(str(BN_DIGIT[c]) for c in s))


def parse_key(src):
    m = re.search(r"উত্তরমালা:\*\*", src)
    if not m:
        return {}
    # the key string may be split across several adjacent string literals;
    # take a generous window up to the box's title= / closing paren.
    tail = src[m.end():m.end() + 600]
    tail = re.split(r'title\s*=|\)\s*\n', tail, 1)[0]
    tail = tail.replace('"', " ").replace("'", " ").replace("+", " ")
    out = {}
    for a, x in re.findall(r"([০-৯]+)\s*[-–]\s*([কখগঘঙ])", tail):
        out[bn2int(a)] = x
    return out


def extract(chnum):
    path = os.path.join(HERE, f"ch{chnum:02d}.py")
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    items = []
    # Form A: mcq = [ (q, [opts]), ... ]
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "mcq" for t in node.targets):
            try:
                lst = ast.literal_eval(node.value)
                for q, opts in lst:
                    items.append((q, list(opts)))
            except Exception:
                pass
    # Form B: b.mcq(n, "q", [opts], ...)
    if not items:
        calls = []
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "mcq" and len(node.args) >= 3):
                try:
                    n = ast.literal_eval(node.args[0])
                    q = ast.literal_eval(node.args[1])
                    opts = list(ast.literal_eval(node.args[2]))
                    calls.append((n, q, opts))
                except Exception:
                    pass
        calls.sort()
        items = [(q, o) for _, q, o in calls]
    key = parse_key(src)
    return items, key


def main():
    def bn(x):
        return str(x).translate(str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯"))

    def pick(items, key, n):
        """Take the first n questions; only if that leaves a letter with no
        correct answer, swap the fewest questions (from just past n) to fix it."""
        chosen = list(range(n))                       # 0-indexed; key is i+1
        used = set(chosen)
        def counts():
            seq = [key[i + 1] for i in chosen]
            return {L: seq.count(L) for L in LET[:4]}
        for L in LET[:4]:
            if counts()[L] == 0:
                # find the earliest unused bank question whose answer is L
                repl = next((i for i in range(len(items))
                             if i not in used and key.get(i + 1) == L), None)
                if repl is None:
                    continue
                # drop one question of the currently most-common letter
                c = counts()
                top = max(c, key=c.get)
                drop = max(i for i in chosen if key[i + 1] == top)
                chosen[chosen.index(drop)] = repl
                chosen.sort()
                used.discard(drop); used.add(repl)
        return chosen

    blocks = []
    for ch in range(1, 29):
        items, key = extract(ch)
        n = COUNT[ch]
        assert len(items) >= n, f"ch{ch}: only {len(items)} MCQs, need {n}"
        assert all(i in key for i in range(1, n + 1)), f"ch{ch}: key gap"
        idx = pick(items, key, n)
        sub = [items[i] for i in idx]
        subkey = ", ".join(f"{bn(j)}-{key[i + 1]}" for j, i in enumerate(idx, 1))
        letters = [key[i + 1] for i in idx]
        dist = {L: letters.count(L) for L in LET[:4]}
        print(f"ch{ch:02d}: {n} MCQ  key spread {dist}")
        lines = [f"    {ch}: {{"]
        lines.append('        "key": ' + repr(subkey) + ",")
        lines.append('        "items": [')
        for q, opts in sub:
            lines.append(f"            ({q!r}, {opts!r}),")
        lines.append("        ],")
        lines.append("    },")
        blocks.append("\n".join(lines))
    out = (
        "# -*- coding: utf-8 -*-\n"
        '"""অনুশীলনী — বহুনির্বাচনী প্রশ্ন, পূর্ণাঙ্গ বই থেকে বাছাই করা (auto by _genmcq.py)।"""\n\n'
        "MCQ = {\n" + "\n".join(blocks) + "\n}\n\n\n"
        "def mcq_section(b, ch):\n"
        '    d = MCQ[ch]\n'
        '    b.h1("অনুশীলনী — বহুনির্বাচনী প্রশ্ন")\n'
        '    for i, (q, opts) in enumerate(d["items"], 1):\n'
        '        b.mcq(i, q, opts, cols=2)\n'
        '    b.box("note", "**উত্তরমালা:**  " + d["key"], title="✔  উত্তরমালা")\n'
    )
    open(os.path.join(HERE, "smmcq.py"), "w", encoding="utf-8").write(out)
    print("\nwrote smmcq.py")


if __name__ == "__main__":
    main()
