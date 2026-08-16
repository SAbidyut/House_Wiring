# -*- coding: utf-8 -*-
"""mathguard.py — বাংলা-ইন-OMML ধরার পাহারাদার।

OMML রান বাংলা যুক্তাক্ষর ও কার-চিহ্ন ভেঙে দেয় এবং শব্দের ফাঁকা মুছে
ফেলে — অধ্যায় ১৪-এ `ডাইভার্সিটি ফ্যাক্টর` হয়ে গিয়েছিল
“ডাইভার্সিটিফ্যাক্টর”, অধ্যায় ১৬-এ `ফ্রিজ` হয়েছিল “িফ্রজ”।  সোর্স পড়ে
এটা চোখে পড়ে না, ছাপা পিডিএফে পড়ে।

তাই একটা AST হাঁটা: `b.math(...)`-এর আর্গুমেন্টে বা
`b.worked_example(..., steps=[...])`-এর ভেতরে কোনো বাংলা কোডপয়েন্ট
থাকলেই ধরিয়ে দেয়।  `given=` / `find=` বাদ — ওগুলো `_rich`-এ যায়,
সাধারণ বডি টেক্সট, বাংলা সেখানে বৈধ।

    python mathguard.py ch17.py
"""
import ast
import sys

BN = range(0x0980, 0x0A00)


def _bangla(s):
    return sorted({c for c in s if ord(c) in BN})


def _strings(node):
    """একটি এক্সপ্রেশনের ভেতরের সব স্ট্রিং লিটারাল।"""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            yield sub


def check(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), path)
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
        targets = []
        if name == "math":
            targets = [("math()", a) for a in node.args]
        elif name in ("worked_example", "equation"):
            targets = [(f"{k.arg}=", k.value) for k in node.keywords
                       if k.arg == "steps"]
        for where, arg in targets:
            for lit in _strings(arg):
                found = _bangla(lit.value)
                if found:
                    bad.append((lit.lineno, where, lit.value.strip(),
                                "".join(found)))
    return bad


if __name__ == "__main__":
    files = sys.argv[1:] or ["ch17.py"]
    total = 0
    for f in files:
        hits = check(f)
        total += len(hits)
        print(f"── {f} ──")
        for line, where, text, chars in hits:
            print(f"  ✗ line {line} in {where}: {text!r}   বাংলা: {chars}")
        if not hits:
            print("  ✓ কোনো বাংলা কোডপয়েন্ট নেই")
    sys.exit(1 if total else 0)
