cmake_minimum_required(VERSION 3.0)
project(boost_python)

include(CMakeParseArguments)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

find_package(PythonLibsNew ${PYTHON_VERSION} REQUIRED)

# evil glob - to be fixed
file(GLOB_RECURSE srcs FOLLOW_SYMLINKS include/*.hpp src/*.cpp)

# static
add_library(boost_python_static STATIC EXCLUDE_FROM_ALL ${srcs})
target_compile_definitions(boost_python_static PUBLIC BOOST_PYTHON_STATIC_LIB)
set_target_properties(boost_python_static PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

# shared
add_library(boost_python_shared SHARED EXCLUDE_FROM_ALL ${srcs})
target_compile_definitions(boost_python_shared PUBLIC BOOST_PYTHON_DYNAMIC_LIB)
if(APPLE)
    target_link_libraries(boost_python_shared PRIVATE "-undefined dynamic_lookup")
    target_link_libraries(boost_python_shared PUBLIC "-Wl,-single_module")
endif()

# Common warning level for library and tests
function(set_warning_level TARGET)
    if(WIN32)
        target_compile_options(${TARGET} PRIVATE /W3)
    else()
        target_compile_options(${TARGET} PRIVATE -Wall -Wextra)
    endif()
endfunction()

foreach(target boost_python_static boost_python_shared)
    set_warning_level(${target})

    target_include_directories(${target} SYSTEM PUBLIC
                               ${PROJECT_SOURCE_DIR}/include
                               ${PYTHON_INCLUDE_DIRS})

    target_compile_definitions(${target} PUBLIC BOOST_ALL_NO_LIB)
    target_compile_definitions(${target} PRIVATE BOOST_PYTHON_SOURCE)

    # MSVC does not require a flag to enable C++11 features.
    # It would be cleaner to do this with target_compiler_features,
    # but this would completely break the build on compilers which
    # CMake does not explicitly support (like Intel's).
    if(NOT WIN32)
        target_compile_options(${target} PUBLIC -std=c++11)
    endif()

    # On Unix-like systems only executables need to link to libpython,
    # but on Windows everything should always link to Python.
    if(WIN32)
        target_link_libraries(${target} PUBLIC ${PYTHON_LIBRARIES})
    endif()
endforeach()

# Build a Python extension module:
# boost_python_add_module(<name> [BP_SHARED] [EXCLUDE_FROM_ALL]
#                         source1 [source2 ...])
#
# BP_SHARED specifies that boost_python should be build as a shared library
# and linked to the Python extension module. If no given, boost_python will
# be static and included inside the Python extension module.
# Note: The Python extension itself is always defined as a MODULE and is not
# affected by BP_SHARED in any way.
function(boost_python_add_module TARGET)
    cmake_parse_arguments(OPT "BP_SHARED" "" "" ${ARGN})

    add_library(${TARGET} MODULE ${OPT_UNPARSED_ARGUMENTS})
    if (OPT_BP_SHARED)
        target_link_libraries(${TARGET} PUBLIC boost_python_shared)
    else()
        target_link_libraries(${TARGET} PUBLIC boost_python_static)
    endif()

    # Prefix and extension provided by FindPythonLibsNew.cmake
    set_target_properties(${TARGET} PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}")
    set_target_properties(${TARGET} PROPERTIES SUFFIX "${PYTHON_MODULE_EXTENSION}")

    # Don't link to libpython on Unix because the python interpreter
    # will provide all the required symbols for the extension module.
    # However, OS X doesn't like undefined symbols by default, but
    # this flag puts it in line with other Unix-like systems.
    if(APPLE)
        target_link_libraries(${TARGET} PRIVATE "-undefined dynamic_lookup")
    endif()
endfunction()

# Build an executable with embedded Python:
# boost_python_add_executable(<name> [BP_SHARED] [EXCLUDE_FROM_ALL]
#                             source1 [source2 ...])
#
# BP_SHARED specifies that boost_python should be build as a shared library.
# Otherwise, it will be statically linked.
function(boost_python_add_executable TARGET)
    cmake_parse_arguments(OPT "BP_SHARED" "" "" ${ARGN})

    add_executable(${TARGET} ${OPT_UNPARSED_ARGUMENTS})
    if (OPT_BP_SHARED)
        target_link_libraries(${TARGET} PUBLIC boost_python_shared)
    else()
        target_link_libraries(${TARGET} PUBLIC boost_python_static)
    endif()

    # On Windows libpython is inherited from boost_python.
    if(NOT WIN32)
        target_link_libraries(${TARGET} PUBLIC ${PYTHON_LIBRARIES})
    endif()
endfunction()

if(EXISTS ${PROJECT_SOURCE_DIR}/test)
    enable_testing()
    add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND} -C $<CONFIG>)
    add_subdirectory(test EXCLUDE_FROM_ALL)
endif()
