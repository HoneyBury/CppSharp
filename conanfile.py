﻿# conanfile.py
# FINAL, CORRECT, AND ROBUST VERSION
# HELLO WORLD, THIS IS A TEST COMMENT TO FORCE A HASH CHANGE
import os
import re
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Version
from conan.errors import ConanException, ConanInvalidConfiguration

def get_project_data_from_cmake():
    cmakelists_path = os.path.join(os.path.dirname(__file__), "CMakeLists.txt")
    if not os.path.exists(cmakelists_path):
        raise ConanException(f"Cannot find CMakeLists.txt at {cmakelists_path}. Check your 'exports' attribute.")

    with open(cmakelists_path, "r", encoding="utf-8") as f:
        cmakelists_content = f.read()

    match = re.search(r'project\s*\(\s*(\S+)\s+VERSION\s+([^\s)]+)(?:\s+DESCRIPTION\s+"([^"]+)")?.*?\)', cmakelists_content, re.DOTALL)
    if not match:
        raise ConanException("Could not extract project name, version, or description from CMakeLists.txt")

    return {
        "name": match.group(1).lower(),
        "version": match.group(2),
        "description": match.group(3) or "A modern C++ project template."
    }

_project_data = get_project_data_from_cmake()

class MyProjectConan(ConanFile):
    """
    This is the final, correct, and robust conanfile for a modern C++ project.
    It relies on the standard, automated behaviors of Conan 2.x tools
    and dynamically loads metadata from CMakeLists.txt.
    """

    # 1. Package Metadata
    name = _project_data["name"]
    version = _project_data["version"]
    description = _project_data["description"]

    license = "MIT"
    author = "HoneyBury zoujiahe389@gmail.com"
    url = "https://github.com/HoneyBury/CppSharp.git"
    topics = ("cpp", "cmake", "conan", "template", "scaffolding")

    # 2. Binary Configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # =============================== 关键改动 ===============================
    # `exports` 确保配方解析时 CMakeLists.txt 可用。
    exports = "CMakeLists.txt"
    # `exports_sources` 确保构建时 CMakeLists.txt 和其他源码被复制到源目录。
    # 扩展 `exports_sources` 以包含所有构建时需要的文件
    # 使用元组可以更清晰地分行
    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "cmake/*",
        "tests/*",
        "assets/*",
        "LICENSE",
        "README.md",
    )
    # =======================================================================

    # 4. Requirements
    def requirements(self):
        """这些是库本身在运行时或编译时真正需要的、需要传递给消费者的依赖。"""
        self.output.info("<<<<<< RUNNING requirements() METHOD >>>>>>")
        self.requires("fmt/10.2.1", visible=True)
        self.requires("spdlog/1.12.0", visible=True)
        self.requires("gtest/1.14.0")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if not self.settings.get_safe("compiler.cppstd"):
            self.settings.compiler.cppstd = "17"

    def validate(self):
        if self.settings.compiler.cppstd:
            if Version(self.settings.compiler.cppstd) < "14":
                raise ConanInvalidConfiguration("MyProject requires at least C++14.")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]
    # =====================================================================