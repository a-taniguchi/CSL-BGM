# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

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

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/akira/Dropbox/iCub/work/motorControlAdvanced2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/akira/Dropbox/iCub/work/motorControlAdvanced2

# Include any dependencies generated for this target.
include CMakeFiles/tutorial_gaze_interface.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/tutorial_gaze_interface.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/tutorial_gaze_interface.dir/flags.make

CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o: CMakeFiles/tutorial_gaze_interface.dir/flags.make
CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o: tutorial_gaze_interface.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/akira/Dropbox/iCub/work/motorControlAdvanced2/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o -c /home/akira/Dropbox/iCub/work/motorControlAdvanced2/tutorial_gaze_interface.cpp

CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/akira/Dropbox/iCub/work/motorControlAdvanced2/tutorial_gaze_interface.cpp > CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.i

CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/akira/Dropbox/iCub/work/motorControlAdvanced2/tutorial_gaze_interface.cpp -o CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.s

CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.requires:
.PHONY : CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.requires

CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.provides: CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.requires
	$(MAKE) -f CMakeFiles/tutorial_gaze_interface.dir/build.make CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.provides.build
.PHONY : CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.provides

CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.provides.build: CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o

# Object files for target tutorial_gaze_interface
tutorial_gaze_interface_OBJECTS = \
"CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o"

# External object files for target tutorial_gaze_interface
tutorial_gaze_interface_EXTERNAL_OBJECTS =

tutorial_gaze_interface: CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o
tutorial_gaze_interface: CMakeFiles/tutorial_gaze_interface.dir/build.make
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_OS.so.2.3.66
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_sig.so.2.3.66
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_math.so.2.3.66
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_dev.so.2.3.66
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_init.so.2.3.66
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_name.so.2.3.66
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_sig.so.2.3.66
tutorial_gaze_interface: /usr/lib/x86_64-linux-gnu/libYARP_OS.so.2.3.66
tutorial_gaze_interface: CMakeFiles/tutorial_gaze_interface.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable tutorial_gaze_interface"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tutorial_gaze_interface.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/tutorial_gaze_interface.dir/build: tutorial_gaze_interface
.PHONY : CMakeFiles/tutorial_gaze_interface.dir/build

CMakeFiles/tutorial_gaze_interface.dir/requires: CMakeFiles/tutorial_gaze_interface.dir/tutorial_gaze_interface.cpp.o.requires
.PHONY : CMakeFiles/tutorial_gaze_interface.dir/requires

CMakeFiles/tutorial_gaze_interface.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/tutorial_gaze_interface.dir/cmake_clean.cmake
.PHONY : CMakeFiles/tutorial_gaze_interface.dir/clean

CMakeFiles/tutorial_gaze_interface.dir/depend:
	cd /home/akira/Dropbox/iCub/work/motorControlAdvanced2 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/akira/Dropbox/iCub/work/motorControlAdvanced2 /home/akira/Dropbox/iCub/work/motorControlAdvanced2 /home/akira/Dropbox/iCub/work/motorControlAdvanced2 /home/akira/Dropbox/iCub/work/motorControlAdvanced2 /home/akira/Dropbox/iCub/work/motorControlAdvanced2/CMakeFiles/tutorial_gaze_interface.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/tutorial_gaze_interface.dir/depend

