# src/CMakeLists.txt

# 1. 创建我们的核心库 (my_lib)
add_library(my_lib STATIC
        my_lib/my_lib.cpp
        my_lib/my_lib.hpp
)
# 使用 STATIC, SHARED, 或 INTERFACE (仅头文件)

# 2. 设置 my_lib 的属性
target_include_directories(my_lib
        PUBLIC
        # $<BUILD_INTERFACE:...> 生成器表达式：
        # 这个路径只在从源码构建时（即在同一个CMake项目中）才会被添加到包含目录中。
        # 当库被安装和导出后，这个路径会自动被忽略。
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>

        PRIVATE
        # 如果有任何只用于 my_lib 内部实现的头文件目录，可以放在这里。
)
set_project_properties(my_lib)

# 3. 链接 my_lib 所需的第三方库
# Conan 生成的目标名通常是 <package_name>::<component_name>
# 对于 fmt 和 spdlog，通常是 fmt::fmt 和 spdlog::spdlog
find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)

target_link_libraries(my_lib PUBLIC
        fmt::fmt
        spdlog::spdlog
)
# --- 新增：为 my_lib 库添加安装规则 ---
# PUBLIC_HEADER：指定哪些头文件是公开的API，需要被安装。
# DESTINATION：指定安装的目标子目录。
install(TARGETS my_lib
        EXPORT ${PROJECT_NAME}Targets # 导出目标，以便其他CMake项目可以find_package(MyProject)
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} # 静态库 (.lib, .a) 的安装位置
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} # 动态库 (.dll, .so) 的安装位置
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # DLL的运行时依赖 (Windows)
        #PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/my_lib # 公开的头文件
        # 新增：告诉CMake安装后的目标，它的头文件在相对于安装前缀的 include 目录下
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
install(FILES my_lib/my_lib.hpp DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/my_lib)


# ... add_executable(app ...) ...
# ... target_link_libraries(app ...) ...


# 4. 创建主可执行文件 (app)
add_executable(app
        main.cpp
)

# 5. 链接 app 到我们的核心库
target_link_libraries(app PRIVATE my_lib)

# 6. 应用我们定义的通用编译选项
set_project_properties(app)

install(TARGETS app
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # 可执行文件 (.exe) 的安装位置
)