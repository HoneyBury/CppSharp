# ./CMakeLists.txt

# 1. 设置CMake最低版本和项目信息
cmake_minimum_required(VERSION 3.15)
project(Project VERSION 1.0.0 LANGUAGES CXX)
# =================== 新增部分：健壮的输出目录设置 (最终版) ===================
# 包含此模块以使用 CMAKE_CFG_INTDIR 变量，它能优雅地处理
# 单配置（如Makefile）和多配置（如Visual Studio）生成器。
include(GNUInstallDirs)

# 对于可执行文件 (runtime)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR})

# 对于库文件 (archive for static, library for shared)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})

# 对于Visual Studio（多配置生成器），需要特别处理以避免创建额外的Debug/Release子目录
foreach(config ${CMAKE_CONFIGURATION_TYPES})
    string(TOUPPER ${config} config_upper)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_${config_upper} ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR})
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_${config_upper} ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_${config_upper} ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
endforeach()
# ==============================================================================

# 2. 将自定义CMake模块路径添加到搜索路径
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(utils)

# 3. Conan集成 (关键步骤)
# Conan 2.0 的现代方法是让用户在配置时通过 CMAKE_TOOLCHAIN_FILE 指定。
# 我们在这里检查它是否被设置，如果没有，就给出一个友好的错误提示。
if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan_toolchain.cmake")
    message(FATAL_ERROR "Conan toolchain file not found at '${CMAKE_BINARY_DIR}/conan_toolchain.cmake'.\n"
            "Please run 'conan install' before configuring with CMake.")
endif()

# 4. 设置全局构建选项
# 我们可以提供一个选项来决定是否构建测试
option(BUILD_TESTING "Build the tests" ON)

# 5. 添加源代码子目录
add_subdirectory(src)

# 6. 如果启用了测试，则添加测试子目录
if(BUILD_TESTING)
    # 启用CTest测试框架
    enable_testing()
    add_subdirectory(tests)
endif()

# =================== 新增：安装与打包配置 ===================
# 1. 包含CMake的打包和安装辅助模块
include(CMakePackageConfigHelpers)
include(CPack)
# 在 include(CPack) 之后添加
set(CPACK_GENERATOR "NSIS") # Windows
set(CPACK_GENERATOR "DEB")  # Debian/Ubuntu
set(CPACK_GENERATOR "RPM")  # Fedora/CentOS
set(CPACK_SOURCE_IGNORE_FILES
        "/.git/"
        "/build/"
        "/.vscode/"
        "/.idea/"
        ".DS_Store"
        "*.swp"
        "*.bak"
)

# 2. 生成 MyProjectConfigVersion.cmake 文件
#    这允许其他项目在find_package时指定版本，例如 find_package(MyProject 1.0.0 EXACT)
write_basic_package_version_file(
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY AnyNewerVersion
)

# 3. 配置并生成 MyProjectConfig.cmake 文件
#    这是find_package的核心
configure_package_config_file(
        "${PROJECT_SOURCE_DIR}/cmake/config.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)
# 4. 将生成的配置文件安装到指定位置
install(FILES
"${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
"${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)

# 5. 安装由我们导出的目标文件 (MyProjectTargets.cmake)
install(EXPORT ${PROJECT_NAME}Targets
FILE ${PROJECT_NAME}Targets.cmake
NAMESPACE ${PROJECT_NAME}::
DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)
# ==========================================================
