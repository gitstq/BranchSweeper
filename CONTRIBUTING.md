# 🤝 Contributing to BranchSweeper

感谢您有兴趣为 BranchSweeper 做出贡献！

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发指南](#开发指南)
- [提交规范](#提交规范)
- [代码风格](#代码风格)

## 行为准则

本项目采用贡献者公约作为行为准则。参与本项目即表示您同意遵守其条款。

## 如何贡献

### 报告Bug

如果您发现了bug，请创建一个issue，包含：

1. 清晰的标题和描述
2. 重现步骤
3. 预期行为
4. 实际行为
5. 环境信息（Python版本、操作系统等）

### 提交功能请求

欢迎提交功能请求！请创建一个issue，描述：

1. 功能的用途
2. 预期的使用方式
3. 可能的实现方案（可选）

### 提交代码

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 进行更改
4. 确保测试通过
5. 提交更改 (`git commit -m 'feat: add amazing feature'`)
6. 推送到分支 (`git push origin feature/amazing-feature`)
7. 创建 Pull Request

## 开发指南

### 环境设置

```bash
# 克隆您的fork
git clone https://github.com/your-username/BranchSweeper.git
cd BranchSweeper

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install pytest black mypy
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_branchsweeper.py
```

### 代码检查

```bash
# 格式化代码
black branchsweeper.py

# 类型检查
mypy branchsweeper.py
```

## 提交规范

我们遵循 [约定式提交](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 代码重构
- `perf:` 性能优化
- `test:` 添加或修改测试
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: 添加分支名称过滤功能
fix: 修复远程分支检测问题
docs: 更新安装说明
```

## 代码风格

- 遵循 PEP 8 规范
- 使用 4 个空格缩进
- 最大行长度 100 字符
- 使用类型注解
- 编写文档字符串

---

再次感谢您的贡献！🎉
