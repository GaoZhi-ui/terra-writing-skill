---
name: pipeline-guard
description: 自动化流水线安全守卫。三步保护写作交付链：filter → 合并前过滤临时/草稿文件；scan → 外发前扫描禁用词（现实世界地名不准出现在虚构世界）；clean → 完成后清理临时文件。防止"深圳来的？"串入泰拉世界这类事故。
metadata:
  openclaw:
    emoji: 🛡️
triggers:
  - 合并章节
  - 发送章节
  - 发前检查
  - 内容审核
  - 清理临时文件
---

# pipeline-guard — 自动化流水线安全守卫

## 三个子命令

### 1. filter — 合并前过滤

排除文件类型：`_tmp_*`（草稿）、`*_锚点*`（锚点）、`*_场景卡*`、`*_评分卡*`、`_*`（临时文件）

```bash
python3 guard.py filter <目录> <glob模式> [--expect-one] [-v]
```

### 2. scan — 外发前内容审核

检查现实世界地名：深圳、北京、上海、中国、地球、美国、日本等。命中即中断。

```bash
python3 guard.py scan <文件路径> [--terms-file <文件>] [--context <标签>] [-v]
```

### 3. clean — 完成后清理

清理临时文件：`_tmp_*`、`_*.py`、`_*_chunk.txt` 等。

```bash
python3 guard.py clean <目录> [--patterns <模式>] [-v]
```

## 使用场景

| 步骤 | guard 命令 |
|------|-----------|
| 草稿清理 | `guard.py clean chapters/` |
| 文件合并 | `guard.py filter chapters/ "第*章*.md"` |
| 发前审核 | `guard.py scan merged.docx` |

## 事故教训

多步骤自动化流水线中，「输出→转换→外发」环节需要两重防护：
1. **文件过滤**：只取正文文件，排除草稿/锚点/场景卡
2. **内容审核**：发前扫描现实世界禁用词，命中即中断

## 禁用词列表

默认禁用：深圳、北京、上海、广州、成都、重庆、武汉、南京、杭州、中国、地球、美国、日本、英国、法国、德国、俄罗斯、韩国、America、Japan、China、England、France、Germany、Russia

可通过 `--terms-file` 扩展。
