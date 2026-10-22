#!/usr/bin/env python3
"""Search YouTube (results page) and print videoId | duration | views | channel | title."""
import sys, re, json, urllib.request, urllib.parse

def search(q, n=12):
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": q, "hl": "en"})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    data = json.loads(m.group(1))
    out = []
    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                t = "".join(r.get("text", "") for r in v.get("title", {}).get("runs", []))
                ch = "".join(r.get("text", "") for r in v.get("ownerText", {}).get("runs", []))
                d = v.get("lengthText", {}).get("simpleText", "")
                views = v.get("viewCountText", {}).get("simpleText", "")
                out.append((v["videoId"], d, views, ch, t))
            for x in o.values(): walk(x)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(data)
    return out[:n]

if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("##", q)
        for r in search(q):
            print(" | ".join(r))
