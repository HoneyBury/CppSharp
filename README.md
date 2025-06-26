# My Modern C++ Project

这是一个基于现代CMake和Conan 2.0的C++项目脚手架。

## 特性

-   C++17 标准
-   CMake (Target-based)
-   Conan 2.0 依赖管理
-   Google Test 集成
-   清晰的项目结构
-   Github Action CI/CD 集成

## 依赖

-   C++ 编译器 (支持 C++17)
-   CMake (>= 3.15)
-   Conan (>= 2.0)

## 如何构建

1.  **克隆仓库**
    ```bash
    git clone https://github.com/HoneyBury/CppSharp.git
    cd CppSharp
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
    # 可以使用预设的命令方式
    
    # windows平台下
    cmake --preset conan-default -DBUILD_TESTING=OFF
    # linux/mac平台下
    cmake --preset conan-debug -DBUILD_TESTING=OFF
    
    # Configure for Release
    cmake -S . -B build/release -DCMAKE_TOOLCHAIN_FILE="build/generators/conan_toolchain.cmake" -DCMAKE_BUILD_TYPE=Release

    # Configure for Debug
    cmake -S . -B build/debug -DCMAKE_TOOLCHAIN_FILE="build/generators/conan_toolchain.cmake" -DCMAKE_BUILD_TYPE=Debug
    ```

4.  **构建项目**
    ```bash
    
    # 同样有预设的方式 这里平台是统一的
    cmake --build --preset conan-debug
    cmake --build --preset conan-release
    
    # Build Release
    cmake --build build/release

    # Build Debug
    cmake --build build/debug
    ```

5.  **运行**
    ```bash
    # Run application
    ./build/release/bin/app
    
    # 如果使用预设的方式windows平台会不太一样
    ./build/bin/app
    
    # Run tests
    cd build/release
    ctest -C Release --output-on-failure
    cd ../..
    ```
6. **打包**
    ```bash
     cmake --build --preset conan-debug --target package
   # 或者可以使用cpack安装
   
   ```
    