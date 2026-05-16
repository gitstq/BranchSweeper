#!/usr/bin/env python3
"""
BranchSweeper - 轻量级Git分支智能清理工具
Lightweight Git Branch Intelligent Cleanup Tool

Author: BranchSweeper Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import json
import argparse
import subprocess
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class BranchStatus(Enum):
    """分支状态枚举"""
    ACTIVE = "active"           # 活跃分支
    MERGED = "merged"           # 已合并分支
    STALE = "stale"            # 废弃分支（长期未活动）
    PROTECTED = "protected"     # 保护分支
    CURRENT = "current"         # 当前分支


@dataclass
class BranchInfo:
    """分支信息数据类"""
    name: str
    is_remote: bool
    last_commit_date: Optional[datetime]
    last_commit_author: Optional[str]
    last_commit_message: Optional[str]
    is_merged: bool
    status: BranchStatus
    ahead_count: int = 0
    behind_count: int = 0
    days_since_last_commit: int = 0


class Colors:
    """终端颜色配置"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    @classmethod
    def disable(cls):
        """禁用颜色输出"""
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = ''
        cls.MAGENTA = cls.CYAN = cls.WHITE = cls.BOLD = ''
        cls.DIM = cls.RESET = ''


class GitCommand:
    """Git命令执行器"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)
        self._verify_git_repo()
    
    def _verify_git_repo(self):
        """验证是否为Git仓库"""
        git_dir = os.path.join(self.repo_path, ".git")
        if not os.path.exists(git_dir):
            raise NotAGitRepositoryError(f"Not a git repository: {self.repo_path}")
    
    def _run_command(self, args: List[str], check: bool = True) -> Tuple[bool, str]:
        """执行Git命令"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip() if e.stderr else str(e)
    
    def get_current_branch(self) -> str:
        """获取当前分支名"""
        success, output = self._run_command(["branch", "--show-current"])
        return output if success else ""
    
    def get_all_branches(self) -> Tuple[List[str], List[str]]:
        """获取所有本地和远程分支"""
        local_branches = []
        remote_branches = []
        
        # 获取本地分支
        success, output = self._run_command(["branch", "--list"])
        if success:
            for line in output.split("\n"):
                line = line.strip()
                if line:
                    # 移除当前分支标记
                    name = line.lstrip("* ").strip()
                    if name:
                        local_branches.append(name)
        
        # 获取远程分支
        success, output = self._run_command(["branch", "-r"])
        if success:
            for line in output.split("\n"):
                line = line.strip()
                if line and "->" not in line:  # 排除HEAD指针
                    # 提取分支名（移除远程名前缀）
                    if "/" in line:
                        name = "/".join(line.split("/")[1:])
                        if name and name not in remote_branches:
                            remote_branches.append(name)
        
        return local_branches, remote_branches
    
    def get_branch_last_commit(self, branch: str, is_remote: bool = False) -> Dict:
        """获取分支最后一次提交信息"""
        branch_ref = f"origin/{branch}" if is_remote else branch
        format_str = "%H|%ci|%an|%s"
        
        success, output = self._run_command(
            ["log", branch_ref, "-1", f"--format={format_str}"],
            check=False
        )
        
        if success and output:
            parts = output.split("|", 3)
            if len(parts) >= 4:
                try:
                    commit_date = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S %z")
                except ValueError:
                    try:
                        commit_date = datetime.strptime(parts[1].split()[0], "%Y-%m-%d")
                    except ValueError:
                        commit_date = None
                
                return {
                    "hash": parts[0],
                    "date": commit_date,
                    "author": parts[2],
                    "message": parts[3]
                }
        
        return {"hash": None, "date": None, "author": None, "message": None}
    
    def is_branch_merged(self, branch: str, target: str = "main") -> bool:
        """检查分支是否已合并到目标分支"""
        # 首先尝试main，然后尝试master
        success, _ = self._run_command(["rev-parse", "--verify", target], check=False)
        if not success:
            success, _ = self._run_command(["rev-parse", "--verify", "master"], check=False)
            if success:
                target = "master"
            else:
                return False
        
        success, output = self._run_command(
            ["branch", "--merged", target],
            check=False
        )
        
        if success:
            merged_branches = [b.strip().lstrip("* ") for b in output.split("\n") if b.strip()]
            return branch in merged_branches
        
        return False
    
    def get_branch_ahead_behind(self, branch: str, target: str = "main") -> Tuple[int, int]:
        """获取分支相对于目标分支的ahead/behind计数"""
        success, _ = self._run_command(["rev-parse", "--verify", target], check=False)
        if not success:
            success, _ = self._run_command(["rev-parse", "--verify", "master"], check=False)
            if success:
                target = "master"
            else:
                return 0, 0
        
        success, output = self._run_command(
            ["rev-list", "--left-right", "--count", f"{branch}...{target}"],
            check=False
        )
        
        if success and output:
            parts = output.split()
            if len(parts) == 2:
                return int(parts[0]), int(parts[1])
        
        return 0, 0
    
    def delete_branch(self, branch: str, force: bool = False) -> Tuple[bool, str]:
        """删除本地分支"""
        flag = "-D" if force else "-d"
        return self._run_command(["branch", flag, branch], check=False)
    
    def delete_remote_branch(self, branch: str) -> Tuple[bool, str]:
        """删除远程分支"""
        return self._run_command(["push", "origin", "--delete", branch], check=False)


class NotAGitRepositoryError(Exception):
    """非Git仓库异常"""
    pass


class BranchSweeper:
    """分支清理器主类"""
    
    DEFAULT_CONFIG = {
        "protected_branches": ["main", "master", "develop", "staging", "production"],
        "stale_days": 90,  # 超过90天未活动视为废弃
        "auto_confirm": False,
        "dry_run": True,
        "delete_remote": False,
        "report_format": "text"  # text, json, markdown
    }
    
    def __init__(self, repo_path: str = ".", config: Optional[Dict] = None):
        self.repo_path = os.path.abspath(repo_path)
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.git = GitCommand(repo_path)
        self.branches: List[BranchInfo] = []
        self.current_branch = ""
        
    def load_config(self, config_path: Optional[str] = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(self.repo_path, ".branchsweeper.json")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except (json.JSONDecodeError, IOError):
                pass
        
        return self.config
    
    def save_config(self, config_path: Optional[str] = None):
        """保存配置文件"""
        if config_path is None:
            config_path = os.path.join(self.repo_path, ".branchsweeper.json")
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def analyze_branches(self) -> List[BranchInfo]:
        """分析所有分支"""
        self.branches = []
        self.current_branch = self.git.get_current_branch()
        
        local_branches, remote_branches = self.git.get_all_branches()
        
        # 分析本地分支
        for branch in local_branches:
            info = self._analyze_single_branch(branch, is_remote=False)
            self.branches.append(info)
        
        # 分析远程分支（如果启用）
        if self.config.get("delete_remote", False):
            for branch in remote_branches:
                if branch not in local_branches:  # 避免重复
                    info = self._analyze_single_branch(branch, is_remote=True)
                    self.branches.append(info)
        
        return self.branches
    
    def _analyze_single_branch(self, branch: str, is_remote: bool) -> BranchInfo:
        """分析单个分支"""
        commit_info = self.git.get_branch_last_commit(branch, is_remote)
        
        # 计算距离上次提交的天数
        days_since = 0
        if commit_info["date"]:
            delta = datetime.now(commit_info["date"].tzinfo) - commit_info["date"]
            days_since = delta.days
        
        # 确定分支状态
        status = self._determine_branch_status(branch, is_remote, commit_info, days_since)
        
        # 获取ahead/behind计数
        ahead, behind = 0, 0
        if not is_remote:
            ahead, behind = self.git.get_branch_ahead_behind(branch)
        
        return BranchInfo(
            name=branch,
            is_remote=is_remote,
            last_commit_date=commit_info["date"],
            last_commit_author=commit_info["author"],
            last_commit_message=commit_info["message"],
            is_merged=(status == BranchStatus.MERGED),
            status=status,
            ahead_count=ahead,
            behind_count=behind,
            days_since_last_commit=days_since
        )
    
    def _determine_branch_status(self, branch: str, is_remote: bool, 
                                  commit_info: Dict, days_since: int) -> BranchStatus:
        """确定分支状态"""
        # 当前分支
        if branch == self.current_branch and not is_remote:
            return BranchStatus.CURRENT
        
        # 保护分支
        protected = self.config.get("protected_branches", [])
        if branch.lower() in [p.lower() for p in protected]:
            return BranchStatus.PROTECTED
        
        # 已合并分支
        if not is_remote and self.git.is_branch_merged(branch):
            return BranchStatus.MERGED
        
        # 废弃分支
        stale_days = self.config.get("stale_days", 90)
        if days_since > stale_days:
            return BranchStatus.STALE
        
        return BranchStatus.ACTIVE
    
    def get_branches_by_status(self, status: BranchStatus) -> List[BranchInfo]:
        """按状态获取分支"""
        return [b for b in self.branches if b.status == status]
    
    def get_deletable_branches(self) -> List[BranchInfo]:
        """获取可删除的分支（已合并或废弃）"""
        return [b for b in self.branches 
                if b.status in (BranchStatus.MERGED, BranchStatus.STALE) 
                and not b.is_remote]
    
    def delete_branches(self, branches: List[str], force: bool = False) -> Dict[str, Tuple[bool, str]]:
        """批量删除分支"""
        results = {}
        
        for branch in branches:
            # 安全检查
            if branch == self.current_branch:
                results[branch] = (False, "Cannot delete current branch")
                continue
            
            branch_info = next((b for b in self.branches if b.name == branch), None)
            if branch_info and branch_info.status == BranchStatus.PROTECTED:
                results[branch] = (False, "Branch is protected")
                continue
            
            if self.config.get("dry_run", True):
                results[branch] = (True, "[DRY RUN] Would delete branch")
                continue
            
            if branch_info and branch_info.is_remote:
                success, msg = self.git.delete_remote_branch(branch)
            else:
                success, msg = self.git.delete_branch(branch, force)
            
            results[branch] = (success, msg)
        
        return results
    
    def generate_report(self, format_type: Optional[str] = None) -> str:
        """生成清理报告"""
        format_type = format_type or self.config.get("report_format", "text")
        
        if format_type == "json":
            return self._generate_json_report()
        elif format_type == "markdown":
            return self._generate_markdown_report()
        else:
            return self._generate_text_report()
    
    def _generate_text_report(self) -> str:
        """生成文本格式报告"""
        lines = []
        lines.append(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        lines.append(f"{Colors.BOLD}📊 BranchSweeper 分支分析报告{Colors.RESET}")
        lines.append(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
        
        # 统计信息
        total = len(self.branches)
        merged = len(self.get_branches_by_status(BranchStatus.MERGED))
        stale = len(self.get_branches_by_status(BranchStatus.STALE))
        active = len(self.get_branches_by_status(BranchStatus.ACTIVE))
        protected = len(self.get_branches_by_status(BranchStatus.PROTECTED))
        
        lines.append(f"📁 仓库路径: {self.repo_path}")
        lines.append(f"🌿 总分支数: {total}")
        lines.append(f"  ├─ {Colors.GREEN}✅ 活跃分支: {active}{Colors.RESET}")
        lines.append(f"  ├─ {Colors.YELLOW}🔀 已合并分支: {merged}{Colors.RESET}")
        lines.append(f"  ├─ {Colors.RED}⏰ 废弃分支: {stale}{Colors.RESET}")
        lines.append(f"  └─ {Colors.BLUE}🔒 保护分支: {protected}{Colors.RESET}")
        
        # 可删除分支
        deletable = self.get_deletable_branches()
        if deletable:
            lines.append(f"\n{Colors.YELLOW}🧹 可清理分支 ({len(deletable)}):{Colors.RESET}")
            for b in deletable:
                status_icon = "🔀" if b.status == BranchStatus.MERGED else "⏰"
                lines.append(f"  {status_icon} {b.name}")
                if b.last_commit_date:
                    lines.append(f"     最后提交: {b.last_commit_date.strftime('%Y-%m-%d')} ({b.days_since_last_commit}天前)")
                if b.last_commit_message:
                    msg = b.last_commit_message[:50] + "..." if len(b.last_commit_message) > 50 else b.last_commit_message
                    lines.append(f"     提交信息: {msg}")
        else:
            lines.append(f"\n{Colors.GREEN}✨ 没有需要清理的分支！{Colors.RESET}")
        
        lines.append(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        return "\n".join(lines)
    
    def _generate_json_report(self) -> str:
        """生成JSON格式报告"""
        report = {
            "repository": self.repo_path,
            "current_branch": self.current_branch,
            "analysis_date": datetime.now().isoformat(),
            "summary": {
                "total_branches": len(self.branches),
                "active": len(self.get_branches_by_status(BranchStatus.ACTIVE)),
                "merged": len(self.get_branches_by_status(BranchStatus.MERGED)),
                "stale": len(self.get_branches_by_status(BranchStatus.STALE)),
                "protected": len(self.get_branches_by_status(BranchStatus.PROTECTED)),
                "deletable": len(self.get_deletable_branches())
            },
            "branches": [
                {
                    "name": b.name,
                    "is_remote": b.is_remote,
                    "status": b.status.value,
                    "last_commit_date": b.last_commit_date.isoformat() if b.last_commit_date else None,
                    "days_since_last_commit": b.days_since_last_commit,
                    "last_commit_author": b.last_commit_author,
                    "ahead_count": b.ahead_count,
                    "behind_count": b.behind_count
                }
                for b in self.branches
            ]
        }
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def _generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        lines = []
        lines.append("# 📊 BranchSweeper 分支分析报告\n")
        lines.append(f"**仓库路径**: `{self.repo_path}`  ")
        lines.append(f"**当前分支**: `{self.current_branch}`  ")
        lines.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 统计表格
        lines.append("## 📈 分支统计\n")
        lines.append("| 状态 | 数量 |")
        lines.append("|------|------|")
        lines.append(f"| ✅ 活跃 | {len(self.get_branches_by_status(BranchStatus.ACTIVE))} |")
        lines.append(f"| 🔀 已合并 | {len(self.get_branches_by_status(BranchStatus.MERGED))} |")
        lines.append(f"| ⏰ 废弃 | {len(self.get_branches_by_status(BranchStatus.STALE))} |")
        lines.append(f"| 🔒 保护 | {len(self.get_branches_by_status(BranchStatus.PROTECTED))} |")
        
        # 可删除分支
        deletable = self.get_deletable_branches()
        if deletable:
            lines.append(f"\n## 🧹 可清理分支\n")
            lines.append("| 分支名 | 状态 | 最后提交 | 天数 |")
            lines.append("|--------|------|----------|------|")
            for b in deletable:
                status = "已合并" if b.status == BranchStatus.MERGED else "废弃"
                date = b.last_commit_date.strftime('%Y-%m-%d') if b.last_commit_date else "N/A"
                lines.append(f"| `{b.name}` | {status} | {date} | {b.days_since_last_commit} |")
        
        return "\n".join(lines)


def interactive_mode(sweeper: BranchSweeper) -> None:
    """交互式模式"""
    print(f"\n{Colors.BOLD}🚀 BranchSweeper - Git分支智能清理工具{Colors.RESET}")
    print(f"{Colors.DIM}版本 1.0.0 | MIT License{Colors.RESET}\n")
    
    # 分析分支
    print(f"{Colors.CYAN}🔍 正在分析分支...{Colors.RESET}")
    sweeper.analyze_branches()
    
    # 显示报告
    print(sweeper.generate_report())
    
    # 获取可删除分支
    deletable = sweeper.get_deletable_branches()
    
    if not deletable:
        print(f"\n{Colors.GREEN}✨ 仓库很干净，没有需要清理的分支！{Colors.RESET}")
        return
    
    # 确认删除
    if sweeper.config.get("dry_run", True):
        print(f"\n{Colors.YELLOW}⚠️ 当前为预览模式 (dry-run)，不会实际删除分支{Colors.RESET}")
        print(f"   使用 --execute 参数执行实际删除操作\n")
        return
    
    if sweeper.config.get("auto_confirm", False):
        print(f"\n{Colors.YELLOW}🔄 自动确认模式，正在删除分支...{Colors.RESET}")
        branches_to_delete = [b.name for b in deletable]
        results = sweeper.delete_branches(branches_to_delete)
        
        for branch, (success, msg) in results.items():
            icon = "✅" if success else "❌"
            print(f"  {icon} {branch}: {msg}")
    else:
        print(f"\n{Colors.YELLOW}是否删除以上分支？{Colors.RESET}")
        print(f"  输入 'y' 确认删除，输入 'n' 取消: ", end="")
        
        try:
            choice = input().strip().lower()
            if choice == 'y':
                branches_to_delete = [b.name for b in deletable]
                results = sweeper.delete_branches(branches_to_delete)
                
                print(f"\n{Colors.GREEN}🗑️ 删除结果:{Colors.RESET}")
                for branch, (success, msg) in results.items():
                    icon = "✅" if success else "❌"
                    print(f"  {icon} {branch}: {msg}")
            else:
                print(f"\n{Colors.BLUE}ℹ️ 操作已取消{Colors.RESET}")
        except EOFError:
            print(f"\n{Colors.BLUE}ℹ️ 操作已取消{Colors.RESET}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="🧹 BranchSweeper - 轻量级Git分支智能清理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 分析当前仓库分支
  %(prog)s --execute          # 执行实际删除操作
  %(prog)s --stale-days 60    # 设置废弃天数为60天
  %(prog)s --report json      # 输出JSON格式报告
  %(prog)s --protect release  # 添加保护分支
        """
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Git仓库路径 (默认: 当前目录)"
    )
    parser.add_argument(
        "-e", "--execute",
        action="store_true",
        help="执行实际删除操作 (默认为预览模式)"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="强制删除分支 (使用 git branch -D)"
    )
    parser.add_argument(
        "-s", "--stale-days",
        type=int,
        default=90,
        help="废弃分支天数阈值 (默认: 90天)"
    )
    parser.add_argument(
        "-r", "--report",
        choices=["text", "json", "markdown"],
        default="text",
        help="报告输出格式 (默认: text)"
    )
    parser.add_argument(
        "-p", "--protect",
        action="append",
        help="添加保护分支 (可多次使用)"
    )
    parser.add_argument(
        "--delete-remote",
        action="store_true",
        help="同时删除远程分支"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="禁用颜色输出"
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="自动确认删除操作"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    # 禁用颜色
    if args.no_color:
        Colors.disable()
    
    # 构建配置
    config = {
        "dry_run": not args.execute,
        "stale_days": args.stale_days,
        "report_format": args.report,
        "delete_remote": args.delete_remote,
        "auto_confirm": args.yes
    }
    
    if args.protect:
        config["protected_branches"] = args.protect
    
    try:
        sweeper = BranchSweeper(args.path, config)
        sweeper.load_config()
        interactive_mode(sweeper)
    except NotAGitRepositoryError as e:
        print(f"{Colors.RED}❌ 错误: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ 操作已中断{Colors.RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"{Colors.RED}❌ 发生错误: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
