#!/usr/bin/env python3
"""
scan_tree.py - 扫描项目目录，生成树结构 Markdown 文档
用法：python scan_tree.py --root /path/to/project [--output out.md] [--ignore node_modules,...] [--max-depth 5]
"""
import os
import argparse
from datetime import date
from pathlib import Path

DEFAULT_IGNORE = {
    'node_modules', '__pycache__', '.git', '.idea', '.vscode',
    'dist', 'build', '.DS_Store', '*.pyc', 'target', '.mvn',
    'venv', '.venv', 'env', '.env', 'coverage', '.nyc_output',
}

EMOJI_MAP = {
    # 目录
    'db': '🗄️ ',
    'database': '🗄️ ',
    'model': '📦 ',
    'models': '📦 ',
    'entity': '📦 ',
    'util': '🔧 ',
    'utils': '🔧 ',
    'common': '🔧 ',
    'config': '⚙️ ',
    'test': '🧪 ',
    'tests': '🧪 ',
    'doc': '📝 ',
    'docs': '📝 ',
    'api': '🌐 ',
    'task': '🚀 ',
    'tasks': '🚀 ',
    'service': '🎯 ',
    'services': '🎯 ',
    'script': '📜 ',
    'scripts': '📜 ',
}


def should_ignore(name: str, ignore_set: set) -> bool:
    if name in ignore_set:
        return True
    for pattern in ignore_set:
        if pattern.startswith('*') and name.endswith(pattern[1:]):
            return True
    return False


def build_tree(root: Path, ignore_set: set, max_depth: int, current_depth: int = 0) -> list[str]:
    if current_depth > max_depth:
        return ['    ' * current_depth + '└── ... (超出最大深度)']

    try:
        entries = sorted(root.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        return []

    entries = [e for e in entries if not should_ignore(e.name, ignore_set)]
    lines = []
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = '└── ' if is_last else '├── '
        indent = '    ' * current_depth

        if entry.is_dir():
            emoji = EMOJI_MAP.get(entry.name.lower(), '📂 ')
            lines.append(f"{indent}{connector}{emoji}{entry.name}/")
            child_indent = '    ' if is_last else '│   '
            sub_lines = build_tree(entry, ignore_set, max_depth, current_depth + 1)
            lines.extend([f"{indent}{child_indent[:-1] if child_indent == '    ' else child_indent}{l.lstrip()}" 
                          if not l.startswith(indent + child_indent) else l 
                          for l in sub_lines])
        else:
            lines.append(f"{indent}{connector}{entry.name}")

    return lines


def build_tree_v2(root: Path, ignore_set: set, max_depth: int) -> list[str]:
    """简洁版：标准树形输出"""
    result = []

    def _walk(path: Path, prefix: str, depth: int):
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
        except PermissionError:
            return
        entries = [e for e in entries if not should_ignore(e.name, ignore_set)]

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = '└── ' if is_last else '├── '
            extension = '    ' if is_last else '│   '

            if entry.is_dir():
                emoji = EMOJI_MAP.get(entry.name.lower(), '📂 ')
                result.append(f"{prefix}{connector}{emoji}{entry.name}/")
                _walk(entry, prefix + extension, depth + 1)
            else:
                result.append(f"{prefix}{connector}{entry.name}")

    _walk(root, '', 0)
    return result


def main():
    parser = argparse.ArgumentParser(description='生成项目树结构 Markdown 文档')
    parser.add_argument('--root', required=True, help='项目根目录路径')
    parser.add_argument('--output', default='project_tree.md', help='输出文件路径')
    parser.add_argument('--ignore', default='', help='忽略的目录/文件（逗号分隔）')
    parser.add_argument('--max-depth', type=int, default=5, help='最大扫描深度（默认5）')
    parser.add_argument('--project-name', default='', help='项目名称（默认用目录名）')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"错误：路径不存在 {root}")
        return

    ignore_set = DEFAULT_IGNORE.copy()
    if args.ignore:
        ignore_set.update(args.ignore.split(','))

    project_name = args.project_name or root.name
    tree_lines = build_tree_v2(root, ignore_set, args.max_depth)

    md_lines = [
        f"# {project_name} - 目录结构",
        "",
        "> <!-- 请在此处填写项目简介 -->",
        "",
        f"**生成时间**：{date.today()}  ",
        f"**根目录**：`{root}/`",
        "",
        "```",
        f"{root.name}/",
    ]
    md_lines.extend(tree_lines)
    md_lines.append("```")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('\n'.join(md_lines), encoding='utf-8')
    print(f"✅ 已生成：{output}")
    print(f"   共扫描 {len([l for l in tree_lines if '──' in l])} 个条目")


if __name__ == '__main__':
    main()
