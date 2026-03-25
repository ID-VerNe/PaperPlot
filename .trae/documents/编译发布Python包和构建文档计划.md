# 编译发布Python包和构建文档计划（含清理步骤）

## 1. 清理旧的编译文件

### 步骤1：检查并删除Python包的旧编译文件
- 删除 `dist` 目录（如果存在）
- 删除 `build` 目录（如果存在）
- 删除 `*.egg-info` 目录（如果存在）

### 步骤2：检查并删除文档的旧构建文件
- 进入 `paperplot-docusaurus-site` 目录
- 删除 `build` 目录（如果存在）

## 2. 编译并发布Python包到PyPI

### 步骤1：构建Python包
- 使用 `python -m build` 命令构建包
- 该命令会生成 `dist` 目录，包含 `.tar.gz` 和 `.whl` 文件

### 步骤2：发布到PyPI
- 使用 `twine upload dist/*` 命令发布包
- 这将把构建好的包上传到PyPI

## 3. 构建文档网站

### 步骤1：进入文档目录
- 切换到 `paperplot-docusaurus-site` 目录

### 步骤2：安装文档依赖（如果需要）
- 执行 `npm install` 安装必要的依赖

### 步骤3：构建文档
- 执行 `npm run build` 构建文档
- 构建完成后，文档将生成在 `build` 目录中

## 4. 验证结果
- 确认PyPI上成功发布了新版本
- 确认文档构建成功，生成了静态文件

## 注意事项
- 确保PyPI账号已配置（通过 `~/.pypirc` 文件）
- 确保npm版本符合要求（文档要求Node.js >= 20.0）
- 构建过程中可能需要联网下载依赖