# conanfile.py
import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout

class MyProjectConan(ConanFile):
    name = "myproject"
    version = "1.0.0"

    # Package metadata
    license = "MIT"
    author = "Your Name <you@example.com>"
    url = "https://github.com/your-repo/myproject"
    description = "A modern C++ project template."
    topics = ("cpp", "cmake", "conan", "template")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "cmake/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        # 强制在所有情况下都使用扁平的构建目录结构
        # 即，生成器文件直接放在构建目录的根下
        self.folders.build = "build"
        self.folders.generators = "build/generators" # 保持默认，让CMakeToolchain去处理
        # 不对，这样还是有问题。让我们用最直接的方式。

        # 让我们回到之前对本地开发有效的那个layout
        build_type_folder = str(self.settings.build_type).lower() if self.settings.build_type else "default"
        self.folders.build = f"build/{build_type_folder}"
        self.folders.generators = self.folders.build

    def generate(self):
        # This is the most important part for consumers and for `conan create`
        # It generates the conan_toolchain.cmake and the XXX-config.cmake files
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        # We can pass options to CMake
        tc.variables["BUILD_TESTING"] = False
        tc.generate()

    def build(self):
        # Standard build implementation
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # This will run `cmake --install .`
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        # This will be used by the consumers of this package
        self.cpp_info.libs = ["my_lib"]