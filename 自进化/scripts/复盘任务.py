#!/usr/bin/env python3
"""
复盘任务脚本（Task Reflection Script）
功能：任务完成后自动执行复盘流程
用法：python 复盘任务.py --任务描述 "xxx" --完成状态 "完全/部分/未完成"
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 路径配置
SCRIPT_DIR = Path(__file__).parent
MEMORY_FILE = Path("../../MEMORY.md")  # 相对于 scripts 目录
SKILL_REFLECTION_TEMPLATE = SCRIPT_DIR / "references" / "反思模板.md"
SKILL_EXPERIENCE_TEMPLATE = SCRIPT_DIR / "references" / "经验固化模板.md"


def load_template(template_path: Path) -> str:
    """加载模板文件"""
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()
    return ""


def generate_reflection_prompt(task_description: str, completion_status: str) -> str:
    """生成复盘引导提示"""
    prompt = f"""
## 任务复盘

**任务描述**：{task_description}
**完成状态**：{completion_status}

请基于上述任务，完成以下复盘：

### 1. 任务目标达成情况
- 原始目标：
- 最终结果：
- 达成度评估：[100%/80-99%/50-79%/<50%]

### 2. 执行过程回顾
请描述采取的关键行动和关键决策点。

### 3. 遇到的问题与解决方案
如果有遇到问题，请描述问题和解决方式。

### 4. 可改进的点
- 立即可改进：
- 需要长期改进：

### 5. 学到的新知识/技能
- 新认知：
- 新技能：
- 新注意事项：

### 6. 经验提取
请判断哪些经验值得固化，并说明理由。
"""
    return prompt


def save_to_memory(reflection_content: str, task_type: str):
    """保存复盘内容到 MEMORY.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    entry = f"""
---
## 复盘记录 [{timestamp}]

**任务类型**：{task_type}
**复盘内容**：
{reflection_content}
"""
    
    # 追加到 MEMORY.md
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "# MEMORY\n\n"
    
    # 在「关键任务」章节后插入复盘记录
    if "## 关键任务" in content:
        content = content.replace("## 关键任务", f"## 关键任务{entry}")
    else:
        content += entry
    
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 复盘记录已保存到 {MEMORY_FILE}")


def create_experience_entry(task_type: str, key_learning: str) -> str:
    """创建经验条目"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    return f"""
### {timestamp} - {task_type}任务经验
**核心学习**：{key_learning}
"""


def main(task_description: str, completion_status: str = "完全完成", task_type: str = "一般"):
    """主函数"""
    print("=" * 50)
    print("🔄 灵女自进化 - 复盘任务")
    print("=" * 50)
    
    # 1. 生成复盘提示
    prompt = generate_reflection_prompt(task_description, completion_status)
    print("\n📋 请根据以下提示完成复盘：")
    print(prompt)
    
    # 2. 这里可以集成 LLM API 自动生成复盘
    # 暂时输出提示，等待手动填写
    
    # 3. 保存到 MEMORY.md
    reflection_content = input("\n📝 请粘贴复盘内容（或按回车跳过）: ")
    if reflection_content.strip():
        save_to_memory(reflection_content, task_type)
    
    print("\n✨ 复盘任务完成！")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="灵女自进化 - 复盘任务")
    parser.add_argument("--任务描述", "-t", required=True, help="任务描述")
    parser.add_argument("--完成状态", "-s", default="完全完成", 
                        choices=["完全完成", "部分完成", "未完成"],
                        help="任务完成状态")
    parser.add_argument("--任务类型", "-y", default="一般",
                        help="任务类型")
    
    args = parser.parse_args()
    main(args.任务描述, args.完成状态, args.任务类型)
