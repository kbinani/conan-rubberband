project(rubberband)
cmake_minimum_required(VERSION 2.8)

file(GLOB rubberband_src
    "src/audiocurves/*.*"
    "src/base/*.*"
    "src/dsp/*.*"
    "src/float_cast/*.*"
    "src/kissfft/*.*"
    "src/pommier/*.*"
    "src/speex/*.*"
    "src/system/*.*"
    "src/*.*"
)

add_library(rubberband ${rubberband_src})

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/src)

# Macro definitions
if (MSVC)
    add_definitions(-D__MSVC__ -DNOMINMAX)
elseif(APPLE)
    add_definitions(-DUSE_PTHREADS -DMALLOC_IS_ALIGNED)
else()
    add_definitions(-DUSE_PTHREADS)
endif()
add_definitions(-D_LIB -D_USE_MATH_DEFINES -DUSE_KISSFFT -DUSE_SPEEX)

# CXX_FLAGS
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG -DNO_THREAD_CHECKS -DNO_TIMING")
if (MSVC)
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /fp:fast /arch:SSE /Ox /Ob2 /Oi /Ot /Oy /Gm- /GS- /Zi /W2")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /Od /Gm /ZI /W2")
else()
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -ffast-math -mfpmath=sse -msse -msse2 -O3 -ftree-vectorize")
endif()
