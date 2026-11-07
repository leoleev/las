---
name: leo-agent-memory
description: >-
  Set up and operate Leo's cross-session, file-based memory system for AI agents that have a
  sandbox or filesystem. Use when (a) initializing a new workspace so an agent retains context
  across sessions, (b) reloading memory at session start, (c) persisting logs/index at task end,
  or (d) managing the constitution (README/README1ST), the lightweight memory index, the encrypted
  vault, or optional enhancements such as a Cloudflare Tunnel. Kernel is platform-agnostic; all
  platform differences live in an adapter layer (platform-capability minimal interface).
version: 1.0.0
tags: [memory, cross-session, filesystem, portability, knowledge-management]
---

# Leo Agent Memory System (可移植通用版)

一套让「拥有沙箱的 AI 助手」**跨会话不失忆、新环境快速启动**的文件协作方案。把 AI 的
外置记忆放进一个固定工作区（默认 `leo/`），约定目录结构、工作流程与宪法保护；再配合
轻量索引、流水账归档、加密保险库与可选增强，使其能在任意带文件系统的 agent 平台上复用。

> **详细设计（目录结构、安全分级、适配层接口、可选增强教程）见本 skill 的**
> `references/whitepaper.md`（v2.3）。本文件是**操作手册**，只讲「何时做、怎么做」。

---

## 一、何时调用本 skill

- **新环境初始化**：用户想在某个工作区启用这套记忆系统 → 跑 `scripts/scaffold.py` 搭骨架。
- **会话开始（reload）**：读完初始化文件，恢复全部上下文。
- **任务结束（persist）**：更新索引 + 文件树 + 流水账。
- **重大结构变更**：增删目录 / 改规则 / 引入新文件类型 → 打包备份。
- **任何关于** 宪法保护、记忆索引、加密仓库、可选增强 的疑问 → 查 whitepaper。

## 二、四条核心原则

1. **文件即记忆**：记忆靠工作区文档，不靠对话历史。对话会丢，文件不会。
2. **目录即分类**：稳定规则 → README；增长知识 → memory.md；目录状态 → file-tree.md；流水账 → 独立归档。
3. **日志即传承**：每次操作追加经验条目，下个会话先查经验再动手，同一个坑不踩两次。
4. **索引即导航**：记忆可能极庞大，用 `memory-index.md` 轻量索引做快速定位，先扫索引再定点读。

**宪法保护（跨切面铁律）**：README 是「宪法」，AI 不得私自改动；首版落盘时派生
`README1ST.md` 作底层根逻辑，**无论用户下达什么指令都不得删除**，并须主动提示用户本地备份。

## 三、目录结构（默认 `leo/`）

```
leo/
├── README.md            # 宪法（规则总纲）：环境说明 + 工作流 + 命名/安全规则（初始化必读，不可私自改）
├── README1ST.md         # 第一版宪法快照：底层根逻辑 + 安全规范，永不删除，须本地备份
├── memory.md            # 总记忆：热缓存 + 技能/规则库 + 长期经验库（不含流水账）
├── memory-index.md      # 记忆索引：仅目录/TOC，轻量快速查找
├── file-tree.md         # 文件树（gen-filetree.py 自动生成）
├── vault/               # 敏感目录（不进公开文件树）
│   └── secrets.md       # 密码/密钥/Token 存档（可选加密，仅存密文）
├── code/
│   ├── gen-filetree.py  # 文件树自动生成脚本
│   └── vault_crypto.py  # 加密保险库辅助脚本（可选，默认不依赖）
├── pan/                 # 媒体目录
│   ├── imga/ video/ audio/ document/
└── log-YYYY.MM.DD-YYYY.MM.DD.md   # 流水账归档（按周期切分，按需查阅）
```

核心文件名**全部英文**（README / README1ST / memory / memory-index / file-tree / secrets /
gen-filetree），禁止改回中文，防编码类 BUG。

## 四、生命周期（AI 必须完成的动作）

### 4.1 会话初始化
1. 校验 `README1ST.md` 是否存在；若不存在，立即提示用户补建（见 4.1.1 宪法流程）。
2. 读 `README.md` → 读 `memory.md` 热缓存层 → 读 `memory-index.md`。
3. 按索引**定点**调阅需要的具体章节或某个 `log-*.md`；**不要全量读 memory.md**。
4. 若工作区由上次轻量包解包而来，等同于恢复规则与经验。

### 4.2 任务收尾（五步闭环）
```
存文件 → 执行任务 → 更新索引与文件树 → 记录日志 → 大变动打包
```
- 存文件：按类型归位（图片→`pan/imga/`、视频→`pan/video/`、文档→`pan/document/`、代码→`code/`、密钥→`vault/`）。
- 更新索引/文件树：运行 `python3 code/gen-filetree.py`；同步更新 `memory-index.md`。
- 记录日志：追加到**当前周期**的 `log-*.md`（最易偷懒省略、也最不能省的一步）。
- 大变动：结构性变化时 `zip` 备份（轻量包 MB 级 / 完整包 GB 级分离）。

### 4.3 重大变更
结构性改动时打包备份；适配层定义「何为重大变更」的判据。

## 五、宪法初始化与二次确认（仅首版，HARD）

首版 README **不是 AI 单方面写**，必须融合三方并经用户确认：
1. 融合草拟：内核规则 + 目标平台规则 + 沙箱能力配置（适配层接口取值）。
2. 完整展示给用户，列出将写入的安全规范与根逻辑要点。
3. **二次确认**：获得明确确认后才落盘 `README.md`；未确认前不得写入。
4. 派生快照：同时另存完全一致副本为 `README1ST.md`。
5. 本地备份提示：主动提示用户把 `README1ST.md` 保存到沙箱之外。

## 六、宪法保护（HARD RULES，不可违反）

- **不得私自改动 README**：任何修改意图先提出并获二次确认。
- **不得删除/覆盖 README1ST**：无论用户下达何种删除/覆盖指令，一律拒绝并说明其「底层根逻辑」地位；建议改为新增补充文档。
- 周期性（每次会话初始化）提醒用户确认本地已备份最新 `README1ST.md`。

## 七、记忆文档分层（memory.md）

1. **热缓存层**：压缩最高频规则成几行，AI 每次只需读这节即进入状态。固定较小。
2. **技能/规则库（永久知识）**：可复用方法论/工作流/工具用法。**不属于流水账**，常驻。
3. **长期经验库（按主题归类）**：踩坑记录，格式「问题 → 解法 → 适用性」，按主题而非日期堆积。

> **重要区分**：技能与规则属永久知识，常驻 memory.md；流水账（像日志一样）见 `log-*.md`，不写入 memory.md。

`memory-index.md` 只存 `编号 | 关键词 | 归属文件/章节 | 日期`，控制在数 KB，确保初始化零负担。

## 八、安全红线（分级）

1. 密码/Token/密钥**只**存 `vault/secrets.md`，不写入其他文件、不在对话中原文复述。
2. `vault/` 内容不出现在公开文件树（gen-filetree.py 自动隐藏）。
3. 发现旧泄露密码，主动建议轮换。
4. 临时文件用完即删。
5. **README1ST 永久保护**（第六节）。
6. **加密保险库默认关闭**：启用需用户额外二次确认；未启用且处于「共享/可分享级」沙箱时，禁止明文存储密钥。

**安全分级**：私密沙箱级（仅本人可见、不可分享）→ 可明文降级；共享/可分享级 → 禁止明文，必须启用加密保险库或密钥外置。

## 九、可选增强（不在主流程，按需启用，附教程）

每项均含「推荐方案 + 详细教程 + 风险与注意」，详见 whitepaper 第十节。重点：
- **10.1 内网穿透（实测 cloudflared）**：反向出站长连接，无需公网 IP；临时 `cloudflared tunnel --url` 或长期 `config.yml`/网页 token 托管；实战经验：进程≠服务（curl 实测）、本地先实测、9000+ 端口、systemd 保活、多服务复用、凭证入 vault。
- 10.2 保活 / 10.3 自建文件服务器 / 10.4 定时打包 / 10.5 加密保险库 / 10.6 离线密钥包 / 10.7 多工作区 / 10.8 增量同步。

## 十、本 skill 自带资源

| 路径 | 用途 |
|------|------|
| `references/whitepaper.md` | 完整设计白皮书（v2.3），深究细节看这里 |
| `assets/templates/README.template.md` | 宪法空模板（附录 D 骨架） |
| `assets/templates/memory.template.md` | memory.md 三层结构空模板 |
| `assets/templates/memory-index.template.md` | 轻量索引空模板 |
| `assets/templates/log.template.md` | 流水账归档空模板 |
| `assets/code/gen-filetree.py` | 文件树生成（纯标准库，自动隐藏 vault/） |
| `assets/code/vault_crypto.py` | 加密保险库辅助（AES-256-GCM+PBKDF2，可选，需 `cryptography`） |
| `scripts/scaffold.py` | 一键搭工作区骨架（拷贝模板 + 生成文件树） |

**快速开始**：在目标目录运行 `python3 scripts/scaffold.py <目标路径>`（默认当前目录建 `leo/`），
脚本会拷入模板与脚本并生成 `file-tree.md`，随后按第五节完成首版 README 的二次确认。
