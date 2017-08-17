cmake_minimum_required(VERSION 2.6)
project(modularnn)
INCLUDE(FindPkgConfig)

IF(CMAKE_COMPILER_IS_GNUCC)
SET(CMAKE_CXX_FLAGS
"${CMAKE_CXX_FLAGS} -Wall -std=c++0x -DBUILD_SHARED_LIBS=OFF")
ENDIF(CMAKE_COMPILER_IS_GNUCC)

# definicoes da remoteAPI para CPP
add_definitions(-DNON_MATLAB_PARSING)
add_definitions(-DMAX_EXT_API_CONNECTIONS=255)

set(SOURCES
    remoteApi/extApi.c
    #remoteApi/extApiCustom.c
    remoteApi/extApiPlatform.c
   
)
 
set(HEADERS
    remoteApi/extApi.h
    #remoteApi/extApiCustom.h
    remoteApi/extApiInternal.h
    remoteApi/extApiPlatform.h
    include/v_repConst.h
    include/v_repLib.h
    Cinematica.h
    Modulo.h
    RedeNeuralModular.h
)
include_directories("include/")
include_directories("remoteApi/")

find_package (Threads)

add_executable(modularnn 
               main.cpp 
               ${SOURCES}
	       ${HEADERS})
	       
target_link_libraries (modularnn ${CMAKE_THREAD_LIBS_INIT})

install(TARGETS modularnn RUNTIME DESTINATION bin)
