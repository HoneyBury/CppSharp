# CppSharp - Modern C++ Scaffold

这是一个基于 `CMake + Conan 2 + GoogleTest + CPack` 的 C++ 脚手架，已针对日常在 macOS + Codex CLI + CLion 的开发场景做了跨平台工程化升级。

## 核心升级

- CI/CD 覆盖 Linux / Windows / macOS
- 统一构建链路：`Conan + CMake + Ninja`
- 自动格式化并自动提交（`main` 分支）
- 统一编码和换行：源码/配置/文档使用 UTF-8 BOM + LF
- 静态检查：`cppcheck + clang-tidy`
- 本地任务编排：`Taskfile.yml`

## 目录中的工程化文件

- `.github/workflows/ci.yml`：主 CI（质量门禁 + 三平台构建测试打包）
- `.github/workflows/release.yml`：tag 发布流程（`v*`）
- `.github/workflows/format.yml`：自动格式化并自动提交
- `.editorconfig`：编辑器统一规范
- `.gitattributes`：Git 层面统一编码/换行策略
- `.clang-tidy`：静态分析规则
- `Taskfile.yml`：本地命令入口
- `scripts/run_clang_format.sh`：C/C++ 格式化
- `scripts/normalize_text.py`：编码/换行归一化（支持 `--check`）

## 快速开始

1. 安装依赖

```bash
python3 -m pip install --upgrade pip
python3 -m pip install conan ninja
conan profile detect --force
```

2. Debug 构建与测试

```bash
task test BUILD_TYPE=Debug
```

3. Release 打包

```bash
task package
```

## 常用 Task

```bash
task setup
task configure BUILD_TYPE=Debug
task build BUILD_TYPE=Debug
task test BUILD_TYPE=Debug
task format
task check-format
task lint
task ci
```

## 编码与换行策略

- 默认文本文件：UTF-8 BOM + LF
- JSON（含 CMake Presets）：UTF-8（无 BOM）+ LF
- 脚本文件（`.py/.sh/.bat/.ps1`）：UTF-8（无 BOM）
  - 原因：解释器脚本使用 BOM 可能影响 shebang/执行行为

CI 会执行：

```bash
python3 scripts/normalize_text.py --check
bash scripts/run_clang_format.sh --check
```

## 自动格式化与自动提交

`format.yml` 在 `main` 分支 push 或手动触发时执行：

1. `clang-format` 格式化 C/C++
2. 编码/换行归一化
3. 若有变更则自动提交到当前分支

## 发布流程

- 创建并推送 tag：`vX.Y.Z`
- `release.yml` 会在三平台构建并生成安装包
- 自动创建 GitHub Release，并上传所有产物
