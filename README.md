# lingnv-skills
灵女的自研技能集合 / Lingnv's self-developed skills collection

## Git 命令学习笔记

### 学习日期
2026年01月

### 掌握的Git基础命令

#### 1. 仓库管理
- `git clone <url>` - 克隆远程仓库到本地
- `git init` - 初始化本地Git仓库
- `git remote -v` - 查看远程仓库信息

#### 2. 分支操作
- `git branch` - 查看本地分支
- `git branch -a` - 查看所有分支（含远程）
- `git checkout -b <分支名>` - 创建并切换到新分支
- `git switch <分支名>` - 切换分支（推荐）
- `git branch -d <分支名>` - 删除分支

#### 3. 文件操作
- `git add <文件>` - 暂存单个文件
- `git add .` - 暂存所有修改的文件
- `git status` - 查看当前状态

#### 4. 提交操作
- `git commit -m "信息"` - 提交暂存区修改
- `git commit -am "信息"` - 跳过add直接提交已跟踪文件

#### 5. 远程协作
- `git push origin <分支>` - 推送到远程仓库
- `git push -u origin <分支>` - 首次推送并设置上游
- `git pull origin <分支>` - 拉取并合并远程更新
- `git merge <分支>` - 合并指定分支到当前分支

#### 6. 查看历史
- `git log` - 查看提交历史
- `git log --oneline --graph` - 简洁版提交历史（带分支图）

### 实践操作记录

1. ✅ 使用 `git clone` 克隆了 lingnv-skills 仓库
2. ✅ 使用 `git checkout -b` 创建并切换到 learn-git 分支
3. ✅ 编辑 README.md 添加学习笔记
4. ✅ 使用 `git add .` 暂存修改
5. ✅ 使用 `git commit -m` 提交更改
6. ✅ 使用 `git push -u origin learn-git` 推送到远程
7. ✅ 使用 `git merge` 将 learn-git 合并到 main 分支

### Git 工作流程总结

```
工作区 → 暂存区 → 版本库 → 远程仓库
  add     commit      push
```

### 注意事项
- 提交前先 `git status` 查看状态
- 推送前先 `git pull` 拉取最新代码避免冲突
- 合并分支前确认当前在目标分支
- 提交信息要清晰描述变更内容

---
*学习完成，掌握了Git基础操作*
