# PaperPlot 开发标准作业程序 (SOP)

本文档定义了 PaperPlot 项目的标准开发流程，旨在确保代码质量、仓库整洁以及发布包的规范性。所有贡献者在进行开发时必须严格遵守本 SOP。

## 1. 开发流程 (Development Workflow)

### 1.1 需求分析与规划
- **明确目标**: 在开始编码前，明确功能需求或 Bug 修复的目标。
- **方案设计**: 对于复杂功能，先进行逻辑设计。
- **禁止提交规划文档**: 除非必要，不要将临时的规划文档（如 `PLAN.md`, `TODO.md`）提交到版本控制系统。

### 1.2 编码规范
- **代码位置**: 核心逻辑必须位于 `paperplot/` 目录下。
- **混入设计 (Mixins)**: 新功能应通过 Mixin 模式扩展，避免 `CorePlotter` 过于臃肿。
- **类型提示**: 尽量使用 Python 类型提示 (Type Hints)。
- **注释**: 仅对复杂逻辑进行注释，保持代码自解释。

### 1.3 测试与验证
- **单元测试**: 在 `tests/` 目录下编写对应的测试用例 (`test_*.py`)。
- **示例脚本**: 在 `examples/` 下添加展示新功能的脚本。
- **本地验证**: 在提交前，必须运行测试和示例脚本，确保功能正常且无回归错误。

## 2. 仓库卫生 (Repository Hygiene)

### 2.1 严禁提交的文件
以下文件被视为“垃圾文件”，绝对禁止提交到 Git 仓库：
- **生成产物**: 运行示例脚本生成的 `.png`, `.jpg`, `.pdf`, `.svg` (除非是项目本身的 Assets)。
- **临时文件**: `__pycache__`, `.pytest_cache`, `.DS_Store`, `.idea`, `.vscode`, `.trae` 等 IDE 配置或缓存。
- **构建产物**: `dist/`, `build/`, `*.egg-info`。
- **日志与报告**: 本地运行生成的日志文件或临时的 Markdown 报告。

### 2.2 `.gitignore` 维护
- 保持 `.gitignore` 更新，确保上述文件被自动忽略。
- 定期检查 `git status`，防止意外添加未跟踪的垃圾文件。

## 3. 文档规范 (Documentation)

- **README.md**: 如果新增了功能，必须在主 `README.md` 中简要说明。
- **Docusaurus**: 同步更新 `paperplot-docusaurus-site/` 下的文档。
- **Docstrings**: 函数和类必须包含清晰的 Docstrings。

## 4. 发布流程 (Release SOP)

发布是本项目的核心环节，必须严格执行以下步骤以防止“脏包”发布。

### 4.1 版本更新
1. 修改 `pyproject.toml` 中的 `version` 字段。
2. 更新 `paperplot-docusaurus-site/docs/changelog.md`：
   - 记录新版本号和发布日期。
   - 详细列出新增特性 (Features)、修复 (Fixes) 和变更 (Changes)。

### 4.2 清理环境
在构建前，强制清理环境：
```bash
rm -rf dist/ build/ *.egg-info
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
```

### 4.3 构建包
使用 `build` 工具构建：
```bash
python -m build
```

### 4.4 **关键：包内容审查**
在上传前，**必须**检查生成的 `sdist` (.tar.gz) 和 `wheel` (.whl) 内容：
- **检查工具**: 使用 `tar -tf dist/*.tar.gz` 和 `zipinfo dist/*.whl`。
- **审查标准**:
  - `wheel` 包中 **严禁** 包含 `tests/`, `examples/`, `docs/`, `resources/` 或 `node_modules/`。
  - `sdist` 包中应包含 `examples/` (仅源码) 和 `tests/` (可选)，但 **严禁** 包含生成的图片或临时文件。
  - 确保 `MANIFEST.in` 和 `pyproject.toml` 的 `exclude` 配置正确。

### 4.5 发布与提交
1. 上传 PyPI: `python -m twine upload dist/*`
2. Git 提交:
   - 提交 `pyproject.toml`, `changelog.md` 及相关代码变更。
   - Tag 版本 (可选): `git tag vX.Y.Z`
   - 推送到 GitHub: `git push`

## 5. 紧急回滚与修复
- 如果发现已发布版本包含错误或垃圾文件，**不可撤销** PyPI 发布。
- **必须** 立即遵循上述流程发布一个新的补丁版本 (Patch Version, 如 `0.1.18` -> `0.1.19`) 进行覆盖修复。
