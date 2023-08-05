include(CMakeParseArguments)


function(copy_and_convert2to3 CONVERTED_FILES OUTPUT_DIR)
    foreach(file_name ${ARGN})
        set(py_source "${CMAKE_CURRENT_LIST_DIR}/${file_name}")
        set(py_converted "${OUTPUT_DIR}/${file_name}")

        if(PYTHON_VERSION_MAJOR GREATER 2)
            # Call 2to3 as a cmake script because it's the only
            # portable way to quiet stdout and stderr.
            set(command2to3 ${CMAKE_COMMAND}
                -DPYTHON_EXEC=${PYTHON_EXECUTABLE}
                -DFILE=${py_converted}
                -P ${CMAKE_SOURCE_DIR}/cmake/Python2to3.cmake)
        endif()

        add_custom_command(OUTPUT ${py_converted}
                           COMMAND ${CMAKE_COMMAND} -E copy ${py_source} ${py_converted}
                           COMMAND ${command2to3}
                           DEPENDS ${py_source})

        list(APPEND converted_files ${py_converted})
    endforeach()

    set(${CONVERTED_FILES} ${converted_files} PARENT_SCOPE)
endfunction()


function(bp_add_py_test NAME)
    set(multi_value_args PY_RUN PY_SOURCES CPP_SOURCES DEPENDS)
    cmake_parse_arguments(OPT "" "" "${multi_value_args}" ${ARGN})

    if(NOT OPT_PY_RUN)
        set(OPT_PY_RUN "${NAME}.py")
    endif()
    if(NOT OPT_CPP_SOURCES AND NOT OPT_DEPENDS)
        set(OPT_CPP_SOURCES "${NAME}.cpp")
    endif()

    set(output_dir ${CMAKE_CURRENT_BINARY_DIR}/${NAME})
    copy_and_convert2to3(converted_files ${output_dir} ${OPT_PY_SOURCES} ${OPT_PY_RUN})
    add_custom_target(${NAME} DEPENDS ${converted_files})
    add_dependencies(check ${NAME})

    foreach(source_file ${OPT_CPP_SOURCES})
        get_filename_component(source_name ${source_file} NAME_WE)
        if("${source_name}.py" STREQUAL "${OPT_PY_RUN}")
            set(ext_name "${source_name}_ext")
        else()
            set(ext_name ${source_name})
        endif()

        boost_python_add_module(${ext_name} BP_SHARED ${source_file})
        add_dependencies(${NAME} ${ext_name})

        set_warning_level(${ext_name})
        set_target_properties(${ext_name} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${output_dir})

        # output_dir != TARGET_FILE_DIR on some build systems
        list(APPEND python_path $<TARGET_FILE_DIR:${ext_name}>)
    endforeach()

    foreach(target ${OPT_DEPENDS})
        add_dependencies(${NAME} ${target})
        list(APPEND python_path $<TARGET_FILE_DIR:${target}>)
    endforeach()

    add_test(NAME ${NAME} COMMAND ${PYTHON_EXECUTABLE} "${output_dir}/${OPT_PY_RUN}")

    # Make sure the executed python script can find the cpp modules.
    list(APPEND python_path $ENV{PYTHONPATH})
    if(WIN32)
        string(REPLACE ";" "\\;" python_path "${python_path}")
    else()
        string(REPLACE ";" ":" python_path ${python_path})
    endif()
    set_property(TEST ${NAME} APPEND PROPERTY ENVIRONMENT "PYTHONPATH=${python_path}")

    if(WIN32)
        set(path $<TARGET_FILE_DIR:boost_python_shared> $ENV{PATH})
        string(REPLACE ";" "\\;" path "${path}")
        set_property(TEST ${NAME} APPEND PROPERTY ENVIRONMENT "PATH=${path}")
    endif()
endfunction()


function(bp_add_exe_test NAME)
    set(options STATIC SHARED SUPPRESS_REGISTRY)
    set(multi_value_args PY_SOURCES CPP_SOURCES DEPENDS)
    cmake_parse_arguments(OPT "${options}" "" "${multi_value_args}" ${ARGN})

    if(NOT OPT_CPP_SOURCES)
        set(OPT_CPP_SOURCES "${NAME}.cpp")
    endif()

    if (OPT_SHARED)
        boost_python_add_executable(${NAME} BP_SHARED ${OPT_CPP_SOURCES})
    else()
        boost_python_add_executable(${NAME} ${OPT_CPP_SOURCES})
    endif()

    add_dependencies(check ${NAME})
    set_warning_level(${NAME})

    set(output_dir ${CMAKE_CURRENT_BINARY_DIR}/${NAME})
    set_target_properties(${NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${output_dir})

    if(OPT_SUPPRESS_REGISTRY)
        target_compile_definitions(${NAME} PUBLIC BOOST_PYTHON_SUPPRESS_REGISTRY_INITIALIZATION)
    endif()

    copy_and_convert2to3(converted_files ${output_dir} ${OPT_PY_SOURCES})
    if(OPT_PY_SOURCES)
        add_custom_target(${NAME}_py DEPENDS ${converted_files})
        add_dependencies(${NAME} ${NAME}_py)
    endif()

    add_test(NAME ${NAME} COMMAND ${NAME} ${OPT_PY_SOURCES} WORKING_DIRECTORY ${output_dir})

    if(WIN32 AND OPT_SHARED)
        set(path $<TARGET_FILE_DIR:boost_python_shared> $ENV{PATH})
        string(REPLACE ";" "\\;" path "${path}")
        set_property(TEST ${NAME} APPEND PROPERTY ENVIRONMENT "PATH=${path}")
    endif()
endfunction()

function(bp_add_compile_test NAME)
    cmake_parse_arguments(OPT "WILL_FAIL" "" "CPP_SOURCES" ${ARGN})

    if(NOT OPT_CPP_SOURCES)
        set(OPT_CPP_SOURCES "${NAME}.cpp")
    endif()

    add_library(${NAME} OBJECT ${OPT_CPP_SOURCES})
    set_warning_level(${NAME})

    # inherit properties from boost_python_static
    target_include_directories(${NAME} PUBLIC
                               $<TARGET_PROPERTY:boost_python_static,INCLUDE_DIRECTORIES>)
    target_compile_definitions(${NAME} PUBLIC
                               $<TARGET_PROPERTY:boost_python_static,INTERFACE_COMPILE_DEFINITIONS>)
    target_compile_options(${NAME} PUBLIC
                           $<TARGET_PROPERTY:boost_python_static,INTERFACE_COMPILE_OPTIONS>)

    if(MSVC)
        set(prefix test/)
    endif()
    add_test(NAME ${NAME}
             COMMAND ${CMAKE_COMMAND} --build . --target ${prefix}${NAME} --config $<CONFIG>
             WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

    if(OPT_WILL_FAIL)
        set_tests_properties(${NAME} PROPERTIES WILL_FAIL TRUE)
    endif()
endfunction()
