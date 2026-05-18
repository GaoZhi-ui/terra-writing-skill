# Terra Writing Skill — 泰拉写作工作流

一个完整的中文长篇小说创作 skill，专为《泰拉拾遗录》打磨，但适用于任何需要严谨结构化写作的项目。

## 核心能力

- **6阶段写作流程**：写前分析→写作→自检→文笔润色→修订→元数据输出
- **流水线安全守卫**：过滤草稿、审核禁用词、清理临时文件
- **章节交付链**：MD合并 → docx转换 → 邮件发送 → 云盘同步
- **状态追踪**：时间线、伏笔、角色状态持续追踪

## 快速开始

通过 ClawHub 安装：

```bash
openclaw skills install terra-writing-skill
```

或手动克隆：

```bash
git clone https://github.com/<你的用户名>/terra-writing-skill.git
cd terra-writing-skill
```

## 目录结构

```
terra-writing-skill/
├── SKILL.md                    # 主入口 — 完整6阶段写作流程
├── README.md                   # 本文件
├── LICENSE
├── pipeline-guard/
│   ├── SKILL.md                # 流水线安全守卫
│   └── guard.py                # filter / scan / clean 三个子命令
└── references/
    └── 写作流程完整参考.md       # 全流程参考文档
```

## 写作工作流

### 阶段1：写前分析
7项检查：沈默的不适、不适推进、工具触发、时间线、角色状态、伏笔清单、连续性约束

### 阶段2：写作
v3风格准则：2500字基线、留白优先、日记体（事实+观察+画面）、萨卡兹式对话、地震信息用短句

### 阶段3：自检
12项双检：
- 逻辑层：时间线/空间/情绪/不重复/人物/伏笔/物品
- 文笔层：对话标签/五感/精简/日记/价值

### 阶段3.5：文笔润色
人物润色 / 语言优化 / 氛围强化

### 阶段4：修订
标记→重写→重新自检直至通过

### 阶段5：章末元数据输出
结构化摘要 → 锚点文件 → 伏笔/时间线/角色持续追踪

## 流水线守卫

```bash
# 合并前过滤草稿
python3 guard.py filter chapters/ "第*章*.md"

# 发前审核禁用词（防跨世界串词）
python3 guard.py scan merged.docx

# 写后清理临时文件
python3 guard.py clean chapters/
```

## 许可证

Apache-2.0
