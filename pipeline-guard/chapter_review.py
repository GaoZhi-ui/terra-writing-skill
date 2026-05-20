#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""python _review.py <章节文件>"""

import re, sys
from pathlib import Path

CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')

def review(fp):
    text = Path(fp).read_text(encoding='utf-8')
    parts = text.split('---')
    body = parts[0]
    diary = parts[1] if len(parts) > 1 else ''
    issues = []

    cjk = len(CJK.findall(body))
    if cjk < 2000:
        issues.append(f"字数{cjk}(需2000+)")
    
    stops = body.count(chr(12290))
    if cjk > 0:
        d = stops / cjk * 100
        if d > 6:
            issues.append(f"句号{d:.1f}/百字")

    ptn = r'不是[^。。，；！？]*是[^。。，；！？]*[。。，；！？]'
    n = len(list(re.finditer(ptn, body)))
    if n >= 2:
        issues.append(f"句式重复{n}次")

    dcjk = len(CJK.findall(diary))
    if dcjk > 0:
        has_fact = bool(re.search(r'(天|到了|找到|遇到|发现)', diary))
        has_obs = bool(re.search(r'(看到|注意到|发现|想起)', diary))
        if not has_fact or not has_obs:
            m = []
            if not has_fact: m.append('缺事实')
            if not has_obs: m.append('缺观察')
            issues.append(f"日记{''.join(m)}")
    elif dcjk < 20:
        issues.append("日记过短")

    if issues:
        print(f"{Path(fp).name}: {'; '.join(issues)}")
    else:
        print(f"{Path(fp).name}: OK")

if __name__ == '__main__':
    review(sys.argv[1])
