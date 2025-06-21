# src/CMakeLists.txt

# 1. 创建我们的核心库 (my_lib)
add_library(my_lib STATIC
        my_lib/my_lib.cpp
        my_lib/my_lib.hpp
)
# 使用 STATIC, SHARED, 或 INTERFACE (仅头文件)

# 2. 设置 my_lib 的属性
# PUBLIC: 使用 my_lib 的目标和 my_lib 自身都需要这个包含目录
# INTERFACE: 只有使用 my_lib 的目标才需要这个包含目录
# PRIVATE: 只有 my_lib 自身构建时需要
target_include_directories(my_lib PUBLIC
        # 允许 #include "my_lib/my_lib.hpp"
        ${CMAKE_CURRENT_SOURCE_DIR}
)
# 应用我们定义的通用编译选项
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

# 4. 创建主可执行文件 (app)
add_executable(app
        main.cpp
)

# 5. 链接 app 到我们的核心库
target_link_libraries(app PRIVATE my_lib)

# 6. 应用我们定义的通用编译选项
set_project_properties(app)

# 7. (可选) 设置输出目录，使结构更整洁
#set_target_properties(app PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")