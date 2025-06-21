# My Modern C++ Project

这是一个基于现代CMake和Conan 2.0的C++项目脚手架。

## 特性

-   C++17 标准
-   CMake (Target-based)
-   Conan 2.0 依赖管理
-   Google Test 集成
-   清晰的项目结构

## 依赖

-   C++ 编译器 (支持 C++17)
-   CMake (>= 3.15)
-   Conan (>= 2.0)

## 如何构建

1.  **克隆仓库**
    ```bash
    git clone <your-repo-url>
    cd my-project
    ```

2.  **安装Conan依赖**
    此命令会读取 `conanfile.py`，下载依赖，并在 `build/` 目录下生成CMake集成所需的文件。
    ```bash
    # 注意：不再需要 --output-folder
    conan install . -s build_type=Debug --build=missing    # For Debug build
    conan install . -s build_type=Release --build=missing    # For Debug build
    ```

3.  **配置CMake项目**
    使用Conan生成的toolchain文件来配置CMake。
    ```bash
    # Configure for Release
    cmake -S . -B build/release -DCMAKE_TOOLCHAIN_FILE=build/release/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release

    # Configure for Debug
    cmake -S . -B build/debug -DCMAKE_TOOLCHAIN_FILE=build/debug/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Debug
    ```

4.  **构建项目**
    ```bash
    # Build Release
    cmake --build build/release

    # Build Debug
    cmake --build build/debug
    ```

5.  **运行**
    ```bash
    # Run application
    ./build/release/bin/app

    # Run tests
    cd build/release
    ctest -C Release --output-on-failure
    cd ../..
    ```