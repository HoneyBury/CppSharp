# tests/CMakeLists.txt

# 1. 查找GTest，这是由Conan提供的
find_package(GTest REQUIRED)

# 2. 创建测试可执行文件
add_executable(run_tests
        main_test.cpp
)

# 3. 链接测试程序到我们的核心库和GTest
target_link_libraries(run_tests PRIVATE
        my_lib          # 链接我们要测试的库
        GTest::gtest_main # GTest库，它包含了main函数和所有测试功能
)
# 注意: GTest::gtest_main 包含了 gtest 和 gtest_main
# 如果你自己写 main 函数，可以只链接 GTest::gtest

# 4. 应用通用编译选项
set_project_properties(run_tests)

# 5. 自动发现并添加测试到CTest
# 这是现代CMake集成GTest的推荐方式
include(GoogleTest)
gtest_discover_tests(run_tests)

# (可选) 设置输出目录
set_target_properties(run_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")