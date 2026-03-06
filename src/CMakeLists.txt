add_library(${PROJECT_NAME} STATIC
        cppsharp/my_lib.cpp
        cppsharp/my_lib.hpp
)

target_include_directories(${PROJECT_NAME}
        PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        PRIVATE
)
set_project_properties(${PROJECT_NAME})

find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)

target_link_libraries(${PROJECT_NAME} PUBLIC
        fmt::fmt
        spdlog::spdlog
)

install(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}Targets
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
install(FILES cppsharp/my_lib.hpp DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME})

add_executable(app
        main.cpp
)

target_link_libraries(app PRIVATE ${PROJECT_NAME})

set_project_properties(app)

install(TARGETS app
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
