#!/usr/bin/env python3
"""
记忆整理脚本（Memory Organization Script）
功能：定期整理记忆文件，保持结构清晰
用法：python 记忆整理.py [--mode full|quick]
"""

import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# 路径配置
SCRIPT_DIR = Path(__file__).parent
MEMORY_DIR = Path("../../..")  # 根目录
MEMORY_FILE = MEMORY_DIR / "MEMORY.md"
SKILL_DIR = MEMORY_DIR / "技能"
GROWTH_DIR = MEMORY_DIR / "能力成长"

# 各记忆文件路径
MEMORY_FILES = {
    "MEMORY": MEMORY_DIR / "MEMORY.md",
    "SOUL": MEMORY_DIR / "SOUL.md",
    "USER": MEMORY_DIR / "USER.md",
    "SECRET": MEMORY_DIR / "SECRET.md",
}


def analyze_memory_file(filepath: Path) -> dict:
    """分析记忆文件状态"""
    if not filepath.exists():
        return {"exists": False}
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("\n")
    
    return {
        "exists": True,
        "path": filepath,
        "size_bytes": filepath.stat().st_size,
        "size_kb": filepath.stat().st_size / 1024,
        "lines": len(lines),
        "sections": extract_sections(content),
        "last_modified": datetime.fromtimestamp(filepath.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def extract_sections(content: str) -> list:
    """提取文档中的章节结构"""
    sections = []
    for line in content.split("\n"):
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title = line.lstrip("#").strip()
            sections.append({"level": level, "title": title})
    return sections


def identify_memory_categories(content: str) -> dict:
    """识别记忆内容分类"""
    categories = defaultdict(list)
    
    # 关键词匹配
    patterns = {
        "用户偏好": [r"偏好", r"喜欢", r"不喜欢", r"希望"],
        "任务经验": [r"任务", r"项目", r"工作"],
        "技术技能": [r"技能", r"工具", r"方法"],
        "注意事项": [r"注意", r"避免", r"规范"],
        "日程安排": [r"日程", r"计划", r"安排"],
    }
    
    for category, keywords in patterns.items():
        for keyword in keywords:
            if re.search(keyword, content):
                categories[category].append(keyword)
    
    return dict(categories)


def generate_memory_summary(memory_info: dict) -> str:
    """生成记忆文件摘要"""
    summary = f"""
## 记忆文件状态报告

**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### {memory_info['path'].name}

| 属性 | 值 |
|------|-----|
| 存在状态 | {'✅ 存在' if memory_info['exists'] else '❌ 不存在'} |
| 文件大小 | {memory_info.get('size_kb', 0):.2f} KB |
| 行数 | {memory_info.get('lines', 0)} |
| 最后修改 | {memory_info.get('last_modified', '未知')} |
"""
    
    if memory_info.get("sections"):
        summary += "\n**章节结构**：\n"
        for section in memory_info["sections"][:10]:  # 只显示前10个
            indent = "  " * (section["level"] - 1)
            summary += f"{indent}- {section['title']}\n"
    
    if memory_info.get("categories"):
        summary += "\n**内容分类**：\n"
        for cat, keywords in memory_info["categories"].items():
            summary += f"- {cat}: {', '.join(set(keywords))}\n"
    
    return summary


def detect_duplicates(content: str) -> list:
    """检测重复内容"""
    duplicates = []
    lines = content.split("\n")
    
    # 简单检测连续重复行
    seen = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) > 10:  # 只检测有意义的行
            if line in seen:
                duplicates.append({
                    "line": i + 1,
                    "content": line[:50],
                    "first_appearance": seen[line]
                })
            else:
                seen[line] = i + 1
    
    return duplicates


def organize_memory_file(filepath: Path) -> str:
    """整理单个记忆文件"""
    if not filepath.exists():
        return f"❌ 文件不存在：{filepath}"
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    issues = []
    
    # 检测问题
    duplicates = detect_duplicates(content)
    if duplicates:
        issues.append(f"发现 {len(duplicates)} 处可能重复的内容")
    
    # 章节检查
    sections = extract_sections(content)
    if not sections:
        issues.append("文件缺少章节结构")
    
    # 生成报告
    report = f"\n{'='*40}\n"
    report += f"📁 {filepath.name}\n"
    report += f"{'='*40}\n"
    
    if issues:
        report += "⚠️ 发现问题：\n"
        for issue in issues:
            report += f"  - {issue}\n"
    else:
        report += "✅ 未发现问题\n"
    
    report += f"\n章节数量：{len(sections)}\n"
    report += f"文件大小：{len(content)} 字符\n"
    
    return report


def quick_scan() -> str:
    """快速扫描所有记忆文件"""
    report = """
╔═══════════════════════════════════════════════════════════╗
║           灵女记忆系统 - 快速扫描报告                      ║
╚═══════════════════════════════════════════════════════════╝
"""
    report += f"\n扫描时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    total_size = 0
    total_files = 0
    
    for name, filepath in MEMORY_FILES.items():
        info = analyze_memory_file(filepath)
        status = "✅" if info["exists"] else "❌"
        size = info.get("size_kb", 0)
        lines = info.get("lines", 0)
        
        report += f"\n{status} {name}: {size:.2f} KB ({lines} 行)\n"
        
        if info["exists"]:
            total_size += size
            total_files += 1
    
    report += f"\n总占用：{total_size:.2f} KB（{total_files}/{len(MEMORY_FILES)} 文件）\n"
    
    # 检查能力成长目录
    if GROWTH_DIR.exists():
        growth_files = list(GROWTH_DIR.rglob("*.md"))
        report += f"\n📊 能力成长记录：{len(growth_files)} 个文件\n"
    
    # 检查技能目录
    if SKILL_DIR.exists():
        skill_files = list(SKILL_DIR.rglob("SKILL.md"))
        report += f"\n🛠️ 已安装技能：{len(skill_files)} 个\n"
    
    return report


def full_organize() -> str:
    """完整整理记忆系统"""
    report = """
╔═══════════════════════════════════════════════════════════╗
║           灵女记忆系统 - 完整整理报告                      ║
╚═══════════════════════════════════════════════════════════╝
"""
    
    report += f"\n整理时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    # 分析所有记忆文件
    for name, filepath in MEMORY_FILES.items():
        info = analyze_memory_file(filepath)
        if info["exists"]:
            info["categories"] = identify_memory_categories(
                open(filepath, "r", encoding="utf-8").read()
            )
        summary = generate_memory_summary(info)
        report += summary
    
    # 建议部分
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 整理建议：

1. **定期归档**：将过期的复盘记录移动到归档目录
2. **经验库维护**：定期审查经验库，淘汰过时内容
3. **技能更新**：当发现新的工具使用技巧时，及时更新 TOOLS.md
4. **记忆同步**：确保各记忆文件之间的信息一致性

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report


def main(mode: str = "quick"):
    """主函数"""
    print("🔄 灵女自进化 - 记忆整理")
    print("=" * 50)
    
    if mode == "quick":
        report = quick_scan()
    else:
        report = full_organize()
    
    print(report)
    
    # 保存报告
    report_file = GROWTH_DIR / "记忆整理报告" / f"报告_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 报告已保存到：{report_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="灵女自进化 - 记忆整理")
    parser.add_argument("--mode", "-m", default="quick",
                        choices=["quick", "full"],
                        help="整理模式：quick(快速扫描) / full(完整整理)")
    
    args = parser.parse_args()
    main(args.mode)
