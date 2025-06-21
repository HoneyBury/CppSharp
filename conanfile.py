# conanfile.py
from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.errors import ConanException

class MyProjectConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("fmt/10.2.1")
        self.requires("spdlog/1.12.0")
        self.requires("gtest/1.14.0")

    def layout(self):
        # 这是现代Conan 2.0的最佳实践。
        # 它将根据构建类型（Debug/Release）自动配置构建和生成器目录。

        # 检查 build_type 是否被设置。这是一个好习惯。
        if not self.settings.build_type:
            raise ConanException("Build type not set. Please specify with '-s build_type=Debug' or '-s build_type=Release'")

        # 根据构建类型，将文件夹设置为 "build/debug" 或 "build/release"
        build_type_folder = str(self.settings.build_type).lower()
        self.folders.build = f"build/{build_type_folder}"

        # 关键：将生成器目录设置为与构建目录相同。
        # 这可以确保 conan_toolchain.cmake 直接生成在 build/debug 或 build/release 目录下。
        self.folders.generators = self.folders.build