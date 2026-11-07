# README（本工作区宪法）

> 本文件为「宪法」：AI 不得私自改动。首次确认日期：____。底层根逻辑与安全规范见 README1ST.md。
> 改动本文件任何内容前，必须先向用户提出并获**二次确认**。

## 0. 版本与根信任
- 当前版本：v1.0 ｜ 首次确认日期：____
- 底层根逻辑快照：README1ST.md（永不删除，须本地备份于沙箱之外）
- 首创：[LeoLee](https://s.iee.li/l/u1)

## 1. 目录结构与命名规则
（引用 whitepaper 第三节模板 + 第七节命名规范；核心文件名全部英文，禁止改回中文）

```
leo/
├── README.md / README1ST.md / memory.md / memory-index.md / file-tree.md
├── vault/（敏感目录，不进文件树）→ secrets.md
├── code/ → gen-filetree.py / vault_crypto.py
├── pan/ → imga/ video/ audio/ document/
└── log-YYYY.MM.DD-YYYY.MM.DD.md
```

## 2. 平台规则与合规
（目标 agent 平台的使用条款、AI 行为限制、合规要求——由适配层填写）

## 3. 沙箱能力配置（来自适配层接口表）
- 持久根目录：____
- 会话自动读取：____ ｜ 定时任务：____ ｜ 沙箱私密性：____（私密 / 可分享）
- 文件交付通道：____ ｜ 网络出网：____（全通 / 白名单 / 不通）

## 4. 标准工作流程
（引用 whitepaper 第五节约五步闭环 + 第六节气生命周期）
存文件 → 执行任务 → 更新索引与文件树 → 记录日志 → 大变动打包

## 5. 文件命名规则
（引用 whitepaper 第七节；默认 `日期_时间戳_三位随机数.扩展名`，文件名主体优先 ASCII）

## 6. 安全规范
（引用 whitepaper 第八节；加密保险库开关状态：开 / 关；安全分级：私密 / 可分享）

## 7. AI 行为约定
- 会话初始化读：README + memory.md 热缓存 + memory-index.md（按需定点读）
- 任务收尾做：更新索引/文件树 + 写 log-*.md
- 诚实/止损原则：____

## 8. 变更记录
- v1.0 ____ 首次确认生效（同步派生 README1ST.md）
