#!/usr/bin/env python3
"""
经验提取脚本（Experience Extraction Script）
功能：从对话/任务中提取有价值经验
用法：python 经验提取.py --对话内容 "xxx"
"""

import json
import re
from datetime import datetime
from pathlib import Path

# 路径配置
SCRIPT_DIR = Path(__file__).parent
EXPERIENCE_DIR = Path("../../能力成长/经验库")
SKILL_EXPERIENCE_TEMPLATE = SCRIPT_DIR / "references" / "经验固化模板.md"


def extract_patterns_from_dialogue(dialogue: str) -> list:
    """
    从对话中提取潜在经验
    模式识别：
    - 成功解决方案
    - 关键决策点
    - 工具使用技巧
    - 用户反馈
    """
    experiences = []
    
    # 识别成功模式
    success_patterns = [
        r'成功',
        r'完成了',
        r'解决了',
        r'达到了',
        r'✅',
        r'很好',
    ]
    
    # 识别问题-解决模式
    problem_solution_pattern = r'(问题|遇到|困难|错误)[:：]?(.*?)(解决|方法|策略)[:：]?(.*?)(?=\n|$)'
    
    # 识别关键学习点
    learning_patterns = [
        r'学到',
        r'发现',
        r'注意',
        r'关键',
        r'重要',
    ]
    
    # 简单提取逻辑（实际使用时可接入 LLM）
    for pattern in success_patterns:
        if re.search(pattern, dialogue):
            experiences.append({
                "type": "成功经验",
                "content": dialogue,
                "confidence": 0.7
            })
            break
    
    return experiences


def validate_experience(experience: dict) -> bool:
    """
    验证经验是否值得固化
    筛选标准：
    1. 可复用性
    2. 有价值性
    3. 可操作性
    """
    criteria = {
        "可复用": len(experience.get("content", "")) > 20,
        "有价值": experience.get("confidence", 0) > 0.5,
    }
    
    return all(criteria.values())


def generate_experience_template(experience: dict) -> str:
    """生成经验模板"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    template = f"""
## 经验基本信息

| 项目 | 内容 |
|------|------|
| **经验名称** | [请填写简洁的经验标题] |
| **固化日期** | {timestamp} |
| **经验来源** | 对话提取 |
| **验证状态** | 🆕 新固化 |
| **使用次数** | 0（初始值） |

## 经验描述

### 原始问题
> [描述这个经验解决的问题]

### 解决方案
> [描述解决方案]

### 核心原理
> [解释为什么有效]

## 适用场景

### 最佳适用
- 场景 1：
- 场景 2：

### 边界条件
- ⚠️ 前提条件：
- ⚠️ 不适用场景：

## 操作步骤

### Step 1：
### Step 2：
### Step 3：

## 注意事项

### ✅ 要点
1. 
2. 

### ❌ 避免
1. 
2. 

---

*自动提取置信度：{experience.get('confidence', 0)}*
"""
    return template


def save_experience(experience: dict, filename: str = None):
    """保存经验到文件"""
    EXPERIENCE_DIR.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"经验_{timestamp}.md"
    
    filepath = EXPERIENCE_DIR / filename
    
    template = generate_experience_template(experience)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 经验固化记录\n{template}")
    
    print(f"✅ 经验已保存到 {filepath}")
    return filepath


def main(dialogue: str):
    """主函数"""
    print("=" * 50)
    print("🔍 灵女自进化 - 经验提取")
    print("=" * 50)
    
    # 1. 提取潜在经验
    experiences = extract_patterns_from_dialogue(dialogue)
    
    print(f"\n📊 发现 {len(experiences)} 个潜在经验")
    
    if not experiences:
        print("❌ 未发现值得提取的经验")
        return
    
    # 2. 验证每个经验
    valid_experiences = []
    for i, exp in enumerate(experiences, 1):
        print(f"\n--- 经验 {i} ---")
        print(f"内容预览：{exp['content'][:100]}...")
        print(f"置信度：{exp['confidence']}")
        
        if validate_experience(exp):
            print("✅ 通过验证")
            valid_experiences.append(exp)
        else:
            print("❌ 未通过验证")
    
    # 3. 保存通过验证的经验
    if valid_experiences:
        print(f"\n📝 保存 {len(valid_experiences)} 个有效经验...")
        for exp in valid_experiences:
            save_experience(exp)
    else:
        print("\n⚠️ 没有通过验证的经验")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="灵女自进化 - 经验提取")
    parser.add_argument("--对话内容", "-d", required=True, help="对话内容")
    
    args = parser.parse_args()
    main(args.对话内容)
