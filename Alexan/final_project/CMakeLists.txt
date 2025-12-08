cmake_minimum_required(VERSION 3.10)
project(final_project)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
    argparse
    GIT_REPOSITORY https://github.com/morrisfranken/argparse.git
    GIT_TAG master
)
FetchContent_MakeAvailable(argparse)

# Find GMP (system library, should be pre-installed)
find_package(PkgConfig REQUIRED)
pkg_check_modules(GMP gmpxx gmp)

# If GMP not found, give helpful error message
if(NOT GMP_FOUND)
    message(FATAL_ERROR 
        "GMP library not found!\n"
        "Please install it:\n"
        "  Ubuntu/Debian: sudo apt-get install libgmp-dev\n"
        "  macOS:         brew install gmp\n"
        "  Windows:       See https://gmplib.org/\n"
    )
endif()

add_executable(finalproject
    src/main.cpp
    src/crypto_utils.cpp
    src/string_utils.cpp
    src/BBSRandom.cpp
    src/Bootstrap.cpp
    src/Cipher.cpp
    src/ElGamal.cpp
    src/RSA.cpp
)

# Include directories
target_include_directories(finalproject PRIVATE 
    ${argparse_SOURCE_DIR}/include
    ${GMP_INCLUDE_DIRS}
)

# Link libraries
target_link_libraries(finalproject 
    ${GMP_LIBRARIES}
)

# Output directory
set_target_properties(finalproject PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin"
)