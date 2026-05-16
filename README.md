<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-zero-brightgreen.svg" alt="Dependencies">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🧹 BranchSweeper</h1>

<p align="center">
  <strong>Lightweight Git Branch Intelligent Cleanup Tool</strong><br>
  <em>Keep your repository clean and organized with smart branch management</em>
</p>

---

## 🎉 Introduction

**BranchSweeper** is a lightweight, zero-dependency Git branch intelligent cleanup tool that helps developers maintain clean and organized repositories. It automatically detects merged branches, identifies stale branches, and provides safe batch cleanup capabilities.

### 💡 Why BranchSweeper?

- 🔍 **Smart Analysis**: Automatically detects merged and stale branches
- 🛡️ **Safe Cleanup**: Protected branch configuration prevents accidental deletion
- 📊 **Detailed Reports**: Generate comprehensive branch analysis reports
- ⚡ **Zero Dependencies**: Pure Python implementation, no external packages required
- 🎨 **Beautiful Output**: Colorful terminal output with multiple report formats

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Auto Detection** | Automatically detect merged local and remote branches |
| 🧠 **Stale Analysis** | Identify branches with no activity for extended periods |
| 🧹 **Batch Cleanup** | Safely delete multiple branches at once |
| 📊 **Report Generation** | Generate reports in Text, JSON, or Markdown format |
| 🔒 **Branch Protection** | Configure protected branches to prevent accidental deletion |
| 💻 **Dual Mode** | Interactive and command-line modes supported |
| ⚡ **Zero Dependencies** | Pure Python implementation with no external dependencies |
| 🎨 **Colorful Output** | Beautiful terminal output with customizable themes |

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.8 or higher
- Git installed and accessible from command line

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/BranchSweeper.git

# Navigate to directory
cd BranchSweeper

# Make it executable (optional)
chmod +x branchsweeper.py
```

### 🔧 Usage

```bash
# Analyze branches (dry-run mode by default)
python branchsweeper.py

# Execute actual cleanup
python branchsweeper.py --execute

# Set stale days threshold
python branchsweeper.py --stale-days 60

# Generate JSON report
python branchsweeper.py --report json

# Add protected branches
python branchsweeper.py --protect release --protect hotfix

# Force delete branches
python branchsweeper.py --execute --force

# Auto-confirm deletion
python branchsweeper.py --execute --yes
```

---

## 📖 Detailed Usage Guide

### 🎯 Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--execute` | `-e` | Execute actual deletion (default: dry-run) |
| `--force` | `-f` | Force delete branches (git branch -D) |
| `--stale-days` | `-s` | Days threshold for stale branches (default: 90) |
| `--report` | `-r` | Report format: text, json, markdown |
| `--protect` | `-p` | Add protected branch (can be used multiple times) |
| `--delete-remote` | | Enable remote branch deletion |
| `--no-color` | | Disable colored output |
| `--yes` | `-y` | Auto-confirm deletion |
| `--version` | | Show version information |

### 📁 Configuration File

Create `.branchsweeper.json` in your repository root:

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

### 📊 Report Formats

**Text Format (Default)**
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

**JSON Format**
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

**Markdown Format**
Perfect for documentation and reports!

---

## 💡 Design Philosophy

### 🎯 Why We Built This

Managing Git branches can become tedious as projects grow. While `git branch -d` exists, it lacks:
- **Intelligent analysis** of branch status
- **Batch operations** with safety checks
- **Detailed reporting** capabilities
- **Protection mechanisms** for critical branches

BranchSweeper fills these gaps with a simple, zero-dependency solution.

### 🔧 Technical Decisions

- **Pure Python**: No external dependencies for maximum portability
- **Subprocess-based**: Uses Git CLI for reliability across platforms
- **Dataclasses**: Clean data structures for branch information
- **Type Hints**: Full type annotation for better code quality

### 🚀 Future Plans

- [ ] GUI interface option
- [ ] Integration with CI/CD pipelines
- [ ] Custom cleanup rules engine
- [ ] Branch naming convention checker
- [ ] Team collaboration features

---

## 📦 Deployment

### As a Standalone Tool

```bash
# Create alias in your shell profile
alias branchsweeper='python /path/to/BranchSweeper/branchsweeper.py'

# Use anywhere
branchsweeper --execute
```

### As a Git Alias

```bash
# Add to your .gitconfig
git config --global alias.sweep '!python /path/to/BranchSweeper/branchsweeper.py'

# Use as
git sweep --execute
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

### 📝 Commit Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the need for cleaner Git workflows
- Built with ❤️ for the developer community
- Thanks to all contributors!

---

<p align="center">
  <strong>Made with ❤️ by BranchSweeper Team</strong>
</p>
