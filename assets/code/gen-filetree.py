#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen-filetree.py - 扫描工作区生成带图标和大小标注的文件树
- 自动隐藏敏感目录（SECRET_DIRS，默认 vault）
- 过滤缓存/临时文件（IGNORE_DIRS / IGNORE_FILES / IGNORE_EXTS）
- 输出到 file-tree.md

移植时只需改两个常量：ROOT（工作区根目录）与 SECRET_DIRS（敏感目录名单）。
默认 ROOT 指向脚本所在目录的上级（即 leo/code/ 的上级 leo/）；作为独立脚本可手动改 ROOT。
"""
import os
import sys
from datetime import datetime

# ===== 只需修改这两个常量 =====
# 默认：脚本在 leo/code/ 下时，上级目录即工作区根 leo/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 若作为独立脚本使用，可改为：ROOT = "/path/to/leo"
SECRET_DIRS = {"vault"}            # 敏感目录（不展开，只留占位符）
# =============================

IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".cache", "tmp"}
IGNORE_FILES = {".DS_Store", "Thumbs.db", "file-tree.md", "memory-index.md"}
IGNORE_EXTS = {".pyc", ".tmp", ".log"}
OUTPUT = os.path.join(ROOT, "file-tree.md")

ICON_DIR = "📁"
ICON_FILE = "📄"
ICON_SECRET = "🔒"


def human_size(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.1f}{unit}" if unit != "B" else f"{num}B"
        num /= 1024
    return f"{num:.1f}PB"


def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and d not in SECRET_DIRS]
        for f in files:
            if f in IGNORE_FILES or os.path.splitext(f)[1].lower() in IGNORE_EXTS:
                continue
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def walk(dir_path, prefix=""):
    lines = []
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return lines
    dirs = [e for e in entries if os.path.isdir(os.path.join(dir_path, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(dir_path, e))]
    items = [(e, True) for e in dirs] + [(e, False) for e in files]
    for idx, (name, is_dir) in enumerate(items):
        last = idx == len(items) - 1
        branch = "└── " if last else "├── "
        full = os.path.join(dir_path, name)
        if is_dir and name in SECRET_DIRS:
            lines.append(f"{prefix}{branch}{ICON_SECRET} {name}/  [敏感目录·已隐藏内容]")
            continue
        if is_dir:
            if name in IGNORE_DIRS:
                continue
            size = dir_size(full)
            lines.append(f"{prefix}{branch}{ICON_DIR} {name}/  ({human_size(size)})")
            ext = "    " if last else "│   "
            lines.extend(walk(full, prefix + ext))
        else:
            if name in IGNORE_FILES or os.path.splitext(name)[1].lower() in IGNORE_EXTS:
                continue
            try:
                size = os.path.getsize(full)
            except OSError:
                size = 0
            lines.append(f"{prefix}{branch}{ICON_FILE} {name}  ({human_size(size)})")
    return lines


def main():
    if not os.path.isdir(ROOT):
        print(f"[错误] 根目录不存在: {ROOT}")
        sys.exit(1)
    lines = [f"# 文件树（自动生成 · {datetime.now():%Y-%m-%d %H:%M}）", "",
             f"{ICON_DIR} ./", ""]
    lines.extend(walk(ROOT))
    content = "\n".join(lines) + "\n"
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[完成] 已生成 {OUTPUT}（{len(lines)} 行）")


if __name__ == "__main__":
    main()
