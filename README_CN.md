<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="许可证">
  <img src="https://img.shields.io/badge/dependencies-zero-brightgreen.svg" alt="依赖">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🧹 BranchSweeper</h1>

<p align="center">
  <strong>轻量级Git分支智能清理工具</strong><br>
  <em>让您的代码仓库保持整洁有序</em>
</p>

---

## 🎉 项目介绍

**BranchSweeper** 是一款轻量级、零依赖的Git分支智能清理工具，帮助开发者维护整洁有序的代码仓库。它能自动检测已合并分支、识别废弃分支，并提供安全的批量清理功能。

### 💡 为什么选择 BranchSweeper？

- 🔍 **智能分析**：自动检测已合并和废弃分支
- 🛡️ **安全清理**：保护分支配置防止误删
- 📊 **详细报告**：生成全面的分支分析报告
- ⚡ **零依赖**：纯Python实现，无需外部包
- 🎨 **美观输出**：彩色终端输出，支持多种报告格式

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **自动检测** | 自动检测已合并的本地和远程分支 |
| 🧠 **废弃分析** | 识别长期未活动的废弃分支 |
| 🧹 **批量清理** | 安全批量删除多个分支 |
| 📊 **报告生成** | 生成文本、JSON或Markdown格式报告 |
| 🔒 **分支保护** | 配置保护分支，防止意外删除 |
| 💻 **双模式** | 支持交互式和命令行两种模式 |
| ⚡ **零依赖** | 纯Python实现，无外部依赖 |
| 🎨 **彩色输出** | 美观的终端输出，支持自定义主题 |

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8 或更高版本
- 已安装Git并可在命令行访问

### 📦 安装方法

```bash
# 克隆仓库
git clone https://github.com/yourusername/BranchSweeper.git

# 进入目录
cd BranchSweeper

# 添加执行权限（可选）
chmod +x branchsweeper.py
```

### 🔧 使用方法

```bash
# 分析分支（默认为预览模式）
python branchsweeper.py

# 执行实际清理
python branchsweeper.py --execute

# 设置废弃天数阈值
python branchsweeper.py --stale-days 60

# 生成JSON格式报告
python branchsweeper.py --report json

# 添加保护分支
python branchsweeper.py --protect release --protect hotfix

# 强制删除分支
python branchsweeper.py --execute --force

# 自动确认删除
python branchsweeper.py --execute --yes
```

---

## 📖 详细使用指南

### 🎯 命令行选项

| 选项 | 简写 | 描述 |
|------|------|------|
| `--execute` | `-e` | 执行实际删除（默认为预览模式） |
| `--force` | `-f` | 强制删除分支（使用 git branch -D） |
| `--stale-days` | `-s` | 废弃分支天数阈值（默认：90天） |
| `--report` | `-r` | 报告格式：text、json、markdown |
| `--protect` | `-p` | 添加保护分支（可多次使用） |
| `--delete-remote` | | 启用远程分支删除 |
| `--no-color` | | 禁用彩色输出 |
| `--yes` | `-y` | 自动确认删除 |
| `--version` | | 显示版本信息 |

### 📁 配置文件

在仓库根目录创建 `.branchsweeper.json`：

```json
{
    "protected_branches": ["main", "master", "develop", "staging", "production"],
    "stale_days": 90,
    "auto_confirm": false,
    "dry_run": true,
    "delete_remote": false,
    "report_format": "text"
}
```

### 📊 报告格式

**文本格式（默认）**
```
============================================================
📊 BranchSweeper 分支分析报告
============================================================

📁 仓库路径: /path/to/repo
🌿 总分支数: 15
  ├─ ✅ 活跃分支: 8
  ├─ 🔀 已合并分支: 4
  ├─ ⏰ 废弃分支: 2
  └─ 🔒 保护分支: 1
```

**JSON格式**
```json
{
  "repository": "/path/to/repo",
  "current_branch": "main",
  "summary": {
    "total_branches": 15,
    "merged": 4,
    "stale": 2
  }
}
```

**Markdown格式**
非常适合文档和报告！

---

## 💡 设计思路

### 🎯 为什么开发这个工具

随着项目规模增长，Git分支管理变得繁琐。虽然 `git branch -d` 存在，但它缺少：
- **智能分析**分支状态的能力
- 带安全检查的**批量操作**
- **详细报告**功能
- 关键分支的**保护机制**

BranchSweeper 用简单、零依赖的方案填补了这些空白。

### 🔧 技术选型

- **纯Python实现**：无外部依赖，最大程度保证可移植性
- **基于子进程**：使用Git CLI确保跨平台可靠性
- **数据类**：清晰的分支信息数据结构
- **类型注解**：完整的类型标注，提高代码质量

### 🚀 迭代规划

- [ ] GUI界面选项
- [ ] CI/CD流水线集成
- [ ] 自定义清理规则引擎
- [ ] 分支命名规范检查器
- [ ] 团队协作功能

---

## 📦 部署指南

### 作为独立工具

```bash
# 在shell配置文件中创建别名
alias branchsweeper='python /path/to/BranchSweeper/branchsweeper.py'

# 在任意位置使用
branchsweeper --execute
```

### 作为Git别名

```bash
# 添加到.gitconfig
git config --global alias.sweep '!python /path/to/BranchSweeper/branchsweeper.py'

# 使用方式
git sweep --execute
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！参与方式：

1. 🍴 Fork本仓库
2. 🌿 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 💾 提交更改 (`git commit -m 'feat: 添加新功能'`)
4. 📤 推送到分支 (`git push origin feature/amazing-feature`)
5. 🎉 提交Pull Request

### 📝 提交规范

我们遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/) 规范：

- `feat:` 新功能
- `fix:` 修复Bug
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 添加测试
- `chore:` 维护任务

---

## 📄 开源协议

本项目采用MIT协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 灵感来源于更整洁的Git工作流需求
- 用❤️为开发者社区构建
- 感谢所有贡献者！

---

<p align="center">
  <strong>BranchSweeper团队 用❤️制作</strong>
</p>
