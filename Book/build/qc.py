# -*- coding: utf-8 -*-
"""qc.py — quality gate for every generated diagram.

Reports label collisions and text that runs off the canvas, so overlap is
caught by measurement instead of by eye.
"""
import importlib, sys
import svgkit as K


def run(module_names):
    problems = 0
    for mod_name in module_names:
        mod = importlib.import_module(mod_name)
        K.COLLECT = True
        for f in mod.ALL:
            try:
                f()
            except Exception:
                pass
        K.COLLECT = False
        K.flush()
        print(f"\n── {mod_name} ──")
        for f in mod.ALL:
            saved = {}

            def cap(self, path, _orig=K.SVG.save, _s=saved):
                _s["svg"] = self
                return _orig(self, path)
            K.SVG.save, old = cap, K.SVG.save
            try:
                f()
            finally:
                K.SVG.save = old
            svg = saved.get("svg")
            if svg is None:
                continue
            ov = svg.overlaps()
            oo = svg.out_of_frame()
            gc = svg.graphic_clashes()
            tag = "✓" if not ov and not oo and not gc else "✗"
            print(f"  {tag} {f.__name__:24s} text×text={len(ov):2d}  "
                  f"text×graphic={len(gc):2d}  off-canvas={len(oo)}")
            for kind, t in gc[:8]:
                print(f"        ⚠ {kind}: '{t[:44]}'")
            for a, b, dx, dy in ov[:6]:
                print(f"        ⚠ '{a[:34]}'  ×  '{b[:34]}'  ({dx}×{dy} px)")
            for t, x0, x1, y0, y1 in oo[:6]:
                print(f"        ⚠ off-canvas '{t[:40]}'  x:{x0}..{x1} y:{y0}..{y1}")
            problems += len(ov) + len(oo) + len(gc)
    print(f"\ntotal problems: {problems}")
    return problems


if __name__ == "__main__":
    sys.exit(1 if run(sys.argv[1:] or ["dia_ch01", "dia_ch02"]) else 0)
