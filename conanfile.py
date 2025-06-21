# conanfile.py
from conan import ConanFile
from conan.tools.cmake import cmake_layout

class MyProjectConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        """
        在此处定义项目的所有第三方依赖。
        Conan会自动处理依赖的依赖（传递性依赖）。
        例如，spdlog 依赖 fmt，Conan会一起下载。
        """
        # 一个高性能的格式化库，C++20 std::format 的基础
        self.requires("fmt/10.2.1")
        # 一个非常流行的日志库
        self.requires("spdlog/1.12.0")
        # Google Test 单元测试框架
        self.requires("gtest/1.14.0")

    def layout(self):
        """
        定义项目布局，告诉Conan源码和构建目录的位置。
        这有助于简化命令行操作。
        """
        cmake_layout(self)