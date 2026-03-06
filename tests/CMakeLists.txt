find_package(GTest REQUIRED)

add_executable(unit_tests
        main_test.cpp
)

target_link_libraries(unit_tests PRIVATE
        ${PROJECT_NAME}
        GTest::gtest_main
)

set_project_properties(unit_tests)

include(GoogleTest)

gtest_discover_tests(unit_tests)
