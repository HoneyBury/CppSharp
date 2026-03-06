function(set_project_properties target)
    target_compile_features(${target} PUBLIC cxx_std_17)

    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
        target_compile_options(${target} PRIVATE
                -Wall
                -Wextra
                -Wpedantic
                -Werror
                -Wno-unused-parameter
        )
    elseif(MSVC)
        target_compile_options(${target} PRIVATE
                /W4
                /WX
        )
    endif()

endfunction()
