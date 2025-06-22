# conanfile.py
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
import os

class MyProjectConan(ConanFile):
    # --- 1. 元数据：描述你的包 ---
    name = "MyProject"
    version = "1.0.0"
    license = "<MIT>"  # 例如 "MIT"
    author = "<HoneyBury> <zoujiahe389@gmail.com>"
    url = "<https://github.com/HoneyBury/CppSharp.git>"
    description = "A modern C++ project template."
    topics = ("template", "modern-cpp", "cmake", "conan")

    # --- 2. 配置：定义包的二进制变体 ---
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # --- 3. 导出：指定哪些文件是配方的一部分 ---
    # 当我们创建包时，这些文件会被复制到Conan缓存中
    exports_sources = "CMakeLists.txt", "src/*", "cmake/*"

    # --- 4. 布局：告诉Conan源码和构建目录的位置 ---
    def layout(self):
        cmake_layout(self)

    # --- 5. 生成器：为消费者项目生成集成文件 ---
    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        # 传递选项给CMake，以便在CMakeLists.txt中可以使用
        tc.variables["BUILD_TESTING"] = False # 打包时不构建测试
        tc.generate()

    # --- 6. 构建：描述如何从源码编译你的包 ---
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    # --- 7. 打包：描述如何从构建目录中收集产物 ---
    def package(self):
        # 这个方法会将文件从构建目录复制到最终的包目录
        # 我们在这里实际上是调用了CMake的安装步骤！
        cmake = CMake(self)
        cmake.install()

    # --- 8. 包信息：描述如何让消费者使用你的包 ---
    def package_info(self):
        # 这一步至关重要，它定义了消费者需要知道的一切

        # 告诉消费者，我们的库名叫 "my_lib"
        # Conan会自动处理好 .lib/.a 后缀和前缀
        self.cpp_info.libs = ["my_lib"]

        # 告诉消费者，需要链接到我们包的依赖项
        # 这是通过 requires="fmt/..." 自动处理的，但如果需要可以手动添加
        # self.cpp_info.requires = ["fmt::fmt", "spdlog::spdlog"]