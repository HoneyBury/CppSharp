import os
import re

from conan import ConanFile
from conan.errors import ConanException, ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.scm import Version


def get_project_data_from_cmake() -> dict:
    cmakelists_path = os.path.join(os.path.dirname(__file__), "CMakeLists.txt")
    if not os.path.exists(cmakelists_path):
        raise ConanException(f"Cannot find CMakeLists.txt at: {cmakelists_path}")

    with open(cmakelists_path, "r", encoding="utf-8-sig") as file:
        content = file.read()

    pattern = r'project\s*\(\s*(\S+)\s+VERSION\s+([^\s)]+)(?:\s+DESCRIPTION\s+"([^"]+)")?.*?\)'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ConanException("Failed to parse project metadata from CMakeLists.txt")

    return {
        "name": match.group(1).lower(),
        "version": match.group(2),
        "description": match.group(3) or "A modern C++ project template.",
    }


_project_data = get_project_data_from_cmake()


class CppSharpConan(ConanFile):
    name = _project_data["name"]
    version = _project_data["version"]
    description = _project_data["description"]

    license = "MIT"
    author = "HoneyBury zoujiahe389@gmail.com"
    url = "https://github.com/HoneyBury/CppSharp.git"
    topics = ("cpp", "cmake", "conan", "template", "scaffolding")

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports = "CMakeLists.txt"
    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "cmake/*",
        "tests/*",
        "assets/*",
        "LICENSE",
        "README.md",
    )

    def requirements(self) -> None:
        self.requires("fmt/10.2.1", visible=True)
        self.requires("spdlog/1.12.0", visible=True)
        self.requires("gtest/1.14.0")

    def config_options(self) -> None:
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self) -> None:
        if not self.settings.get_safe("compiler.cppstd"):
            self.settings.compiler.cppstd = "17"

    def validate(self) -> None:
        if self.settings.compiler.cppstd and Version(self.settings.compiler.cppstd) < "14":
            raise ConanInvalidConfiguration("CppSharp requires at least C++14.")

    def layout(self) -> None:
        cmake_layout(self)

    def generate(self) -> None:
        deps = CMakeDeps(self)
        deps.generate()

        toolchain = CMakeToolchain(self)
        toolchain.generate()

    def build(self) -> None:
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self) -> None:
        cmake = CMake(self)
        cmake.install()

    def package_info(self) -> None:
        self.cpp_info.libs = [self.name]
