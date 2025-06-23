# ./CMakeLists.txt

# 1. 设置CMake最低版本和项目信息
cmake_minimum_required(VERSION 3.15)
project(Project VERSION 1.0.2 LANGUAGES CXX)
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




# 4. 设置全局构建选项
# 我们可以提供一个选项来决定是否构建测试
option(BUILD_TESTING "Build the tests" OFF)

# 5. 添加源代码子目录
add_subdirectory(src)

# 6. 如果启用了测试，则添加测试子目录
if(BUILD_TESTING)
    # 启用CTest测试框架
    enable_testing()
    add_subdirectory(tests)
endif()

# =================== 新增：安装与打包配置 (最终修正版) ===================
# 1. 包含CMake的打包和安装辅助模块
include(CMakePackageConfigHelpers)
include(CPack)

# 2. 根据操作系统，条件性地设置 CPack 生成器
if(WIN32)
  # 在 Windows 上，使用 NSIS 创建 .exe 安装程序
  set(CPACK_GENERATOR "NSIS")
elseif(UNIX AND NOT APPLE)
  # 在 Linux (GitHub Actions 的 runner 是基于 Debian/Ubuntu 的) 上，创建 .deb 包
  set(CPACK_GENERATOR "DEB")
elseif(APPLE)
  # 在 macOS 上，创建用户友好的 .dmg 拖拽安装包
  set(CPACK_GENERATOR "DragNDrop")
endif()

# 3. 设置通用的包元数据 (强烈推荐)
set(CPACK_PACKAGE_NAME "${PROJECT_NAME}")
set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PROJECT_DESCRIPTION}")
set(CPACK_PACKAGE_VENDOR "MyProject Inc.")
set(CPACK_PACKAGE_CONTACT "${PROJECT_AUTHOR}")
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE") # 假设你有一个LICENSE文件
set(CPACK_RESOURCE_FILE_README "${CMAKE_CURRENT_SOURCE_DIR}/README.md") # 假设你有一个README.md

# 4. 设置 DEB 包的特定元数据 (可选，但推荐)
if(CPACK_GENERATOR STREQUAL "DEB")
  set(CPACK_DEBIAN_PACKAGE_MAINTAINER "${PROJECT_AUTHOR}")
  set(CPACK_DEBIAN_PACKAGE_SECTION "devel")
  set(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")
endif()

# 5. 设置 NSIS 安装程序的特定元数据 (可选)
if(CPACK_GENERATOR STREQUAL "NSIS")
  set(CPACK_NSIS_DISPLAY_NAME "${CPACK_PACKAGE_NAME} ${CPACK_PACKAGE_VERSION}")
  set(CPACK_NSIS_PUBLISHER "${CPACK_PACKAGE_VENDOR}")
  set(CPACK_NSIS_URL_INFO_ABOUT "${PROJECT_URL}")
endif()

# 6. 设置源文件打包时要忽略的文件
set(CPACK_SOURCE_IGNORE_FILES
    "/.git/"
    "/build/"
    "/.vscode/"
    "/.idea/"
    ".DS_Store"
    "*.swp"
    "*.bak"
)

# 7. 生成 MyProjectConfigVersion.cmake 文件
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)

# 8. 配置并生成 MyProjectConfig.cmake 文件
configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/cmake/config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)

# 9. 将生成的配置文件安装到指定位置
install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)

# 10. 安装由我们导出的目标文件 (MyProjectTargets.cmake)
install(EXPORT ${PROJECT_NAME}Targets
    FILE ${PROJECT_NAME}Targets.cmake
    NAMESPACE ${PROJECT_NAME}::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)
# ==========================================================================