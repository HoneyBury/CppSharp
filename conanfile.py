# conanfile.py
# FINAL AND CORRECT VERSION
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout

class MyProjectConan(ConanFile):
    """
    This is the final, correct, and robust conanfile for a modern C++ project.
    It relies on the standard, automated behaviors of Conan 2.x tools.
    """

    # 1. Package Metadata
    name = "myproject"
    version = "1.0.2"
    license = "MIT"
    author = "Your Name <you@example.com>"
    url = "https://github.com/your-repo/myproject"
    description = "A modern C++ project template using Conan and CMake."
    topics = ("cpp", "cmake", "conan", "template", "scaffolding")

    # 2. Binary Configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # 3. Requirements
    def requirements(self):
        self.requires("fmt/10.2.1")
        self.requires("spdlog/1.12.0")
        self.requires("gtest/1.14.0")

    # 4. Source Export
    exports_sources = "CMakeLists.txt", "src/*", "cmake/*"

    # 5. Option Configuration
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    # 6. Layout
    def layout(self):
        # Use the standard cmake_layout. This is the most robust choice.
        cmake_layout(self)

    # 7. Generators
    def generate(self):
        # The CMakeToolchain will AUTOMATICALLY generate the CMakePresets.json file.
        # We do not need to import or call any 'CMakePresets' class.
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    # 8. Build
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    # 9. Package
    def package(self):
        cmake = CMake(self)
        cmake.install()

    # 10. Package Info
    def package_info(self):
        self.cpp_info.libs = ["my_lib"]