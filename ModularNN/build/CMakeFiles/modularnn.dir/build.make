# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build

# Include any dependencies generated for this target.
include CMakeFiles/modularnn.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/modularnn.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/modularnn.dir/flags.make

CMakeFiles/modularnn.dir/main.cpp.o: CMakeFiles/modularnn.dir/flags.make
CMakeFiles/modularnn.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/modularnn.dir/main.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/modularnn.dir/main.cpp.o -c /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/main.cpp

CMakeFiles/modularnn.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/modularnn.dir/main.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/main.cpp > CMakeFiles/modularnn.dir/main.cpp.i

CMakeFiles/modularnn.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/modularnn.dir/main.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/main.cpp -o CMakeFiles/modularnn.dir/main.cpp.s

CMakeFiles/modularnn.dir/main.cpp.o.requires:

.PHONY : CMakeFiles/modularnn.dir/main.cpp.o.requires

CMakeFiles/modularnn.dir/main.cpp.o.provides: CMakeFiles/modularnn.dir/main.cpp.o.requires
	$(MAKE) -f CMakeFiles/modularnn.dir/build.make CMakeFiles/modularnn.dir/main.cpp.o.provides.build
.PHONY : CMakeFiles/modularnn.dir/main.cpp.o.provides

CMakeFiles/modularnn.dir/main.cpp.o.provides.build: CMakeFiles/modularnn.dir/main.cpp.o


CMakeFiles/modularnn.dir/remoteApi/extApi.c.o: CMakeFiles/modularnn.dir/flags.make
CMakeFiles/modularnn.dir/remoteApi/extApi.c.o: ../remoteApi/extApi.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/modularnn.dir/remoteApi/extApi.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/modularnn.dir/remoteApi/extApi.c.o   -c /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/remoteApi/extApi.c

CMakeFiles/modularnn.dir/remoteApi/extApi.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/modularnn.dir/remoteApi/extApi.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/remoteApi/extApi.c > CMakeFiles/modularnn.dir/remoteApi/extApi.c.i

CMakeFiles/modularnn.dir/remoteApi/extApi.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/modularnn.dir/remoteApi/extApi.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/remoteApi/extApi.c -o CMakeFiles/modularnn.dir/remoteApi/extApi.c.s

CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.requires:

.PHONY : CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.requires

CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.provides: CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.requires
	$(MAKE) -f CMakeFiles/modularnn.dir/build.make CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.provides.build
.PHONY : CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.provides

CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.provides.build: CMakeFiles/modularnn.dir/remoteApi/extApi.c.o


CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o: CMakeFiles/modularnn.dir/flags.make
CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o: ../remoteApi/extApiPlatform.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o   -c /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/remoteApi/extApiPlatform.c

CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/remoteApi/extApiPlatform.c > CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.i

CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/remoteApi/extApiPlatform.c -o CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.s

CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.requires:

.PHONY : CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.requires

CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.provides: CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.requires
	$(MAKE) -f CMakeFiles/modularnn.dir/build.make CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.provides.build
.PHONY : CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.provides

CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.provides.build: CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o


# Object files for target modularnn
modularnn_OBJECTS = \
"CMakeFiles/modularnn.dir/main.cpp.o" \
"CMakeFiles/modularnn.dir/remoteApi/extApi.c.o" \
"CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o"

# External object files for target modularnn
modularnn_EXTERNAL_OBJECTS =

modularnn: CMakeFiles/modularnn.dir/main.cpp.o
modularnn: CMakeFiles/modularnn.dir/remoteApi/extApi.c.o
modularnn: CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o
modularnn: CMakeFiles/modularnn.dir/build.make
modularnn: CMakeFiles/modularnn.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX executable modularnn"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/modularnn.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/modularnn.dir/build: modularnn

.PHONY : CMakeFiles/modularnn.dir/build

CMakeFiles/modularnn.dir/requires: CMakeFiles/modularnn.dir/main.cpp.o.requires
CMakeFiles/modularnn.dir/requires: CMakeFiles/modularnn.dir/remoteApi/extApi.c.o.requires
CMakeFiles/modularnn.dir/requires: CMakeFiles/modularnn.dir/remoteApi/extApiPlatform.c.o.requires

.PHONY : CMakeFiles/modularnn.dir/requires

CMakeFiles/modularnn.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/modularnn.dir/cmake_clean.cmake
.PHONY : CMakeFiles/modularnn.dir/clean

CMakeFiles/modularnn.dir/depend:
	cd /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build /home/hudson/Desktop/UFG/TCC/Códigos/ModularNN/build/CMakeFiles/modularnn.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/modularnn.dir/depend
