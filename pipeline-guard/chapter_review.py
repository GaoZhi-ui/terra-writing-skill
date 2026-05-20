#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chapter_review.py — 章节自动审查脚本（阶段3.3）
用法: python chapter_review.py <章节文件路径>
"""

import re, sys
from pathlib import Path

CJK_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')

def count_cjk(text):
    return len(CJK_RE.findall(text))

def review(filepath):
    fp = Path(filepath)
    text = fp.read_text(encoding='utf-8')
    parts = text.split('---')
    body = parts[0]
    diary = parts[1] if len(parts) > 1 else ''
    
    print("=" * 50)
    print(f"审查章节: {fp.name}")
    print("=" * 50)
    
    issues = []
    
    # 1. 字数
    cjk = count_cjk(body)
    if cjk < 2000:
        print(f"[字数] 不足: 正文{cjk}字 (目标2000+)")
        issues.append("字数不足")
    elif cjk < 2200:
        print(f"[字数] 偏低: 正文{cjk}字 (建议2200-2800)")
    else:
        print(f"[字数] 达标: {cjk}字")
    
    # 2. 句号密度
    stops = body.count(chr(12290))
    if cjk > 0:
        density = stops / cjk * 100
        if density > 6:
            print(f"[密度] 超标: {density:.2f}/百字 ({stops}句号, 目标<=6)")
            issues.append("句号密度超标")
        else:
            print(f"[密度] 达标: {density:.2f}/百字")
    
    # 3. 句式重复（不是A是B）
    pattern = r'不是[^。。，；！？]*是[^。。，；！？]*[。。，；！？]'
    matches = list(re.finditer(pattern, body))
    if len(matches) >= 2:
        print(f"[句式] 重复: '{'不是A是B'}'出现{len(matches)}次")
        issues.append(f"句式重复{len(matches)}次")
    else:
        print(f"[句式] 正常: '{'不是A是B'}'出现{len(matches)}次")
    
    # 4. 日记
    dj_cjk = count_cjk(diary)
    if dj_cjk < 30:
        print(f"[日记] 过短或无: {dj_cjk}字")
    else:
        has_fact = bool(re.search(r'(天|日|走了|到了|找到|遇到|发现)', diary))
        has_obs = bool(re.search(r'(看到|注意到|意识到|发现|知道|想起)', diary))
        missing = []
        if not has_fact: missing.append("事实")
        if not has_obs: missing.append("观察")
        if missing:
            print(f"[日记] 要素缺失: {', '.join(missing)}")
        else:
            print(f"[日记] 三要素齐全 ({dj_cjk}字)")
    
    # 5. 末句钩子
    body_lines = [l.strip() for l in body.split('\n') if l.strip() and not l.startswith('#')]
    if body_lines:
        last = body_lines[-1]
        hooks = ['明天', '下一次', '还会', '不知道', '会回来', '还没', '没开', 
                 '要回答', '要去', '会有的', '还在', '还没放']
        found_hook = [h for h in hooks if h in last]
        if found_hook:
            print(f"[衔接] 末句有钩子: '{'...'+last[-30:]}'")
        else:
            print(f"[衔接] 末句无钩子: '{last[:50]}'")
    
    # 6. 连续性检查
    places = set(re.findall(r'(灰烬平原|盐碱地|龙门|永宁|MC-0729|拾遗|骨架)', body))
    people = set(re.findall(r'(沈默|阿枣|星熊|古籍修复师|陈晖洁|老方|老张|阿远|大壮|刘婶|卫大姐|左林)', body))
    print(f"[连续] 地点: {places if places else '无'}  人物: {people if people else '无'}")
    
    print("=" * 50)
    if issues:
        print(f"发现 {len(issues)} 个问题: {'; '.join(issues)}")
    else:
        print("审查通过")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python chapter_review.py <章节文件>")
        sys.exit(1)
    review(sys.argv[1])
