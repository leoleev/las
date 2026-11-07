#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scaffold.py - 一键搭建 Leo Agent 记忆系统工作区骨架

用法：
    python3 scaffold.py [目标路径]
    目标路径 默认为当前目录下的 ./leo
    （也可用 --root . 直接在当前目录初始化）

行为：
    1. 创建目录结构（leo/ 下各子目录）
    2. 从 skill 的 assets/templates 拷入空模板（README/memory/memory-index/log）
    3. 从 assets/code 拷入 gen-filetree.py / vault_crypto.py 到 code/
    4. 运行 gen-filetree.py 生成 file-tree.md
    5. 打印后续步骤（重点：首版 README 必须二次确认后才落盘）

注意：本脚本只搭骨架与空模板。首版 README.md 需由 AI 融合平台规则与沙箱配置、
完整展示给用户并获二次确认后才写入（详见 whitepaper 第四节 / SKILL.md 第五节）。
"""
import argparse
import os
import shutil
import subprocess
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(SKILL_ROOT, "assets", "templates")
CODE_SRC = os.path.join(SKILL_ROOT, "assets", "code")

# 工作区内要创建的目录
SUBDIRS = [
    "vault",
    "code",
    "pan/imga",
    "pan/video",
    "pan/audio",
    "pan/document",
]

TEMPLATE_FILES = {
    "README.template.md": "README.md",
    "memory.template.md": "memory.md",
    "memory-index.template.md": "memory-index.md",
    "log.template.md": "log-2026.01.01-2026.12.31.template.md",
}

CODE_FILES = ["gen-filetree.py", "vault_crypto.py"]


def main():
    ap = argparse.ArgumentParser(description="Leo Agent 记忆系统工作区脚手架")
    ap.add_argument("target", nargs="?", default=None, help="目标工作区路径（默认 ./leo）")
    ap.add_argument("--root", action="store_true", help="直接在目标路径初始化（不建 leo 子目录）")
    args = ap.parse_args()

    if args.target:
        target = os.path.abspath(args.target)
    else:
        target = os.path.join(os.getcwd(), "leo")

    # 决定根：--root 时 target 即根；否则在其下建 leo/
    root = target if args.root else target

    if os.path.exists(root) and os.listdir(root):
        print(f"[警告] 目标目录非空：{root}")
        print("         继续将向其中添加缺失的文件/目录（不覆盖已存在的 README/memory 等）。")
    os.makedirs(root, exist_ok=True)

    # 1. 创建子目录
    for sub in SUBDIRS:
        os.makedirs(os.path.join(root, sub), exist_ok=True)
    # vault 占位说明（不写敏感内容）
    vault_readme = os.path.join(root, "vault", "README.md")
    if not os.path.exists(vault_readme):
        with open(vault_readme, "w", encoding="utf-8") as f:
            f.write("# vault/（敏感目录）\n\n本目录不进公开文件树（gen-filetree.py 自动隐藏）。\n"
                    "仅存放 secrets.md（密码/密钥/Token）；启用加密保险库后只存密文。\n")

    # 2. 拷贝模板
    for src_name, dst_name in TEMPLATE_FILES.items():
        src = os.path.join(TEMPLATES, src_name)
        dst = os.path.join(root, dst_name)
        if not os.path.exists(dst):
            shutil.copyfile(src, dst)
            print(f"[拷贝] {dst_name}")
        else:
            print(f"[跳过] {dst_name}（已存在）")

    # 3. 拷贝代码
    for cf in CODE_FILES:
        src = os.path.join(CODE_SRC, cf)
        dst = os.path.join(root, "code", cf)
        if not os.path.exists(dst):
            shutil.copyfile(src, dst)
            print(f"[拷贝] code/{cf}")
        else:
            print(f"[跳过] code/{cf}（已存在）")

    # 4. 生成文件树
    try:
        subprocess.run([sys.executable, os.path.join(root, "code", "gen-filetree.py")],
                       check=True)
    except Exception as e:
        print(f"[提示] 生成文件树失败：{e}（可稍后手动运行 code/gen-filetree.py）")

    # 5. 后续步骤
    print("\n========== 骨架搭建完成 ==========")
    print(f"工作区根：{root}")
    print("\n后续步骤（重要）：")
    print("1. 由 AI 融合「内核规则 + 平台规则 + 沙箱能力配置」草拟首版 README.md")
    print("2. 完整展示给用户，列明安全规范与根逻辑要点")
    print("3. 获用户【二次确认】后，才将 README.md 落盘")
    print("4. 同时派生 README1ST.md（逐字副本），并提示用户本地（沙箱外）备份")
    print("5. 写一条初始 log-*.md、按索引登记 memory-index.md")
    print("6. 需要时启用加密保险库（默认关闭，需额外二次确认）")
    print("\n详细设计见 skill 内 references/whitepaper.md")


if __name__ == "__main__":
    main()
