# -*- coding: utf-8 -*-
"""অধ্যায় ১১ — জয়েন্ট, স্প্লাইস ও সোল্ডারিং : ডায়াগ্রাম।

**২০২৬-০৮-২৫ — দ্বিতীয় ও পূর্ণ পুনর্নির্মাণ।**  ব্যবহারকারীর দ্বিতীয়
পর্যবেক্ষণ:  আসল ছবিগুলো ঘোলা, আর আঁকা জয়েন্টে "অনেক ভুল"।  দুটোই
সঠিক ছিল।

──  ছবি  ──────────────────────────────────────────────────────────────
Abuz Mordecai-র তিনটি আলোকচিত্র (ওয়েস্টার্ন ইউনিয়ন, টি, ব্রিটানিয়া)
**বাদ**।  ওগুলো মোবাইলে তোলা ও ফোকাসের বাইরে — মূল ফাইলেই ঝাপসা, কাজেই
শার্পেনিং করে লাভ নেই (আনশার্প মাস্ক কেবল নয়েজটাই ধারালো করে)।  ছাপা
বইয়ে ঘোলা ছবির চেয়ে নিখুঁত আঁকা ছবি ভালো।  যে ছবিগুলো সত্যিই ঝকঝকে —
জংশন বক্সের পিগটেল ও কানেক্টর ক্যাপ, ওয়্যার নাট, লিভার কানেক্টর,
সোল্ডারিং আয়রন — সেগুলো আছে।

──  আঁকা  ─────────────────────────────────────────────────────────────
ভুলটা একটাই ছিল, কিন্তু প্রতিটি জয়েন্টে:  পুরনো `wrap()` কেবল কয়েকটা
হেলানো দাগ টানত।  ফলে (ক) মূল তার পাকের নিচে হারিয়ে যেত, (খ) যে তার
জড়াচ্ছে তার সঙ্গে পাকের কোনো ধারাবাহিকতা থাকত না — শাখা-তার এক জায়গায়
শেষ, পাশে একটা আলাদা স্প্রিং।  ছবিটা "তারের গায়ে তার জড়ানো" নয়,
"তারের পাশে স্প্রিং" পড়াত।

এখন পাক আসল হেলিক্স, **ত্রিমাত্রিকভাবে** হিসাব করা:

    বিন্দু(t) = p0 + u·(tL) + n·(r·cos θ)      θ = 2π·turns·t + phase
    গভীরতা(t) = sin θ         (+১ = চোখের দিকে, −১ = তারের পেছনে)

গভীরতা ধনাত্মক হলে ওই টুকরো মূল তারের **সামনে**, ঋণাত্মক হলে **পেছনে**।
আঁকার ক্রম তাই — পেছনের টুকরো → মূল তার → সামনের টুকরো।  এতেই পাক
তারটিকে সত্যি জড়িয়ে ধরে;  আর গভীরতা অনুযায়ী রং বদলানোয় পাকটা গোল
দেখায়।  দুই তার পরস্পরে পাকানো (`twist2`) একই হিসাব, কেবল দুটি হেলিক্স
১৮০° ব্যবধানে।

সংশোধিত বিষয়বস্তুর ভুল (`qc.py` এগুলোর একটিও ধরে না — ও ধরে লেখার
সংঘর্ষ, বস্তুর গঠন নয়):

* **ব্রিটানিয়া** — আগে একটিমাত্র মোটা দণ্ড আঁকা ছিল, অথচ এই জয়েন্টের
  সংজ্ঞাই "দুই তার **পাশাপাশি** রেখে বাঁধা"।  এখন দুটি আলাদা তার,
  একটির প্রান্ত উপরে ও অন্যটির নিচে সমকোণে ভাঁজ, আর বাঁধন-তার দুটিকেই
  একসঙ্গে জড়ায় (তাই ডিম্বাকার হেলিক্স)।
* **ফিক্সচার** — আগে দুই তার সমান মোটা ছিল, অথচ এই জয়েন্টই হয় অসম মোটা
  তারে;  আর "প্রান্ত ভাঁজ" বলতে এখন সত্যিই মোটা তারের ডগা পাকের উপর
  ফিরে আসে।
* **ক্রস** — দুই শাখা এখন এক বিন্দু থেকে দুই বিপরীত দিকে, আর জড়ানো পাক
  শাখা-তারেরই ধারাবাহিকতা।
* **ম্যারিড** — 'খ' ধাপে খেই এখন সত্যি চিরুনির দাঁতের মতো **পরস্পরের
  ফাঁকে** ঢোকে;  শেষ ধাপে জোড়াটা দুই দিকে সরু হয়ে আসে (তাই টেপার)।
* **টেপ** — আগে চ্যাপ্টা কালো পাখনা ছিল, চিরুনির মতো দেখাত;  এখন টেপও
  হেলিক্স, প্রতিটি পাক আগেরটির অর্ধেক ঢেকে (হাফ-ল্যাপ)।

**টাইপের মাপ:** ১২৪০ px ক্যানভাস ১৫.৪ সেমিতে বসলে `N px = N × 0.352 pt`।
সবচেয়ে ছোট লেখা `T_SMALL` ২৩ px = ৮.১ পয়েন্ট।  কোনো চিত্র ১৫.৪ সেমির
চেয়ে সরু করে বসানো হয় না — `ch11.py` প্রস্থের অভিধানটাই লুপে বানায়।
"""
import math
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap as tw_wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch11")
IMG = os.path.join(HERE, "assets", "ch11")

# ১২৪০ px ক্যানভাস ১৫.৪ সেমি চওড়া = ৪৩৬.৫ pt → ১ px = ০.৩৫২ pt
T_TITLE = 38
T_HEAD = 27
T_NODE = 30
T_BODY = 25
T_SMALL = 23
T_CALL = 27
LH = 1.42

# ── উপকরণের রং:  প্রান্ত (ছায়া) · গা · ঝিলিক ─────────────────────────
CU = "#CE8636"           # তামা
CU_SH = "#79450F"
CU_HL = "#F7D6A0"
BIND = "#C98A45"         # বাঁধন-তার — একটু হালকা, যাতে মূল তার থেকে আলাদা
INS_K, INS_KE, INS_KH = "#39434F", "#0E141A", "#8A98A6"      # কালো
INS_R, INS_RE, INS_RH = "#A8342A", "#4E1610", "#E0736A"      # লাল
INS_B, INS_BE, INS_BH = "#28518C", "#12253F", "#7CA2D8"      # নীল
INS_G, INS_GE, INS_GH = "#3F7A46", "#17331B", "#8EC195"      # সবুজ (আর্থ)
SHEATH, SHEATH_E, SHEATH_H = "#9AA5B0", "#4F5A65", "#DCE3E9"  # যমজ তারের খোল
TAPE, TAPE_E, TAPE_H = "#2A323B", "#080C10", "#66727E"        # পিভিসি টেপ


# ── জ্যামিতির খুচরা কাজ ────────────────────────────────────────────────
def _axis(p0, p1):
    """দুই বিন্দুর মাঝে একক ভেক্টর, লম্ব ভেক্টর ও দৈর্ঘ্য।"""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    return (dx / L, dy / L), (-dy / L, dx / L), L


def _P(p0, u, n, a, b):
    """অক্ষ বরাবর a, লম্বে b — ফেরত আসল স্থানাঙ্ক।"""
    return (p0[0] + u[0] * a + n[0] * b, p0[1] + u[1] * a + n[1] * b)


def within(name, lo, hi, bounds):
    """আঁকা বস্তু প্যানেলের ভেতরে আছে কি না — না থাকলে বিল্ড থামে।

    `qc.py` লেখার সংঘর্ষ দেখে, বাক্সের সীমা নয় (অধ্যায় ১৯ ও ২৩-এর
    শিক্ষা):  ছবির একটা কোণ প্যানেলের বাইরে বেরিয়ে গেলেও ও পরিষ্কার
    রিপোর্ট দেয়।  জয়েন্টের লম্বা কতটা হবে তা এখন তারের মোটা থেকে হিসাব
    হয়, তাই প্যানেল ছোট হলে চুপচাপ উপচে পড়ার আশঙ্কা আসল — এই
    পাহারাদারটাই সেটা ধরে।

    **খাড়া দিকেও লাগে।**  ট্যাপ ও ক্রস জয়েন্টের শাখা-তার নিচে (ও উপরে)
    নেমে যায়;  প্যানেল ছোট হলে শাখার ডগা প্যানেলের কিনারা কেটে বেরিয়ে
    যায় আর উপরের ডগা শিরোনামের চিপে গিয়ে ঠেকে — দুটোই একবার ছাপা
    হয়েছিল, আর `qc.py` দুটোর একটিও ধরেনি।"""
    if bounds is None:
        return
    x0, x1 = bounds
    if lo < x0 - 0.5 or hi > x1 + 0.5:
        raise SystemExit("✗ %s প্যানেল ছাপিয়ে গেছে: [%.0f, %.0f] ⊄ [%.0f, %.0f]"
                         % (name, lo, hi, x0, x1))


def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def _mix(c1, c2, t):
    a, b = _hex(c1), _hex(c2)
    t = 0.0 if t < 0 else (1.0 if t > 1 else t)
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t)
                                   for i in range(3))


def _dstr(pts):
    return "M " + " L ".join("%.1f %.1f" % (x, y) for x, y in pts)


def _offset(pts, d):
    """পলিলাইনকে তার নিজের লম্ব বরাবর d দূরে সরানো — ঝিলিকের জন্য।"""
    if not d:
        return pts
    out, n = [], len(pts)
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[-2][0], y - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1.0
        out.append((x - dy / L * d, y + dx / L * d))
    return out


# ── নলাকার তার ────────────────────────────────────────────────────────
#
# গ্রেডিয়েন্ট ব্যবহার করা হয়নি ইচ্ছা করেই:  ছবিটা ওয়ার্ডে **SVG হিসেবেই**
# বসে (`bookkit._add_svg`), আর ওয়ার্ড ও লিব্রেঅফিসের SVG রেন্ডারার এক নয়।
# তাই গোলত্ব আসে ধাপে ধাপে সরু ও উজ্জ্বল স্ট্রোক থেকে — নিছক `<path>`,
# সব রেন্ডারারে একরকম।  বাইরের গাঢ় রেখাটিই `qc.py`-র চোখে পড়ে;  ভেতরের
# ব্যান্ডগুলো `add()` দিয়ে সরাসরি বসে, নইলে একটি হেলিক্সই `shapes`-এ
# কয়েকশো এন্ট্রি ঢেলে qc-কে অচল করে দেয়।

def tube(s, pts, th, base=CU, edge=CU_SH, hi=CU_HL, bands=6, record=True):
    """একটি পথ → নলাকার তার।  `pts` অন্তত দুটি বিন্দু।"""
    d0 = _dstr(pts)
    if record:
        s.path(d0, edge, th + 2.6)
    else:
        s.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" '
              'stroke-linecap="round" stroke-linejoin="round"/>'
              % (d0, edge, th + 2.6))
    body = _mix(edge, base, 0.78)
    for k in range(bands):
        f = k / (bands - 1.0) if bands > 1 else 1.0
        w = th * (1 - 0.80 * f)
        col = _mix(body, hi, f ** 1.2)
        p = _offset(pts, -th * 0.30 * f)
        s.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" '
              'stroke-linecap="round" stroke-linejoin="round"/>'
              % (_dstr(p), col, w))


def straight(s, p0, p1, th, base=CU, edge=CU_SH, hi=CU_HL, bands=6):
    tube(s, [p0, p1], th, base, edge, hi, bands)


def copper(s, p0, p1, th=17):
    straight(s, p0, p1, th)


def insul(s, p0, p1, th=30, col=INS_K, edge=INS_KE, hi=INS_KH, cut=None):
    """ইনসুলেশনে মোড়া তার।  `cut` = কোন প্রান্তে কাটা মুখ দেখা যাবে
    (`0` শুরুতে, `1` শেষে) — খালি তামা যেখান থেকে বেরোয়।"""
    straight(s, p0, p1, th, col, edge, hi)
    if cut is not None:
        u, n, L = _axis(p0, p1)
        c = p1 if cut else p0
        s.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" '
              'transform="rotate(%.2f %.1f %.1f)"/>'
              % (c[0], c[1], th * 0.17, th * 0.50, _mix(edge, "#000000", 0.35),
                 math.degrees(math.atan2(u[1], u[0])), c[0], c[1]))


# ── হেলিক্স:  তারের গায়ে তার জড়ানো ───────────────────────────────────
def _helix_pts(p0, p1, turns, r, phase=0.0, spt=30, taper=None):
    """হেলিক্সের নমুনা-বিন্দু ও প্রতিটির গভীরতা (sin θ)।

    `turns` ঋণাত্মক দিলে পাক উল্টো দিকে ঘোরে — ব্রিটানিয়ার বাঁধন মাঝ
    থেকে দুই দিকে যায় বলে তার দুই অর্ধেকের হাত (handedness) উল্টো, আর
    ভালো আঁকায় সেটা চোখে পড়ে।"""
    u, n, L = _axis(p0, p1)
    N = max(12, int(round(abs(turns) * spt)))
    out = []
    for i in range(N + 1):
        t = i / N
        a = 2 * math.pi * turns * t + phase
        k = taper(t) if taper else 1.0
        out.append((_P(p0, u, n, t * L, r * k * math.cos(a)), math.sin(a)))
    return out


def _split(pts):
    """সিলুয়েট বরাবর ভাগ → [(সামনে?, বিন্দু-তালিকা, গড় গভীরতা), …]।

    ক্রসিং-বিন্দুটি দুই অংশেই রাখা হয়, নইলে জোড়ের মুখে ফাঁক থাকে।"""
    runs, cur, dep = [], [pts[0][0]], [pts[0][1]]
    front = pts[0][1] >= 0
    for i in range(1, len(pts)):
        p, d = pts[i]
        f = d >= 0
        if f != front:
            cur.append(p); dep.append(d)
            runs.append((front, cur, sum(dep) / len(dep)))
            cur, dep, front = [pts[i - 1][0], p], [pts[i - 1][1], d], f
        else:
            cur.append(p); dep.append(d)
    runs.append((front, cur, sum(dep) / len(dep)))
    return [r for r in runs if len(r[1]) > 1]


def _run_tube(s, pts, d, th, base=CU, edge=CU_SH, hi=CU_HL, bands=None):
    """গভীরতা অনুযায়ী রং — পেছনের পাক গাঢ়, সামনেরটা উজ্জ্বল।

    ব্যান্ডের সংখ্যা তারের মোটা থেকে নেওয়া:  মোটা তারে কম ব্যান্ড দিলে
    ছায়ার ধাপ চোখে পড়ে আর পাকগুলো চ্যাপ্টা লজেন্সের মতো দেখায়।
    `bands` হাতে দিলে সেটাই মানা হয় — টেপের ফিতে গোল নয়, তাই ওখানে ২।"""
    if bands is None:
        bands = max(3, min(6, int(th / 6.0) + 2))
    b = _mix(_mix(edge, base, 0.55), base, d + 1) if d < 0 \
        else _mix(base, hi, d * 0.42)
    e = _mix(edge, "#000000", 0.30) if d < 0 else edge
    tube(s, pts, th, b, e, hi, bands=bands, record=False)


def helix_end(p0, p1, turns, r, phase=0.0, taper=None, at=0.0):
    """পাক আঁকার **আগে** তার শুরু/শেষ বিন্দুটি জানা দরকার হয়।"""
    u, n, L = _axis(p0, p1)
    a = 2 * math.pi * turns * at + phase
    k = taper(at) if taper else 1.0
    return _P(p0, u, n, at * L, r * k * math.cos(a))


def twist2(s, p0, p1, turns=6, th=15, r=None, phase=0.0,
           cols=((CU, CU_SH, CU_HL), (CU, CU_SH, CU_HL)), spt=30, taper=None):
    """দুই তার পরস্পরে পাকানো — একই হিসাব, দুটি হেলিক্স ১৮০° ব্যবধানে।

    দুটোই আধা-পাক পরপর সামনে-পেছনে যায়, তাই পেছনের সব অংশ আগে আর
    সামনের সব অংশ পরে আঁকলেই আসল মোচড়ের চেহারা আসে।"""
    r = r if r is not None else th * 0.58
    sets = [(_split(_helix_pts(p0, p1, turns, r, phase + k * math.pi, spt,
                               taper)), cols[k]) for k in (0, 1)]
    for want in (False, True):
        for runs, (b, e, h) in sets:
            for f, pts, d in runs:
                if f == want:
                    _run_tube(s, pts, d, th, b, e, h)


def strands(s, p0, p1, n_str=7, spread=44, th=6, phase=0.0, base=CU):
    """বহু খেইয়ের তারের ছড়ানো খেই — ম্যারিড জয়েন্টের প্রথম ধাপ।"""
    u, n, L = _axis(p0, p1)
    tips = []
    for i in range(n_str):
        f = (i / (n_str - 1) - 0.5) * 2          # −১ … +১
        tip = _P(p0, u, n, L, f * spread)
        mid = _P(p0, u, n, L * 0.38, f * spread * 0.22)
        col = _mix(base, CU_HL, 0.30) if i % 2 else base
        tube(s, [p0, mid, tip], th, col, CU_SH, CU_HL, bands=3, record=False)
        tips.append(tip)
    return tips


def knife(s, tip, ang, blade=104, bol=12, handle=74, spine=-1, h=25):
    """ইলেকট্রিশিয়ান নাইফ — ডগা `tip`-এ, `ang` ডিগ্রিতে হাতলের দিক।

    আগে ফলাটা ছিল নিছক একটা ত্রিভুজ, তাই খাড়া ধরলে ছুঁচের মতো আর শোয়ানো
    থাকলে ধূসর কীলকের মতো দেখাত — কোন দিকটা ধার তা বোঝাই যেত না।  এখন
    আসল ফলার আকার:  **ধার সোজা, পিঠ বাঁকা** (শিপসফুট), সঙ্গে ঝকঝকে
    বেভেল, বোলস্টার আর রিভেটসহ কাঠের হাতল।

    `spine` ঠিক করে পিঠ কোন পাশে, অর্থাৎ ধার কোন দিকে মুখ করে আছে —
    ছোলার ছবিতে ধার তারের দিকে থাকতেই হবে।"""
    a = math.radians(ang)
    u = (math.cos(a), math.sin(a))            # ডগা → হাতল
    n = (-u[1], u[0])
    sp = h * spine
    P = lambda d, w: (tip[0] + u[0] * d + n[0] * w,
                      tip[1] + u[1] * d + n[1] * w)
    F = lambda *pts: " ".join("%.1f %.1f" % p for p in pts)

    # ফলা:  ধার (w = 0) সোজা, পিঠ বাঁকা হয়ে ডগায় নামে
    s.path("M %s L %s L %s Q %s %s Z"
           % (F(P(0, 0)), F(P(blade, 0)), F(P(blade, sp)),
              F(P(blade * 0.34, sp * 1.20)), F(P(0, 0))),
           "#59636D", 2.4, fill="#C3CCD5")
    # বেভেল — ধার বরাবর সরু উজ্জ্বল ফালি
    s.path("M %s L %s Q %s %s Z"
           % (F(P(2, 0)), F(P(blade * 0.94, 0)),
              F(P(blade * 0.46, sp * 0.34)), F(P(2, 0))),
           "none", 0, fill="#E9EFF4")
    # বোলস্টার — ফলার চেয়ে সামান্য গভীর, কলারের মতো মোটা নয়
    s.poly([P(blade, -h * 0.06 * spine), P(blade + bol, -h * 0.10 * spine),
            P(blade + bol, sp * 1.12), P(blade, sp * 1.06)],
           "#8D969F", "#4E575F", 2.2)

    # হাতল — দুই ধার **সমান্তরাল**, লেজের মুখ গোল।
    #
    # আগের সংস্করণে শেষ Q-কমান্ডটির নিয়ন্ত্রণ-বিন্দু ছিল হাতলের সামনের
    # উপরের কোণে আর শেষবিন্দু সামনের নিচের কোণে — অর্থাৎ একটিমাত্র বাঁকা
    # রেখা গোটা হাতলটা কেটে বেরিয়ে যেত।  ফলে হাতল সামনে সরু, লেজে চওড়া
    # — জুতোর মতো দেখাত।  এখন উপরের ধারটাও সোজা `L`, আর গোলত্ব কেবল
    # লেজের মুখে।
    d0, d1 = blade + bol, blade + bol + handle
    lo, hi = -h * 0.16 * spine, sp * 1.16
    cap = h * 0.62
    s.path("M %s L %s Q %s %s L %s Z"
           % (F(P(d0, lo)), F(P(d1 - cap, lo)),
              F(P(d1 + cap * 0.42, (lo + hi) / 2)), F(P(d1 - cap, hi)),
              F(P(d0, hi))),
           "#241811", 2.4, fill="#4A3428")
    # কাঠের গায়ে আলোর রেখা ও দুটি রিভেট
    s.path("M %s L %s" % (F(P(d0 + h * 0.42, lo + (hi - lo) * 0.26)),
                          F(P(d1 - cap * 0.9, lo + (hi - lo) * 0.26))),
           "#6B4B36", h * 0.17)
    for f in (0.26, 0.62):
        c = P(d0 + handle * f, (lo + hi) / 2)
        s.circle(c[0], c[1], h * 0.12, "#B9A48E", "#2E2018", 1.2)


def magnifier(s, cx, cy, r, inner, src=None, ring=STEEL, sw=5):
    """বৃত্তাকার বিবর্ধক — ভেতরে `inner()` যা আঁকে তা-ই বড় করে দেখায়।

    `clip_begin` আয়তক্ষেত্র নেয়, কিন্তু বাহু = ব্যাস আর `rx` = ব্যাসার্ধ
    দিলে সেটিই বৃত্ত — তাই আলাদা ক্লিপ-পাথ লাগে না।"""
    if src:
        for sgn in (-1, 1):
            s.path("M %.1f %.1f L %.1f %.1f"
                   % (src[0] + sgn * 11, src[1] + 9,
                      cx + sgn * r * 0.74, cy - r * 0.66),
                   ring, 1.8, opacity=0.55)
    s.circle(cx, cy, r, "#FFFFFF")
    s.clip_begin(cx - r, cy - r, 2 * r, 2 * r, rx=r)
    inner()
    s.clip_end()
    s.circle(cx, cy, r, "none", ring, sw)


def notch(s, x, cy, cu, bg="#FCFDFE", crack=True):
    """তামার গায়ে ছুরির কাটা খাঁজ — ও তা থেকে নামা চুলচেরা ফাটল।

    খাঁজটা আঁকা হয় পটভূমির রঙে ভরা একটি 'V' দিয়ে, তামার **উপরে** —
    তাতে তামার নিজের গাঢ় প্রান্তরেখাটাও ঢাকা পড়ে, আর সত্যিকারের কাটা
    দাগের মতো দেখায়।"""
    top = cy - cu * 0.5 - 4
    apex = cy + cu * 0.12
    s.poly([(x - cu * 0.44, top), (x + cu * 0.44, top), (x, apex)],
           bg, CU_SH, 2.6)
    if crack:
        s.path("M %.1f %.1f L %.1f %.1f L %.1f %.1f"
               % (x, apex, x - cu * 0.10, apex + cu * 0.20,
                  x + cu * 0.04, apex + cu * 0.40), CU_SH, 2.0)


def wound_multi(s, core, *segs):
    """একাধিক পাক-অঞ্চল, কিন্তু মূল তার একবারই আঁকা।

    নটেড ট্যাপে গিঁট আর জড়ানো — দুটো আলাদা হেলিক্স, অথচ মূল তার একটাই;
    আলাদা করে `wound()` দুবার ডাকলে দ্বিতীয় ডাকের মূল তার প্রথমটির
    সামনের পাক ঢেকে দিত।  প্রতিটি `seg` একটি dict:
    `p0 p1 turns r th [phase taper base edge hi spt]`।"""
    R = []
    for g in segs:
        R.append((_split(_helix_pts(g["p0"], g["p1"], g["turns"], g["r"],
                                    g.get("phase", 0.0), g.get("spt", 30),
                                    g.get("taper"))), g))
    for want in (False, True):
        if want and core:
            core()
        for runs, g in R:
            for f, pts, d in runs:
                if f == want:
                    _run_tube(s, pts, d, g["th"], g.get("base", CU),
                              g.get("edge", CU_SH), g.get("hi", CU_HL),
                              g.get("bands"))


def wound(s, p0, p1, core, turns=6, r=20, th=13, phase=0.0, base=CU,
          edge=CU_SH, hi=CU_HL, taper=None, spt=30, bands=None):
    """একটিই পাক-অঞ্চল — `wound_multi`-র সহজ রূপ।"""
    wound_multi(s, core, dict(p0=p0, p1=p1, turns=turns, r=r, th=th,
                              phase=phase, base=base, edge=edge, hi=hi,
                              taper=taper, spt=spt, bands=bands))


# ── শিট বানানোর খুচরা কাজ ─────────────────────────────────────────────
def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_HEAD, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_BODY):
    """একটি চিত্রে একটিই নোট, এক লাইনে, নিছক তথ্য (অধ্যায় ১৫-এর নিয়ম)।"""
    import svgkit as _K
    if not _K.COLLECT and tw(text, size, 700) > w - 40:
        raise SystemExit("✗ নোট এক লাইনে ধরে না (%.0f px): %s…"
                         % (tw(text, size, 700), text[:50]))
    s.rect(x, y, w, 62, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 39, text, size, tcolor, 700, "middle")
    return y + 62


def img_panel(s, x, y, w, h, title, img, col=STEEL, pad=16):
    """নির্দিষ্ট উচ্চতার প্যানেলে ছবি — সারিতে সব প্যানেল সমান রাখতে।"""
    from PIL import Image as _I
    panel(s, x, y, w, h, title, col)
    bw, bh = w - 2 * pad, h - 62 - pad
    with _I.open(img) as im:
        iw, ih = im.size
    k = min(bw / iw, bh / ih)
    dw, dh = iw * k, ih * k
    dx, dy = x + pad + (bw - dw) / 2, y + 62 + (bh - dh) / 2
    s.image(dx, dy, dw, dh, img, 6)
    # হালকা প্রান্তরেখা — নইলে সাদা জমিনে তোলা ছবির কিনারা প্যানেলের
    # সাদা ভেতরে মিশে যায় (ছাপার পিডিএফে ধরা পড়েছিল)
    s.rect(dx, dy, dw, dh, "none", "#9AA7B4", 1.6, 6)


def step_cards(s, steps, x0, y0, bw, bh, gx, gy, per_row, ar):
    """নম্বরযুক্ত ধাপের কার্ড — সারিতে তীরসহ।"""
    dig = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮"]
    for i, (t, d) in enumerate(steps):
        r, c = divmod(i, per_row)
        x = x0 + c * (bw + gx)
        y = y0 + r * (bh + gy)
        s.rect(x, y, bw, bh, "#F5F9FC", STEEL, 2, 13)
        s.circle(x + 46, y + 46, 28, NAVY)
        s.text(x + 46, y + 57, dig[i], T_NODE, "#FFFFFF", 700, "middle")
        s.text(x + 88, y + 57, t, T_HEAD, NAVY, 700)
        for j, ln in enumerate(tw_wrap(d, bw - 60, T_SMALL, 400)):
            s.text(x + 30, y + 112 + j * T_SMALL * 1.38, ln, T_SMALL,
                   "#39434D", 400)
        if c < per_row - 1 and i < len(steps) - 1:
            s.path("M %.0f %.0f L %.0f %.0f" % (x + bw + 4, y + bh / 2,
                                                x + bw + gx - 8, y + bh / 2),
                   STEEL, 3.2, marker=ar)
    return y0 + ((len(steps) - 1) // per_row + 1) * bh + \
        ((len(steps) - 1) // per_row) * gy


# ── জয়েন্টগুলোর আঁকা রূপ ──────────────────────────────────────────────
#
# সাধারণ নিয়ম, প্রতিটি ফাংশনে মানা হয়েছে:
#
# ১. **পাক আঁটসাঁট।**  আসল জয়েন্টে পাক পাকের গায়ে লেগে থাকে;  ফাঁক
#    থাকলে সোল্ডারও ধরে না, টানও সয় না।  তাই জয়েন্টের মাপ ঠিক হয়
#    তারের মোটা থেকে — `পাকের দৈর্ঘ্য = পাকসংখ্যা × তারের ব্যাস × ১.০৬`
#    — প্যানেলের চওড়া থেকে নয়।  প্রথম ড্রাফটে উল্টোটা করা হয়েছিল, ফলে
#    ছয় পাক ৩০০ px জুড়ে ছড়িয়ে দড়ির মতো দেখাত।
# ২. হেলিক্স সবসময় **বাঁ থেকে ডানে** আঁকা;  কোন প্রান্তে তার উপরে না
#    নিচে থাকবে তা ঠিক করে `phase` (পাকসংখ্যা পূর্ণসংখ্যা হলে দুই
#    প্রান্তে কোণ এক)।  উল্টো দিকে আঁকলে লম্ব ভেক্টরের চিহ্ন উল্টে যায়
#    আর জোড়ের মুখ মেলে না।
# ৩. যে তার জড়াচ্ছে তার খালি তামা এসে **ঠিক হেলিক্সের প্রথম বিন্দুতে**
#    শেষ হয় — পাকটা তাই ওই তারেরই ধারাবাহিকতা, আলাদা স্প্রিং নয়।
# ৪. মূল তার আঁকা হয় `wound*()`-এর ভেতর থেকে, তাই পেছনের পাক তার নিচে
#    আর সামনের পাক তার উপরে পড়ে।

PITCH = 1.06             # পাশাপাশি দুই পাকের কেন্দ্রের দূরত্ব ÷ তারের ব্যাস
TPITCH = 2.05            # পরস্পর-পাকে এক পাকে অক্ষ বরাবর কতটা এগোয়


def _lead(s, p_ins, p_cut, p_end, ins_th, cu_th, col):
    """ইনসুলেশনসহ তার, তারপর খালি তামা — কাটা মুখ ঠিক জায়গায়।"""
    insul(s, p_ins, p_cut, ins_th, *col, cut=1)
    u, n, L = _axis(p_cut, p_end)
    copper(s, _P(p_cut, u, n, -3, 0), p_end, cu_th)


def wu_joint(s, cx, cy, cu=18, mid_turns=2, end_turns=5, ins=250,
             lcol=(INS_K, INS_KE, INS_KH), rcol=(INS_R, INS_RE, INS_RH),
             bounds=None):
    """ওয়েস্টার্ন ইউনিয়ন জয়েন্ট, সম্পূর্ণ — `cx`-এ কেন্দ্র করে।

    গঠনটা বইয়ের ১১.৫.১ যা বলে ঠিক তাই:  মাঝখানে দুই তার **পরস্পরে**
    পাকানো, আর দুই প্রান্তে একটির ডগা অন্যটির গায়ে জড়ানো।  বাঁ তারের
    ডগা ডান দিকে গিয়ে ডান তারের গায়ে জড়ায়, ডান তারের ডগা বাঁ দিকে —
    তাই মাঝের মোচড়ের দুই মাথায় দুই হেলিক্সের কোণ হুবহু মেলাতে হয়
    (`phase` π ও ০, পাকসংখ্যা পূর্ণসংখ্যা)।  ফেরত দেয় মাঝের মোচড়ের
    দুই সীমা ও জয়েন্টের বাইরের দুই প্রান্ত।"""
    We = end_turns * cu * PITCH
    Wm = mid_turns * cu * TPITCH
    ml, mr = cx - Wm / 2, cx + Wm / 2
    lw0, rw1 = ml - We, mr + We          # জড়ানো পাকের বাইরের সীমা
    bx0, bx1 = lw0 - cu * 0.9, rw1 + cu * 0.9
    r = cu * 0.98
    within("ওয়েস্টার্ন ইউনিয়ন", bx0 - ins, bx1 + ins, bounds)
    _lead(s, (bx0 - ins, cy), (bx0, cy), (lw0, cy), cu + 15, cu, lcol)
    _lead(s, (bx1 + ins, cy), (bx1, cy), (rw1, cy), cu + 15, cu, rcol)
    wound_multi(
        s,
        lambda: (copper(s, (bx0, cy), (ml, cy), cu),
                 copper(s, (mr, cy), (bx1, cy), cu)),
        dict(p0=(lw0, cy), p1=(ml, cy), turns=end_turns, r=r, th=cu,
             phase=math.pi),
        dict(p0=(mr, cy), p1=(rw1, cy), turns=end_turns, r=r, th=cu,
             phase=0.0))
    twist2(s, (ml, cy), (mr, cy), mid_turns, cu, r=cu * 0.52)
    return ml, mr, bx0 - ins, bx1 + ins


def tap_joint(s, cx, cy, cu=18, turns=6, knot=False, drop=140, ins=150,
              tail=110, branch=(INS_R, INS_RE, INS_RH), bounds=None,
              ybounds=None):
    """টি বা ট্যাপ জয়েন্ট — মূল লাইন আস্ত, শাখা-তার জড়ানো।

    শাখা নিচ থেকে উঠে মূল তারের **তলার সিলুয়েটে** এসে ঠেকে (`phase` ০),
    সেখান থেকেই প্রথম পাক সামনের দিকে বেরিয়ে যায়।  নটেড ট্যাপে জড়ানোর
    আগে একটি পূর্ণ আংটি — সেটিও হেলিক্সই, কেবল এক পাক আর অক্ষটা ছোট,
    তাই বাকি পাকের চেয়ে চওড়া হয়ে আলাদা চোখে পড়ে।"""
    Wt = turns * cu * PITCH
    kw = cu * 1.9 if knot else 0.0
    xs = cx - (kw + Wt) / 2                  # শাখা যেখানে এসে মেশে
    r = cu * 0.98
    bx0, bx1 = xs - tail, xs + kw + Wt + tail
    within("টি জয়েন্ট", bx0 - ins, bx1 + ins, bounds)
    within("টি জয়েন্টের খাড়া মাপ", cy - max(r + cu * 0.5, (cu + 15) * 0.5) - 2,
           cy + drop + (cu + 11) * 0.5 + 2, ybounds)
    _lead(s, (bx0 - ins, cy), (bx0, cy), (bx0 + 6, cy), cu + 15, cu,
          (INS_K, INS_KE, INS_KH))
    _lead(s, (bx1 + ins, cy), (bx1, cy), (bx1 - 6, cy), cu + 15, cu,
          (INS_K, INS_KE, INS_KH))
    _lead(s, (xs, cy + drop), (xs, cy + drop - 62), (xs, cy + r), cu + 11,
          cu, branch)
    segs = [dict(p0=(xs + kw, cy), p1=(xs + kw + Wt, cy), turns=turns, r=r,
                 th=cu, phase=0.0)]
    if knot:
        segs.insert(0, dict(p0=(xs, cy), p1=(xs + kw, cy), turns=1,
                            r=r * 1.12, th=cu, phase=0.0, spt=48))
    wound_multi(s, lambda: copper(s, (bx0, cy), (bx1, cy), cu), *segs)


def cross_joint(s, cx, cy, cu=18, turns=5, knot=False, reach=150, ins=120,
                tail=64, bounds=None, ybounds=None):
    """ক্রস জয়েন্ট — এক বিন্দু থেকে **দুটি** শাখা, দুই বিপরীত দিকে।

    উপরের শাখা বাঁ দিকে জড়ায়, নিচেরটা ডান দিকে।  উপরের হেলিক্সও বাঁ
    থেকে ডানে আঁকা, কেবল `phase` π — তাতে তার ডান মাথাটা তারের **উপরে**
    পড়ে, যেখানে শাখাটি এসে ঠেকেছে।"""
    Wt = turns * cu * PITCH
    kw = cu * 1.9 if knot else 0.0
    r = cu * 0.98
    bx0, bx1 = cx - kw - Wt - tail, cx + kw + Wt + tail
    within("ক্রস জয়েন্ট", bx0 - ins, bx1 + ins, bounds)
    within("ক্রস জয়েন্টের খাড়া মাপ", cy - reach - (cu + 11) * 0.5 - 2,
           cy + reach + (cu + 11) * 0.5 + 2, ybounds)
    _lead(s, (bx0 - ins, cy), (bx0, cy), (bx0 + 6, cy), cu + 15, cu,
          (INS_K, INS_KE, INS_KH))
    _lead(s, (bx1 + ins, cy), (bx1, cy), (bx1 - 6, cy), cu + 15, cu,
          (INS_K, INS_KE, INS_KH))
    for sgn, col in ((-1, (INS_B, INS_BE, INS_BH)),
                     (1, (INS_R, INS_RE, INS_RH))):
        _lead(s, (cx, cy + sgn * reach), (cx, cy + sgn * (reach - 66)),
              (cx, cy + sgn * r), cu + 11, cu, col)
    segs = [dict(p0=(cx - kw - Wt, cy), p1=(cx - kw, cy), turns=turns, r=r,
                 th=cu, phase=math.pi),
            dict(p0=(cx + kw, cy), p1=(cx + kw + Wt, cy), turns=turns, r=r,
                 th=cu, phase=0.0)]
    if knot:
        segs += [dict(p0=(cx - kw, cy), p1=(cx, cy), turns=1, r=r * 1.12,
                      th=cu, phase=math.pi, spt=48),
                 dict(p0=(cx, cy), p1=(cx + kw, cy), turns=1, r=r * 1.12,
                      th=cu, phase=0.0, spt=48)]
    wound_multi(s, lambda: copper(s, (bx0, cy), (bx1, cy), cu), *segs)


def britannia(s, cx, cy, cu=19, bind=9, bound=False, overlap=380, ins=230,
              bounds=None):
    """ব্রিটানিয়া জয়েন্ট — উপর থেকে দেখা।

    মোটা তার হাতে পাকানো যায় না, তাই দুই তার **পাশাপাশি** শুইয়ে (উপর
    থেকে দেখলে একটির নিচে আরেকটি) সরু বাঁধন-তার দিয়ে জড়ানো হয়।  বাঁ
    তারের ডগা উপরে আর ডান তারের ডগা নিচে সমকোণে ভাঁজ — ওই দুই ভাঁজই
    বাঁধনকে সরে যেতে দেয় না।

    আগের ড্রাফটে একটিমাত্র মোটা দণ্ড আঁকা ছিল, অর্থাৎ 'পাশাপাশি দুই
    তার' কথাটাই ছবিতে ছিল না — জয়েন্টের সংজ্ঞাটাই বাদ পড়েছিল।"""
    # দুই তারের কেন্দ্র ১.৫ ব্যাসার্ধ দূরে — ছুঁয়ে থাকলে ছাপায় একটাই
    # মোটা দণ্ড দেখায়, আর 'পাশাপাশি দুই তার' কথাটাই হারিয়ে যায়
    dy = cu * 0.75
    ytop, ybot = cy - dy, cy + dy
    xL, xR = cx - overlap / 2, cx + overlap / 2
    bend = cu * 2.0
    within("ব্রিটানিয়া", xL - ins - 44, xR + ins + 44, bounds)
    insul(s, (xL - ins, ytop), (xL - 40, ytop), cu + 13, INS_K, INS_KE,
          INS_KH, cut=1)
    insul(s, (xR + ins, ybot), (xR + 40, ybot), cu + 13, INS_K, INS_KE,
          INS_KH, cut=1)

    def cores():
        # বাঁ তার:  ডান দিকে গিয়ে ডগা উপরে ভাঁজ
        tube(s, [(xL - 44, ytop), (xR, ytop), (xR, ytop - bend)], cu)
        # ডান তার:  বাঁ দিকে গিয়ে ডগা নিচে ভাঁজ
        tube(s, [(xR + 44, ybot), (xL, ybot), (xL, ybot + bend)], cu)

    if bound:
        # বাঁধন দুটি তারকেই একসঙ্গে জড়ায়, তাই ব্যাসার্ধ লম্বাটে।
        # বাঁধন-তারের মাঝখানটা জয়েন্টের মাঝে বসিয়ে অর্ধেক দিয়ে এক পাশ,
        # বাকি অর্ধেক দিয়ে অন্য পাশ জড়ানো হয় (১১.৫.২) — তাই বাঁ অর্ধেকের
        # পাক ঘোরে উল্টো দিকে, `turns` ঋণাত্মক দিয়ে সেটাই আঁকা
        r = dy + cu * 0.5 + bind * 0.5
        half = max(4, int(round(((xR - bind) - cx) / (bind * PITCH))))
        wound_multi(s, cores,
                    dict(p0=(cx, cy), p1=(xR - bind, cy), turns=half, r=r,
                         th=bind, base=BIND),
                    dict(p0=(xL + bind, cy), p1=(cx, cy), turns=-half, r=r,
                         th=bind, base=BIND))
    else:
        cores()


def pigtail(s, cx, base, height, turns=6, cu=17, spread=112):
    """পিগটেল — দুই তার পাশাপাশি এনে দুই প্রান্ত একসঙ্গে মোচড়।"""
    top = base - height
    for sgn, col in ((-1, (INS_K, INS_KE, INS_KH)),
                     (1, (INS_R, INS_RE, INS_RH))):
        insul(s, (cx + sgn * spread, base + 40), (cx + sgn * 26, base),
              cu + 12, *col, cut=1)
        copper(s, (cx + sgn * 26, base - 2),
               (cx + sgn * cu * 0.55, base - 34), cu)
    twist2(s, (cx, base - 30), (cx, top), turns, cu, r=cu * 0.55)


def married(s, x0, x1, cy, stage, cu=27, n_str=7, st=7, turns=6):
    """ম্যারিড বা টেপার স্প্লাইস — চারটি অবস্থা।

    'গাঁথা' মানে খেই কেবল ছুঁয়ে থাকা নয় — এক কেবলের প্রতিটি খেই অন্য
    কেবলের দুই খেইয়ের **ফাঁকে** ঢুকে যায়।  তাই খ ধাপে মাঝখানে ১৪টি খেই
    পাশাপাশি সমান্তরাল, এক-একটি এক-এক দিক থেকে (হালকা/গাঢ় ছোপে আলাদা)।

    জড়ানোর সময় এক পাশের খেইগুলো **একসঙ্গে, গোছা ধরে** ঘোরানো হয় —
    একটিমাত্র মোটা তার নয়।  তাই তিনটি সমান্তরাল হেলিক্স (তিন খেই),
    আর ব্যাসার্ধ বাইরের দিকে কমে আসে;  ওই ক্রমশ-সরু হওয়াই 'টেপার'
    নামের কারণ।"""
    ins = (x1 - x0) * 0.19
    insul(s, (x0, cy), (x0 + ins, cy), cu + 12, INS_K, INS_KE, INS_KH, cut=1)
    insul(s, (x1, cy), (x1 - ins, cy), cu + 12, INS_K, INS_KE, INS_KH, cut=1)
    lb, rb = x0 + ins - 4, x1 - ins + 4
    mc = (lb + rb) / 2
    LIT = _mix(CU, CU_HL, 0.36)
    core_th = cu * 0.60
    W = turns * st * 3 * PITCH               # তিন খেইয়ের গোছা
    if W > (rb - mc) - st:
        raise SystemExit("✗ ম্যারিড জয়েন্টের পাক ইনসুলেশনে উঠে যাচ্ছে "
                         "(%.0f > %.0f)" % (W, (rb - mc) - st))
    tap = lambda t: 1 - 0.55 * t

    def bundle(xa, xb, base, phase, reverse):
        segs = []
        for k in range(3):
            off = k * st * PITCH
            segs.append(dict(p0=(xa + off, cy), p1=(xb + off, cy),
                             turns=turns, r=core_th * 0.5 + st * 0.5,
                             th=st, phase=phase, base=base,
                             taper=(lambda t: tap(1 - t)) if reverse else tap))
        return segs

    if stage == 1:                            # খেই ছড়ানো
        strands(s, (lb, cy), (mc - 34, cy), n_str, cu * 1.7, st)
        strands(s, (rb, cy), (mc + 34, cy), n_str, cu * 1.7, st)
    elif stage == 2:                          # খেই পরস্পরের ফাঁকে গাঁথা
        w = (rb - lb) * 0.18
        pitch = st * 1.32
        for i in range(n_str):
            for src, dst, col, k in ((lb, mc + w, CU, 0),
                                     (rb, mc - w, LIT, 1)):
                yy = cy + (2 * i + k - (n_str - 0.5)) * pitch
                fan = src + (dst - src) * 0.42
                tube(s, [(src, cy), (fan, yy), (dst, yy)], st, col, CU_SH,
                     CU_HL, bands=3, record=False)
    elif stage == 3:                          # এক পাশ জড়ানো
        wound_multi(
            s,
            lambda: (copper(s, (lb, cy), (rb, cy), core_th),
                     strands(s, (lb, cy), (mc + 40, cy), n_str, cu * 1.15,
                             st)),
            *bundle(mc, mc + W, CU, 0.0, False))
    else:                                     # সম্পূর্ণ
        wound_multi(
            s, lambda: copper(s, (lb, cy), (rb, cy), core_th),
            *(bundle(mc, mc + W, CU, 0.0, False)
              + bundle(mc - W, mc, LIT, 0.0, True)))


def fixture_joint(s, cx, cy, folded, big=23, small=11, turns=7, ins=120,
                  bounds=None):
    """ফিক্সচার জয়েন্ট — অসম মোটা দুই তার।

    ঝাড়বাতির সরু তার মোটা তারের গায়ে কয়েক পাক জড়ানো হয়, তারপর **মোটা
    তারের ডগা পেছনে ভাঁজ করে** ওই পাকের উপর চেপে দেওয়া হয় — তাতে সরু
    তারটি আর পিছলে বেরোতে পারে না।  আগের ড্রাফটে দুই তার সমান মোটা ছিল,
    অথচ অসম মাপই এই জয়েন্টের একমাত্র কারণ।"""
    W = turns * small * PITCH
    r = big * 0.5 + small * 0.5
    xw0, xw1 = cx - W / 2, cx + W / 2
    xe = xw1 + big * 0.75                    # মোটা তামার ডগা
    xa = xw0 - big * 1.6                     # মোটা তারের ইনসুলেশন শেষ
    within("ফিক্সচার", xa - ins, xe + ins + 40, bounds)
    insul(s, (xa - ins, cy), (xa, cy), big + 15, INS_K, INS_KE, INS_KH, cut=1)
    _lead(s, (xe + ins + 40, cy - r), (xe + 40, cy - r), (xw1, cy - r),
          small + 11, small, (INS_R, INS_RE, INS_RH))
    wound(s, (xw0, cy), (xw1, cy),
          lambda: copper(s, (xa - 4, cy), (xe, cy), big),
          turns=turns, r=r, th=small, phase=math.pi)
    if folded:
        # মোটা তারের ডগা উপর দিয়ে ফিরে এসে পাকের উপর চেপে বসে
        tube(s, [(xe - big * 0.34, cy), (xe + big * 0.44, cy - big * 0.06),
                 (xe + big * 0.50, cy - r - small * 0.60),
                 (xe - big * 0.24, cy - r - small * 1.12),
                 (xw0 - small * 0.6, cy - r - small * 1.12)], big * 0.78)


# ═══════════════════════════════════════════════════════════════════════
def d01_steps():
    """একটি আদর্শ জয়েন্টের পাঁচটি ধাপ।"""
    s = SVG(1240, 760)
    s.title("আদর্শ জয়েন্ট তৈরির পাঁচটি ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 16)
    steps = [
        ("স্কিনিং", "ছুরি বা স্ট্রিপার দিয়ে তারের ইনসুলেশন তুলে ফেলা"),
        ("স্ক্র্যাপিং", "খেই থেকে অক্সাইড ও ময়লা চেঁছে তামা ঝকঝকে করা"),
        ("টাইয়িং", "নিয়ম মেনে দুই তার পাকিয়ে জয়েন্ট বাঁধা"),
        ("সোল্ডারিং", "গলিত সোল্ডার ঢুকিয়ে জয়েন্ট স্থায়ী করা"),
        ("টেপিং", "ইনসুলেশন টেপ পেঁচিয়ে জয়েন্ট ঢেকে দেওয়া"),
    ]
    BW, BH, GX, GY = 356, 196, 30, 36
    x0 = (1240 - (3 * BW + 2 * GX)) / 2
    bottom = step_cards(s, steps, x0, 138, BW, BH, GX, GY, 3, ar)
    ry = 138 + BH
    s.path("M %.0f %.0f L %.0f %.0f L %.0f %.0f L %.0f %.0f"
           % (x0 + 2 * (BW + GX) + BW / 2, ry + 6,
              x0 + 2 * (BW + GX) + BW / 2, ry + GY / 2,
              x0 + BW / 2, ry + GY / 2, x0 + BW / 2, ry + GY - 6),
           STEEL, 3.2, marker=ar)
    y = note_strip(s, bottom + 32,
                   "পাঁচটি ধাপের একটিও বাদ দেওয়া চলবে না — স্ক্র্যাপিং ছাড়া "
                   "সোল্ডার ধরে না, টেপিং ছাড়া জয়েন্ট বিপজ্জনক")
    s.fit(y, 24)
    return s.save("%s/d01_steps.svg" % OUT)


def d02_skinning():
    """স্কিনিংয়ের সঠিক ও ভুল পদ্ধতি।

    **২০২৬-০৮-২৫-এ নতুন করে আঁকা।**  আগের ছবিতে তিনটি গোলমাল ছিল:
    ছুরির ফলা নিছক একটা ত্রিভুজ, তাই খাড়া ধরলে ছুঁচের মতো দেখাত;  'সঠিক'
    প্যানেলে ছিলে-ওঠা ইনসুলেশনটা ফলার গায়ে একটা বাঁকা আঁচড়ের মতো
    পড়েছিল;  আর সবচেয়ে বড় কথা — যে **খাঁজ** নিয়ে গোটা ছবিটা, সেই খাঁজ
    আঁকাই ছিল না, কেবল একটা লাল বৃত্ত আর সতর্ক-চিহ্ন বসানো ছিল।

    এখন ফলা তারের গায়ে প্রায় শুয়ে (সঠিক) বা খাড়া হয়ে (ভুল) বসে।
    সঠিক প্যানেলে হাতল **বাঁ দিকে** — ছুরি ডান দিকে ঠেলা হচ্ছে, আর
    ইনসুলেশনের ফালি ডগার সামনে কুণ্ডলী পাকিয়ে উঠছে;  তাতে ফলা আর ফালি
    দুই দিকে থাকে, একটার উপর আরেকটা পড়ে না।

    খাঁজটা ২৪ px তামায় আঁকলে ছাপায় ১ মিমিও হতো না, তাই নিচে বিবর্ধক —
    দুই প্যানেলে একই মাপে, একদিকে মসৃণ তামা আর অন্যদিকে কাটা খাঁজ ও তা
    থেকে নামা ফাটল।"""
    s = SVG(1240, 760)
    s.title("স্কিনিং — ছুরি ধরার সঠিক ও ভুল কোণ", T_TITLE)
    PW, PH = 560, 472
    cy = 96 + 62 + 208
    INS_TH, CU_TH = 40, 24
    MR = 58                                   # বিবর্ধকের ব্যাসার্ধ

    for px, col, head, ok in ((46, GREEN, "সঠিক — পেনসিল ছোলার মতো", True),
                              (634, RED, "ভুল — তারের সঙ্গে সমকোণে", False)):
        panel(s, px, 96, PW, PH, head, col)
        wx0, wx1 = px + 30, px + PW - 30
        edge = px + 262                       # ইনসুলেশন যেখানে শেষ
        xn = px + 368                          # ভুল প্যানেলে ফলা যেখানে বসে
        tx = edge + 62                    # ঢালু মুখ যেখানে শেষ
        insul(s, (wx0, cy), (edge, cy), INS_TH, cut=(None if ok else 1))
        copper(s, (tx - 8 if ok else edge - 5, cy), (wx1, cy), CU_TH)

        if ok:
            # 'পেনসিল ছোলার মতো' কথাটা ছবিতেই দেখানো — ইনসুলেশনের মুখ
            # লম্বা ঢাল হয়ে তামার মাপে নেমেছে, ঠিক ছোলা পেনসিলের মতো।
            # আগে এখানে কুণ্ডলী-পাকানো একটা ফালি আঁকা ছিল;  রেখায় আঁকা
            # কুণ্ডলী তারের পাশে ঝোলা আঁকশির মতো দেখাত, আর ফলার সঙ্গে
            # তার কোনো যোগও চোখে পড়ত না।  ঢালটা যথেষ্ট লম্বা না হলে
            # আবার কলার বা আংটির মতো দেখায় — তাই ৬২ px।
            s.poly([(edge - 3, cy - INS_TH * 0.5), (tx, cy - CU_TH * 0.5 - 1),
                    (tx, cy + CU_TH * 0.5 + 1), (edge - 3, cy + INS_TH * 0.5)],
                   INS_K, INS_KE, 2.4)
            # নলের গায়ের মতোই আলো-ছায়া, নইলে ঢালটা চ্যাপ্টা তাপ্পি লাগে
            s.path("M %.1f %.1f L %.1f %.1f"
                   % (edge + 3, cy - INS_TH * 0.30, tx - 5, cy - CU_TH * 0.34),
                   INS_KH, 4.2, opacity=0.55)
            s.path("M %.1f %.1f L %.1f %.1f"
                   % (edge + 3, cy + INS_TH * 0.33, tx - 4, cy + CU_TH * 0.30),
                   INS_KE, 5.0, opacity=0.75)
            # ফলা ঢালের গায়ে প্রায় শুয়ে, ধার নিচে, হাতল ইনসুলেশনের উপরে
            knife(s, (tx - 3, cy - CU_TH * 0.5 - 2), -172, blade=104, bol=11,
                  handle=109, spine=1, h=25)
        else:
            knife(s, (xn, cy + CU_TH * 0.08), -82, blade=92, bol=10,
                  handle=97, spine=1, h=23)
            notch(s, xn, cy, CU_TH)

        # নিচে বিবর্ধক — তামার গা দুই অবস্থায়, একই মাপে
        mx, my = px + 424, cy + 78

        def inner(ok=ok, mx=mx, my=my):
            big = CU_TH * 2.1
            # ১০টি ব্যান্ড — ৬টিতে এত মোটা নলে ছায়ার ধাপ চোখে পড়ে
            tube(s, [(mx - MR - 16, my), (mx + MR + 16, my)], big,
                 CU, CU_SH, CU_HL, bands=14)
            if not ok:
                notch(s, mx, my, big, bg="#FFFFFF")

        magnifier(s, mx, my, MR, inner,
                  src=(tx + 46 if ok else xn, cy + CU_TH * 0.5),
                  ring=GREEN if ok else RED)
        s.box_auto(mx, my + MR + 10, "খেই অক্ষত" if ok else "খাঁজ পড়েছে",
                   T_SMALL, fill=GREENBG if ok else REDBG,
                   stroke=GREEN if ok else RED,
                   tcolor=GREEN if ok else RED, pad_x=16, pad_y=7)

    y = note_strip(s, 96 + PH + 22,
                   "যতটুকু ইনসুলেশন তোলা হবে তার পুরোটাই জয়েন্টের ভেতরে "
                   "ঢুকবে — বাইরে খালি তামা থাকা চলবে না")
    s.fit(y, 24)
    return s.save("%s/d02_skinning.svg" % OUT)


def d03_types():
    """জয়েন্টের শ্রেণিবিভাগ।"""
    s = SVG(1240, 800)
    s.title("বৈদ্যুতিক তারের জয়েন্টের শ্রেণিবিভাগ", T_TITLE)

    RW, RH = 420, 76
    rx = (1240 - RW) / 2
    s.rect(rx, 108, RW, RH, NAVY, NAVY, 2, 12)
    s.text(620, 108 + 50, "তারের জয়েন্ট ও স্প্লাইস", T_HEAD,
           "#FFFFFF", 700, "middle")

    groups = [
        ("সোজা বা স্ট্রেইট জয়েন্ট", STEEL,
         ["ওয়েস্টার্ন ইউনিয়ন জয়েন্ট", "ব্রিটানিয়া জয়েন্ট",
          "ম্যারিড বা টেপার জয়েন্ট", "স্লিভ জয়েন্ট"]),
        ("শাখা বা ট্যাপ জয়েন্ট", GREEN,
         ["টি বা ট্যাপ জয়েন্ট", "ক্রস জয়েন্ট", "নটেড ট্যাপ জয়েন্ট",
          "বহু-খেই তারের টি জয়েন্ট"]),
        ("প্রান্তিক বা টার্মিনাল জয়েন্ট", AMBER,
         ["পিগটেল বা র‍্যাট-টেইল", "ফিক্সচার জয়েন্ট",
          "লাগ বা সকেট সংযোগ", "কানেক্টর ও কাপলার"]),
    ]
    GW, GAP, gx0, ytop = 372, 16, 46, 250
    s.path("M 620 %d L 620 %d" % (108 + RH, ytop - 38), STEEL, 3)
    for i, (name, col, items) in enumerate(groups):
        x = gx0 + i * (GW + GAP)
        cx = x + GW / 2
        s.path("M %.0f %d L %.0f %d" % (cx, ytop - 38, cx, ytop), STEEL, 3)
        if i != 1:
            s.path("M %.0f %d L %.0f %d" % (min(cx, 620), ytop - 38,
                                            max(cx, 620), ytop - 38), STEEL, 3)
        s.rect(x, ytop, GW, 72, col, col, 2, 11)
        lines = tw_wrap(name, GW - 40, T_BODY, 700)
        for j, ln in enumerate(lines):
            s.text(cx, ytop + (46 if len(lines) == 1
                               else 33 + j * T_BODY * 1.34),
                   ln, T_BODY, "#FFFFFF", 700, "middle")
        by = ytop + 84
        s.rect(x, by, GW, 250, "#F7FAFC", LINE, 1.8, 11)
        yy = by + 48
        for it in items:
            wr = tw_wrap(it, GW - 70, T_SMALL, 400)
            s.circle(x + 32, yy - 8, 7, col)
            for k, ln in enumerate(wr):
                s.text(x + 54, yy + k * T_SMALL * 1.3, ln, T_SMALL,
                       "#28323C", 400)
            yy += 56 if len(wr) == 1 else 84
    y = note_strip(s, ytop + 84 + 250 + 30,
                   "একক খেইয়ের (solid) তারে যে জয়েন্ট চলে, বহু খেইয়ের "
                   "(stranded) তারে তা হুবহু চলে না")
    s.fit(y, 24)
    return s.save("%s/d03_types.svg" % OUT)


def d04_wu():
    """ওয়েস্টার্ন ইউনিয়ন জয়েন্ট — তিন ধাপ ও সম্পূর্ণ রূপ।

    আগে এখানে একটি আসল আলোকচিত্র ছিল;  ফোকাসের বাইরে তোলা বলে ছাপায়
    প্যাঁচ বোঝাই যেত না, তাই বাদ (মডিউল-ডকস্ট্রিং দ্রষ্টব্য)।  ওই
    জায়গায় এখন নিচের চওড়া প্যানেলে সম্পূর্ণ জয়েন্টটাই বড় করে আঁকা —
    দুই প্রান্তের পাঁচটি করে পাক আর মাঝের দুই মোচড় আলাদা করে গোনা যায়।"""
    s = SVG(1240, 860)
    s.title("ওয়েস্টার্ন ইউনিয়ন জয়েন্ট", T_TITLE)
    PW, PH = 372, 286
    cy = 96 + 62 + 108
    heads = ("ক — দুই তার আড়াআড়ি", "খ — মাঝে দুই পরস্পর-পাক",
             "গ — দুই প্রান্তে পাঁচ পাক")
    cu = 15
    for i, head in enumerate(heads):
        x = 46 + i * (PW + 16)
        cx = x + PW / 2
        panel(s, x, 96, PW, PH, head, GREEN if i == 2 else STEEL)
        if i == 0:
            # দুই তার **দুই দিক** থেকে এসে খালি অংশে আড়াআড়ি — একই দিক
            # থেকে আঁকলে ছবিটাই ভুল হয়ে যায়
            for sgn, col in ((-1, (INS_K, INS_KE, INS_KH)),
                             (1, (INS_R, INS_RE, INS_RH))):
                a = math.radians(21 * sgn)
                ux, uy = math.cos(a), math.sin(a)
                within("ওয়েস্টার্ন ইউনিয়ন ধাপ ক",
                       cx - ux * 168 - (cu + 15) * 0.5,
                       cx + ux * 128 + (cu + 15) * 0.5, (x + 6, x + PW - 6))
                ip = (cx - ux * 168, cy - uy * 168 - sgn * 26)
                cp = (cx - ux * 66, cy - uy * 66 - sgn * 26)
                tp = (cx + ux * 128, cy + uy * 128 - sgn * 26)
                _lead(s, ip, cp, tp, cu + 15, cu, col)
        elif i == 1:
            r = cu * 0.52
            Wm = 2 * cu * TPITCH
            ml, mr = cx - Wm / 2, cx + Wm / 2
            # শাঙ্ক দুই পাশ থেকে এসে মোচড়ে ঢোকে, ডগা দুটো এখনো মুক্ত
            # লিডের বাইরের মুখ প্যানেলের ভেতরে থাকতে হবে — স্ট্রোকের
            # গোল মাথা আরও (cu+15)/2 px বাড়ায়, প্রথম ড্রাফটে সেটাই
            # হিসাবের বাইরে ছিল আর লাল তারটা প্যানেল কেটে বেরিয়ে যেত
            within("ওয়েস্টার্ন ইউনিয়ন ধাপ খ", ml - 120 - (cu + 15) * 0.5,
                   mr + 120 + (cu + 15) * 0.5, (x + 6, x + PW - 6))
            _lead(s, (ml - 120, cy + r), (ml - 62, cy + r), (ml, cy + r),
                  cu + 15, cu, (INS_K, INS_KE, INS_KH))
            _lead(s, (mr + 120, cy - r), (mr + 62, cy - r), (mr, cy - r),
                  cu + 15, cu, (INS_R, INS_RE, INS_RH))
            copper(s, (mr, cy + r), (mr + 92, cy + 78), cu)
            copper(s, (ml, cy - r), (ml - 92, cy - 78), cu)
            twist2(s, (ml, cy), (mr, cy), 2, cu, r=r)
        else:
            wu_joint(s, cx, cy, cu=cu, mid_turns=2, end_turns=5, ins=28,
                     bounds=(x + 22, x + PW - 22))

    yb = 96 + PH + 20
    panel(s, 46, yb, 1148, 208, "সম্পূর্ণ জয়েন্ট", NAVY)
    wu_joint(s, 620, yb + 62 + 70, cu=30, mid_turns=2, end_turns=5,
             ins=210, bounds=(70, 1170))
    y = note_strip(s, yb + 208 + 22,
                   "দৈর্ঘ্য বাড়ানোর সবচেয়ে প্রচলিত জয়েন্ট — টান পড়লে "
                   "জয়েন্টের আগে তারই ছেঁড়ে")
    s.fit(y, 24)
    return s.save("%s/d04_wu.svg" % OUT)


def d05_wu_ties():
    """লং টাই ও শর্ট টাই।

    তফাত কেবল **মাঝের পরস্পর-পাকের দৈর্ঘ্য** — প্রান্তের জড়ানো পাক
    দুটোতেই পাঁচটি করে।  দুই প্যানেল পাশাপাশি, একই মাপে;  তুলনার ছবি
    পাশাপাশি রাখলেই চোখ তফাতটা ধরে, আর লাল বন্ধনী মাঝের অংশটা দাগিয়ে
    দেয়।  (আগে দুটি প্যানেল একটির নিচে আরেকটি ছিল — তাতে চিত্রটা ৭.৩
    সেমি লম্বা হয়ে যেত আর পরের অনুচ্ছেদের ছবির জায়গা থাকত না।)"""
    s = SVG(1240, 480)
    s.title("ওয়েস্টার্ন ইউনিয়ন জয়েন্টের দুই ধরন", T_TITLE)
    PW, PH = 560, 168

    def sheet(px, head, col, mid_turns):
        panel(s, px, 96, PW, PH, head, col)
        cy = 96 + 62 + 46
        ml, mr, _, _ = wu_joint(s, px + PW / 2, cy, cu=16,
                                mid_turns=mid_turns, end_turns=5, ins=42,
                                bounds=(px + 20, px + PW - 20))
        by = cy + 44
        s.path("M %.1f %d L %.1f %d L %.1f %d L %.1f %d"
               % (ml, by - 11, ml, by, mr, by, mr, by - 11), RED, 3.2)

    sheet(46, "লং টাই — মাঝের পাক লম্বা", STEEL, 6)
    sheet(634, "শর্ট টাই — মাঝের পাক ছোট", GREEN, 2)
    y = note_strip(s, 96 + PH + 22,
                   "লং টাইয়ে সোল্ডার ভেতরে ভালো ঢোকে, শর্ট টাই জায়গা কম "
                   "নেয় — কন্ডুইটের ভেতরে সুবিধা")
    s.fit(y, 24)
    return s.save("%s/d05_wu_ties.svg" % OUT)


def d09_britannia():
    """ব্রিটানিয়া জয়েন্ট — বাঁধনের আগে ও পরে।

    দুটি প্যানেলই পুরো চওড়ায়, একটির নিচে আরেকটি:  জয়েন্টটা লম্বা ও
    সরু, পাশাপাশি বসালে দৈর্ঘ্য পেত না আর ভাঁজ করা ডগা দুটো কাছাকাছি
    এসে পড়ত।"""
    s = SVG(1240, 620)
    s.title("ব্রিটানিয়া জয়েন্ট", T_TITLE)
    PW, PH = 1148, 196
    for k, (bound, head, col) in enumerate((
            (False, "ধাপ ১ — দুই তার পাশাপাশি, ডগা সমকোণে ভাঁজ", STEEL),
            (True, "ধাপ ২ — সরু বাঁধন-তার মাঝ থেকে দুই দিকে", GREEN))):
        py = 96 + k * (PH + 20)
        panel(s, 46, py, PW, PH, head, col)
        britannia(s, 620, py + 62 + 66, cu=20, bind=10, bound=bound,
                  overlap=420, ins=180, bounds=(70, 1170))
    y = note_strip(s, 96 + 2 * (PH + 20) + 2,
                   "মোটা তার পাকানো যায় না বলে পাশাপাশি রেখে সরু বাঁধন-তার "
                   "দিয়ে জড়ানো হয়")
    s.fit(y, 24)
    return s.save("%s/d09_britannia.svg" % OUT)


def d10_married():
    """ম্যারিড বা টেপার জয়েন্ট — চার ধাপ।"""
    s = SVG(1240, 720)
    s.title("ম্যারিড জয়েন্ট — বহু খেইয়ের তারের স্প্লাইস", T_TITLE)
    PW, PH = 560, 216
    heads = ["ক — খেই ছড়ানো", "খ — খেই পরস্পরের ফাঁকে গাঁথা",
             "গ — এক পাশ জড়ানো", "ঘ — সম্পূর্ণ জয়েন্ট"]
    for i, head in enumerate(heads):
        r, c = divmod(i, 2)
        x = 46 + c * (PW + 28)
        y = 96 + r * (PH + 22)
        panel(s, x, y, PW, PH, head, STEEL if i < 3 else GREEN)
        married(s, x + 26, x + PW - 26, y + 62 + 76, i + 1)
    y = note_strip(s, 96 + 2 * PH + 22 + 22,
                   "প্রতিটি খেই আলাদা করে ছড়িয়ে, চিরুনির দাঁতের মতো গেঁথে "
                   "তবেই জড়াতে হয়")
    s.fit(y, 24)
    return s.save("%s/d10_married.svg" % OUT)


def d07_tee():
    """টি বা ট্যাপ জয়েন্ট — সাধারণ, নটেড ও বহু-খেই।

    তৃতীয় প্যানেলটি ১১.৬.১-এর শেষ বাক্যের ছবি:  বহু খেইয়ের তারে শাখার
    খেইগুলোকে **দুই ভাগ করে দুই দিকে** আলাদাভাবে জড়াতে হয়।"""
    s = SVG(1240, 700)
    s.title("টি বা ট্যাপ জয়েন্ট", T_TITLE)
    PW, PH = 560, 234
    cy = 96 + 62 + 32
    for i, (head, kn, col) in enumerate((
            ("সাধারণ ট্যাপ", False, STEEL),
            ("নটেড ট্যাপ — টান পড়ার জায়গায়", True, GREEN))):
        x = 46 + i * (PW + 28)
        panel(s, x, 96, PW, PH, head, col)
        tap_joint(s, x + PW / 2, cy, cu=18, turns=6, knot=kn, drop=112,
                  ins=96, tail=52, bounds=(x + 22, x + PW - 22),
                  ybounds=(96 + 62, 96 + PH - 6))

    yb = 96 + PH + 20
    PH2 = 230
    panel(s, 46, yb, 1148, PH2, "বহু খেইয়ের তারে ট্যাপ — খেই দুই ভাগ",
          NAVY)
    cy2 = yb + 62 + 40
    cu, st = 22, 7
    W = 5 * st * 3 * PITCH
    bx0, bx1 = 620 - W - 190, 620 + W + 190
    r = cu * 0.5 + st * 0.5
    _lead(s, (bx0 - 130, cy2), (bx0, cy2), (bx0 + 6, cy2), cu + 15, cu,
          (INS_K, INS_KE, INS_KH))
    _lead(s, (bx1 + 130, cy2), (bx1, cy2), (bx1 - 6, cy2), cu + 15, cu,
          (INS_K, INS_KE, INS_KH))
    insul(s, (620, cy2 + 100), (620, cy2 + 54), cu + 11, INS_R, INS_RE,
          INS_RH, cut=1)
    if cy2 + 100 + (cu + 11) * 0.5 + 6 > yb + PH2:
        raise SystemExit("✗ বহু-খেই ট্যাপের শাখা প্যানেল ছাপিয়ে গেছে")
    segs = []
    for k in range(3):
        off = k * st * PITCH
        # শাখার খেই দুই ভাগ — অর্ধেক বাঁ দিকে, অর্ধেক ডান দিকে
        segs.append(dict(p0=(620 + off, cy2), p1=(620 + W + off, cy2),
                         turns=5, r=r, th=st, phase=0.0))
        segs.append(dict(p0=(620 - W - off, cy2), p1=(620 - off, cy2),
                         turns=5, r=r, th=st, phase=0.0))

    def core():
        copper(s, (bx0, cy2), (bx1, cy2), cu)
        for sgn in (-1, 1):
            for k in range(3):
                tube(s, [(620 + sgn * (k * 3 - 3), cy2 + 56),
                         (620 + sgn * (16 + k * 6), cy2 + 30),
                         (620 + sgn * (r + k * st * PITCH), cy2 + r * 0.35)],
                     st, CU, CU_SH, CU_HL, bands=3, record=False)

    wound_multi(s, core, *segs)
    y = note_strip(s, yb + PH2 + 22,
                   "মূল লাইন না কেটে শাখা নেওয়ার জয়েন্ট — টান পড়ার জায়গায় "
                   "নট দিতে হয়")
    s.fit(y, 24)
    return s.save("%s/d07_tee.svg" % OUT)


def d08_cross():
    """ক্রস জয়েন্ট — একই বিন্দু থেকে **দুটি** শাখা।"""
    s = SVG(1240, 600)
    s.title("ক্রস বা দ্বি-শাখা জয়েন্ট", T_TITLE)
    PW, PH = 560, 344
    cy = 96 + 62 + 141
    for i, (head, kn) in enumerate((("সাধারণ ক্রস জয়েন্ট", False),
                                    ("নট দেওয়া ক্রস জয়েন্ট", True))):
        x = 46 + i * (PW + 28)
        panel(s, x, 96, PW, PH, head, GREEN if kn else STEEL)
        cross_joint(s, x + PW / 2, cy, cu=18, turns=5, knot=kn, reach=118,
                    ins=76, tail=40, bounds=(x + 22, x + PW - 22),
                    ybounds=(96 + 62, 96 + PH - 6))
    y = note_strip(s, 96 + PH + 22,
                   "একই বিন্দু থেকে দুই দিকে শাখা — দুই পাশে সমান পাক দিতে "
                   "হয়")
    s.fit(y, 24)
    return s.save("%s/d08_cross.svg" % OUT)


def d06_pigtail():
    """পিগটেল বা র‍্যাট-টেইল জয়েন্ট — দুটি আসল ছবি ও আঁকা রূপ।

    এই দুটি আলোকচিত্র ঝকঝকে (৭৩০০×১০৯৬০ পিক্সেলের মূল ফাইল থেকে কাটা),
    তাই থাকল।"""
    s = SVG(1240, 560)
    s.title("পিগটেল বা র‍্যাট-টেইল জয়েন্ট", T_TITLE)
    PW, PH = 372, 300
    img_panel(s, 46, 96, PW, PH, "আসল ছবি — বক্সে তিনটি জোড়া",
              "%s/ph_pig_real.jpg" % IMG, GREEN)
    img_panel(s, 46 + PW + 16, 96, PW, PH, "উপরে কানেক্টর ক্যাপ",
              "%s/ph_pig_nut.jpg" % IMG, GREEN)
    x = 46 + 2 * (PW + 16)
    panel(s, x, 96, PW, PH, "আঁকা রূপ", STEEL)
    pigtail(s, x + PW / 2, 96 + PH - 58, 158, turns=6, cu=17, spread=112)
    y = note_strip(s, 96 + PH + 22,
                   "জংশন বা আউটলেট বক্সের ভেতরে চলে — টান পড়ে এমন জায়গায় নয়")
    s.fit(y, 24)
    return s.save("%s/d06_pigtail.svg" % OUT)


def d11_fixture():
    """ফিক্সচার জয়েন্ট ও স্তম্ভিত জয়েন্ট।"""
    s = SVG(1240, 660)
    s.title("ফিক্সচার জয়েন্ট ও স্তম্ভিত (staggered) জয়েন্ট", T_TITLE)
    PW, PH = 560, 190
    cy = 96 + 62 + 62
    for i, (head, fold) in enumerate((("১ — সরু তার মোটা তারে জড়ানো", False),
                                      ("২ — মোটা তারের ডগা ভাঁজ", True))):
        x = 46 + i * (PW + 28)
        panel(s, x, 96, PW, PH, head, STEEL)
        fixture_joint(s, x + PW / 2 - 24, cy, folded=fold, big=25, small=12,
                      turns=7, ins=104, bounds=(x + 22, x + PW - 22))

    yb = 96 + PH + 20
    PH2 = 224
    panel(s, 46, yb, 1148, PH2, "যমজ তারে স্তম্ভিত জয়েন্ট", GREEN)
    a, b = 92, 1148
    cy2 = yb + 62 + 78
    dy, cu = 42, 15
    f1, f2 = 0.36, 0.66
    # চ্যাপ্টা যমজ তারের খোলস — দুই কোর ভেতরে, তাই বাইরের রেখাটা
    # দুই কোরকে ঘিরে থাকা লম্বাটে চাকতি
    sh = dy + 20                              # খোলসের অর্ধ-উচ্চতা
    for xs, xe in ((a, a + 250), (b - 250, b)):
        s.rect(xs, cy2 - sh, xe - xs, 2 * sh, SHEATH, SHEATH_E, 2.4, 18)
        s.rect(xs + 12, cy2 - sh + 7, xe - xs - 24, 9, SHEATH_H, "none", 0, 4)
        # ভেতরের দুই কোরের জায়গা — খোলসেই হালকা খাঁজ পড়ে
        s.path("M %.0f %.0f L %.0f %.0f" % (xs + 10, cy2, xe - 10, cy2),
               _mix(SHEATH, SHEATH_E, 0.55), 2.2)
    for k, (sgn, col) in enumerate(((-1, (INS_R, INS_RE, INS_RH)),
                                    (1, (INS_K, INS_KE, INS_KH)))):
        yy = cy2 + sgn * dy
        jc = a + (b - a) * (f1 if k == 0 else f2)
        Wt = 4 * cu * TPITCH
        insul(s, (a + 248, yy), (jc - Wt / 2 - 34, yy), cu + 11, *col, cut=1)
        insul(s, (b - 248, yy), (jc + Wt / 2 + 34, yy), cu + 11, *col, cut=1)
        copper(s, (jc - Wt / 2 - 38, yy), (jc + Wt / 2 + 38, yy), cu)
        twist2(s, (jc - Wt / 2, yy), (jc + Wt / 2, yy), 4, cu, r=cu * 0.52)
    j1, j2 = a + (b - a) * f1, a + (b - a) * f2
    for jx in (j1, j2):
        s.path("M %.1f %d L %.1f %d" % (jx, cy2 - dy - 34, jx, cy2 + dy + 34),
               RED, 2.6, dash="8 6")
    s.path("M %.1f %d L %.1f %d" % (j1, cy2, j2, cy2), RED, 3.2)
    y = note_strip(s, yb + PH2 + 22,
                   "ঝাড়বাতির সরু তার মোটা তারে জোড়ার সময় ফিক্সচার জয়েন্ট; "
                   "যমজ তারের জয়েন্ট মুখোমুখি নয়")
    s.fit(y, 24)
    return s.save("%s/d11_fixture.svg" % OUT)


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    """লেবেল ও তার লিডার — লেখা সবসময় ছবির বাইরে, লিডার লেখার যে ধারে
    লক্ষ্যবস্তু সেই ধার থেকে বেরোয় (অধ্যায় ১০-এর শিক্ষা)।"""
    w = tw(text, size, 700)
    x0 = x - w if anchor == "end" else (x - w / 2 if anchor == "middle" else x)
    x1 = x0 + w
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    if tx < x0 - 6:
        start = (x0 - 10, y)
    elif tx > x1 + 6:
        start = (x1 + 10, y)
    else:
        start = ((x0 + x1) / 2, y + (size * 0.55 if ty > y else -size * 0.9))
    s.path("M %.1f %.1f L %.1f %.1f" % (start[0], start[1], tx, ty), STEEL, 2.6)
    s.circle(tx, ty, 6, STEEL)


def d12_solder_tools():
    """সোল্ডারিংয়ের সরঞ্জাম পরিচিতি।"""
    s = SVG(1240, 820)
    s.title("সোল্ডারিং আয়রন ও সোল্ডার তার", T_TITLE)
    IX, IY, IW = 160, 246, 920
    IH = IW * 639 / 1600
    s.rect(IX - 12, IY - 12, IW + 24, IH + 24, "#FCFDFE", LINE, 1.8, 12)
    s.image(IX, IY, IW, IH, "%s/ph_solder_iron.jpg" % IMG, 6)

    callout(s, 300, 180, "সোল্ডার তারের রোল", IX + 0.16 * IW,
            IY + 0.52 * IH, "middle")
    callout(s, 748, 180, "হ্যান্ডল", IX + 0.60 * IW, IY + 0.33 * IH, "middle")
    callout(s, 1120, 180, "সাপ্লাই কর্ড ও প্লাগ", IX + 0.86 * IW,
            IY + 0.12 * IH, "end")
    callout(s, 300, IY + IH + 70, "বিট বা টিপ", IX + 0.21 * IW,
            IY + 0.92 * IH, "middle")
    callout(s, 800, IY + IH + 70, "হিটিং এলিমেন্টসহ ব্যারেল",
            IX + 0.345 * IW, IY + 0.705 * IH, "middle")

    y = note_strip(s, IY + IH + 118,
                   "ঘরোয়া ওয়্যারিংয়ের জয়েন্টে ৬০–১০০ ওয়াটের আয়রন আর "
                   "রজন-কোর সোল্ডার তার ব্যবহার হয়")
    s.fit(y, 24)
    return s.save("%s/d12_solder_tools.svg" % OUT)


def d13_solder_steps():
    """সোল্ডারিংয়ের ধাপ।"""
    s = SVG(1240, 780)
    s.title("সোল্ডারিং করার ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 16)
    steps = [
        ("জয়েন্ট পরিষ্কার", "তেল, ময়লা ও অক্সাইড তুলে তামা ঝকঝকে করা"),
        ("ফ্লাক্স লাগানো", "জয়েন্টে রজন বা সোল্ডারিং পেস্ট মাখানো"),
        ("আয়রন গরম", "সোল্ডার সহজে গলা পর্যন্ত বিট গরম হতে দেওয়া"),
        ("বিট টিনিং", "গরম বিটে সামান্য সোল্ডার ধরিয়ে চকচকে আবরণ দেওয়া"),
        ("সোল্ডার প্রয়োগ", "বিট জয়েন্টে চেপে ধরে সোল্ডার জয়েন্টে গলানো"),
        ("ঠান্ডা করা", "নড়াচড়া না করে ঠান্ডা হতে দেওয়া, তারপর টেপ লাগানো"),
    ]
    BW, BH, GX, GY = 356, 196, 30, 36
    x0 = (1240 - (3 * BW + 2 * GX)) / 2
    bottom = step_cards(s, steps, x0, 138, BW, BH, GX, GY, 3, ar)
    ry = 138 + BH
    s.path("M %.0f %.0f L %.0f %.0f L %.0f %.0f L %.0f %.0f"
           % (x0 + 2 * (BW + GX) + BW / 2, ry + 6,
              x0 + 2 * (BW + GX) + BW / 2, ry + GY / 2,
              x0 + BW / 2, ry + GY / 2, x0 + BW / 2, ry + GY - 6),
           STEEL, 3.2, marker=ar)
    y = note_strip(s, bottom + 32,
                   "সোল্ডার গলবে জয়েন্টের তাপে — বিটের গায়ে গলিয়ে ফোঁটা "
                   "ফেললে ঠান্ডা জোড়া (dry joint) হয়",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save("%s/d13_solder_steps.svg" % OUT)


def d14_taping():
    """টেপিং পদ্ধতি।

    আগে টেপ আঁকা হতো চ্যাপ্টা কালো পাখনা দিয়ে — দেখাত চিরুনির মতো।
    টেপও তো তারের গায়ে জড়ানো, কাজেই ওটাও হেলিক্স;  কেবল সুতোর বদলে
    চওড়া ফিতে।  হাফ-ল্যাপ মানে প্রতি পাক আগেরটির অর্ধেক ঢাকে, অর্থাৎ
    পিচ = ফিতের চওড়ার অর্ধেক — পাকসংখ্যা সেখান থেকেই হিসাব করা।"""
    s = SVG(1240, 740)
    s.title("জয়েন্টে টেপ পেঁচানোর নিয়ম", T_TITLE)
    PW, PH = 372, 214
    cases = [("১ — শুরু", 0.24), ("২ — হাফ-ল্যাপ", 0.66), ("৩ — শেষ", 1.0)]
    cy = 96 + 62 + 66
    band, cu = 27, 15
    for i, (head, frac) in enumerate(cases):
        x = 46 + i * (PW + 16)
        panel(s, x, 96, PW, PH, head, STEEL if frac < 1 else GREEN)
        wx0, wx1 = x + 26, x + PW - 26
        t0, t1 = wx0 + 42, wx1 - 42
        te = t0 + (t1 - t0) * frac
        mc = (wx0 + wx1) / 2

        def joint():
            insul(s, (wx0, cy), (wx0 + 86, cy), cu + 13, cut=1)
            insul(s, (wx1, cy), (wx1 - 86, cy), cu + 13, cut=1)
            copper(s, (wx0 + 82, cy), (wx1 - 82, cy), cu)
            twist2(s, (mc - 46, cy), (mc + 46, cy), 4, cu, r=cu * 0.52)

        turns = max(1, int(round((te - t0) / (band * 0.5))))
        wound(s, (t0, cy), (te, cy), joint, turns=turns, r=cu * 0.92,
              th=band, base=TAPE, edge=TAPE_E, hi=TAPE_H, bands=2)

    yb = 96 + PH + 22
    bullets = [
        "টেপ শুরু ও শেষ হবে তারের ইনসুলেশনের উপরে, অন্তত ২৫ মিমি ছাড়িয়ে;",
        "প্রতিটি পাক আগের পাকের অর্ধেক ঢেকে দেবে — একেই হাফ-ল্যাপ বলে;",
        "টেপ হালকা টান দিয়ে পেঁচাতে হবে, ঢিলা টেপ খুলে যায়;",
        "টেপের মোট পুরুত্ব তারের নিজস্ব ইনসুলেশনের চেয়ে কম হবে না।",
    ]
    s.rect(46, yb, 1148, 196, "#F7FAFC", LINE, 1.8, 12)
    yy = yb + 50
    for bt in bullets:
        s.circle(78, yy - 8, 7, STEEL)
        s.text(102, yy, bt, T_BODY, "#28323C")
        yy += 44
    y = note_strip(s, yb + 216,
                   "টেপ IEC 60454-3-1 অনুযায়ী পিভিসি হতে হবে; কাপড়ের ফিতা "
                   "বা কাগজের টেপ চলবে না")
    s.fit(y, 24)
    return s.save("%s/d14_taping.svg" % OUT)


def d15_modern():
    """আধুনিক সংযোগ-সামগ্রী।"""
    s = SVG(1240, 620)
    s.title("আধুনিক সংযোগ-সামগ্রী", T_TITLE)
    PW, PH = 560, 356
    img_panel(s, 46, 96, PW, PH, "টুইস্ট-অন কানেক্টর (ওয়্যার নাট)",
              "%s/ph_wire_nuts.jpg" % IMG, STEEL)
    img_panel(s, 634, 96, PW, PH, "লিভার-টাইপ কানেক্টর",
              "%s/ph_lever_conn.jpg" % IMG, GREEN)
    y = note_strip(s, 96 + PH + 22,
                   "বক্সের ভেতরে পাকানো জয়েন্টের বদলে অনুমোদিত কানেক্টরও "
                   "ব্যবহার করা যায়")
    s.fit(y, 24)
    return s.save("%s/d15_modern.svg" % OUT)


ALL = [d01_steps, d02_skinning, d03_types, d04_wu, d05_wu_ties, d06_pigtail,
       d07_tee, d08_cross, d09_britannia, d10_married, d11_fixture,
       d12_solder_tools, d13_solder_steps, d14_taping, d15_modern]

if __name__ == "__main__":
    import svgkit as K
    os.makedirs(OUT, exist_ok=True)
    K.COLLECT = True
    for f in ALL:
        try:
            f()
        except Exception as e:
            print("  (collect)", f.__name__, e)
    K.COLLECT = False
    K.flush()
    for f in ALL:
        print("✓", os.path.relpath(f()))
