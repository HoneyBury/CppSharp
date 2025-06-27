# conanfile.py
# FINAL, CORRECT, AND DYNAMIC VERSION
import os
import re
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Version
from conan.errors import ConanInvalidConfiguration

class MyProjectConan(ConanFile):
    """
    This is the final, correct, and robust conanfile for a modern C++ project.
    It relies on the standard, automated behaviors of Conan 2.x tools
    and dynamically loads metadata from CMakeLists.txt.
    """

    # 1. Package Metadata (大部分将从CMakeLists.txt动态加载)
    # name 和 version 将在 load() 方法中设置
    license = "MIT"
    author = "HoneyBury zoujiahe389@gmail.com"
    url = "https://github.com/HoneyBury/CppSharp.git"
    # description 也会在 load() 中设置
    topics = ("cpp", "cmake", "conan", "template", "scaffolding")

    # 2. Binary Configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # 3. Source Export
    # 必须导出 CMakeLists.txt，因为我们需要读取它
    exports_sources = "CMakeLists.txt", "src/*", "cmake/*"

    # ============================ 新增部分: 动态加载元数据 ============================
    def load(self, conanfile_path):
        """
        这个方法在配方处理的早期被调用，非常适合从外部文件加载数据。
        """
        # 读取 CMakeLists.txt 文件内容
        cmakelists_path = os.path.join(self.recipe_folder, "CMakeLists.txt")
        with open(cmakelists_path, "r") as f:
            cmakelists_content = f.read()

        # 使用正则表达式从 project() 命令中提取信息
        # project(Project VERSION 2.0.0 DESCRIPTION "Some desc")
        match = re.search(r'project\s*\(\s*(\S+)\s+VERSION\s+([^\s)]+)(?:\s+DESCRIPTION\s+"([^"]+)")?\s*\)', cmakelists_content)

        if not match:
            raise ConanInvalidConfiguration("Could not extract project name, version, or description from CMakeLists.txt")

        # 将提取到的值赋给 Conan 的属性
        self.name = match.group(1)
        self.version = match.group(2)
        # 如果有 DESCRIPTION，就用它；否则保持一个默认值
        self.description = match.group(3) or "A modern C++ project template."
        self.output.info(f"Loaded from CMake: name='{self.name}' version='{self.version}'")
    # ==============================================================================

    # 4. Requirements
    def requirements(self):
        self.requires("fmt/10.2.1")
        self.requires("spdlog/1.12.0")
        self.requires("gtest/1.14.0")

    # 5. Option Configuration
    def config_options(self):
        if self.settings.os == "Windows":
            # 在Windows上移除 fPIC 选项
            self.options.rm_safe("fPIC")

    # 6. Configure (更适合处理值和设置的地方)
    def configure(self):
        # 如果用户没有在profile中指定C++标准，我们设置一个默认值
        if not self.settings.get_safe("compiler.cppstd"):
            self.settings.compiler.cppstd = "17"

    # 7. Validate (保持不变)
    def validate(self):
        # 限制最低标准
        if self.settings.compiler.cppstd:
            if Version(self.settings.compiler.cppstd) < "14":
                raise ConanInvalidConfiguration("MyProject requires at least C++17.")

    # 8. Layout (保持不变)
    def layout(self):
        cmake_layout(self)

    # 9. Generators (保持不变)
    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    # 10. Build (保持不变)
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    # 11. Package (保持不变)
    def package(self):
        cmake = CMake(self)
        cmake.install()

    # 12. Package Info (保持不变)
    def package_info(self):
        self.cpp_info.libs = ["my_lib"]