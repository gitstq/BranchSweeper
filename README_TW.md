<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="授權條款">
  <img src="https://img.shields.io/badge/dependencies-zero-brightgreen.svg" alt="依賴">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🧹 BranchSweeper</h1>

<p align="center">
  <strong>輕量級Git分支智慧清理工具</strong><br>
  <em>讓您的程式碼儲存庫保持整潔有序</em>
</p>

---

## 🎉 專案介紹

**BranchSweeper** 是一款輕量級、零依賴的Git分支智慧清理工具，幫助開發者維護整潔有序的程式碼儲存庫。它能自動偵測已合併分支、識別廢棄分支，並提供安全的批次清理功能。

### 💡 為什麼選擇 BranchSweeper？

- 🔍 **智慧分析**：自動偵測已合併和廢棄分支
- 🛡️ **安全清理**：保護分支設定防止誤刪
- 📊 **詳細報告**：產生全面的分支分析報告
- ⚡ **零依賴**：純Python實作，無需外部套件
- 🎨 **美觀輸出**：彩色終端機輸出，支援多種報告格式

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **自動偵測** | 自動偵測已合併的本機和遠端分支 |
| 🧠 **廢棄分析** | 識別長期未活動的廢棄分支 |
| 🧹 **批次清理** | 安全批次刪除多個分支 |
| 📊 **報告產生** | 產生文字、JSON或Markdown格式報告 |
| 🔒 **分支保護** | 設定保護分支，防止意外刪除 |
| 💻 **雙模式** | 支援互動式和命令列兩種模式 |
| ⚡ **零依賴** | 純Python實作，無外部依賴 |
| 🎨 **彩色輸出** | 美觀的終端機輸出，支援自訂主題 |

---

## 🚀 快速開始

### 📋 環境需求

- Python 3.8 或更高版本
- 已安裝Git並可在命令列存取

### 📦 安裝方式

```bash
# 複製儲存庫
git clone https://github.com/yourusername/BranchSweeper.git

# 進入目錄
cd BranchSweeper

# 新增執行權限（選用）
chmod +x branchsweeper.py
```

### 🔧 使用方式

```bash
# 分析分支（預設為預覽模式）
python branchsweeper.py

# 執行實際清理
python branchsweeper.py --execute

# 設定廢棄天數閾值
python branchsweeper.py --stale-days 60

# 產生JSON格式報告
python branchsweeper.py --report json

# 新增保護分支
python branchsweeper.py --protect release --protect hotfix

# 強制刪除分支
python branchsweeper.py --execute --force

# 自動確認刪除
python branchsweeper.py --execute --yes
```

---

## 📖 詳細使用指南

### 🎯 命令列選項

| 選項 | 簡寫 | 描述 |
|------|------|------|
| `--execute` | `-e` | 執行實際刪除（預設為預覽模式） |
| `--force` | `-f` | 強制刪除分支（使用 git branch -D） |
| `--stale-days` | `-s` | 廢棄分支天數閾值（預設：90天） |
| `--report` | `-r` | 報告格式：text、json、markdown |
| `--protect` | `-p` | 新增保護分支（可多次使用） |
| `--delete-remote` | | 啟用遠端分支刪除 |
| `--no-color` | | 停用彩色輸出 |
| `--yes` | `-y` | 自動確認刪除 |
| `--version` | | 顯示版本資訊 |

### 📁 設定檔

在儲存庫根目錄建立 `.branchsweeper.json`：

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

### 📊 報告格式

**文字格式（預設）**
```
============================================================
📊 BranchSweeper 分支分析報告
============================================================

📁 儲存庫路徑: /path/to/repo
🌿 總分支數: 15
  ├─ ✅ 活躍分支: 8
  ├─ 🔀 已合併分支: 4
  ├─ ⏰ 廢棄分支: 2
  └─ 🔒 保護分支: 1
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
非常適合文件和報告！

---

## 💡 設計理念

### 🎯 為什麼開發這個工具

隨著專案規模增長，Git分支管理變得繁瑣。雖然 `git branch -d` 存在，但它缺少：
- **智慧分析**分支狀態的能力
- 帶安全檢查的**批次操作**
- **詳細報告**功能
- 關鍵分支的**保護機制**

BranchSweeper 用簡單、零依賴的方案填補了這些空白。

### 🔧 技術選型

- **純Python實作**：無外部依賴，最大程度保證可攜性
- **基於子程序**：使用Git CLI確保跨平台可靠性
- **資料類別**：清晰的分支資訊資料結構
- **型別註解**：完整的型別標註，提高程式碼品質

### 🚀 迭代規劃

- [ ] GUI介面選項
- [ ] CI/CD管線整合
- [ ] 自訂清理規則引擎
- [ ] 分支命名規範檢查器
- [ ] 團隊協作功能

---

## 📦 部署指南

### 作為獨立工具

```bash
# 在shell設定檔中建立別名
alias branchsweeper='python /path/to/BranchSweeper/branchsweeper.py'

# 在任意位置使用
branchsweeper --execute
```

### 作為Git別名

```bash
# 新增到.gitconfig
git config --global alias.sweep '!python /path/to/BranchSweeper/branchsweeper.py'

# 使用方式
git sweep --execute
```

---

## 🤝 貢獻指南

我們歡迎各種形式的貢獻！參與方式：

1. 🍴 Fork本儲存庫
2. 🌿 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 💾 提交變更 (`git commit -m 'feat: 新增功能'`)
4. 📤 推送到分支 (`git push origin feature/amazing-feature`)
5. 🎉 提交Pull Request

### 📝 提交規範

我們遵循 [約定式提交](https://www.conventionalcommits.org/zh-hant/) 規範：

- `feat:` 新功能
- `fix:` 修復Bug
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 新增測試
- `chore:` 維護任務

---

## 📄 開源授權

本專案採用MIT授權條款開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

## 🙏 致謝

- 靈感來源於更整潔的Git工作流程需求
- 用❤️為開發者社群建構
- 感謝所有貢獻者！

---

<p align="center">
  <strong>BranchSweeper團隊 用❤️製作</strong>
</p>
