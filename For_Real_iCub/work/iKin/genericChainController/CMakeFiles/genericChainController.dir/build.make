# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.0

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
CMAKE_SOURCE_DIR = /home/icub/Desktop/Akira/iCub/work/iKin

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/icub/Desktop/Akira/iCub/work/iKin

# Include any dependencies generated for this target.
include genericChainController/CMakeFiles/genericChainController.dir/depend.make

# Include the progress variables for this target.
include genericChainController/CMakeFiles/genericChainController.dir/progress.make

# Include the compile flags for this target's objects.
include genericChainController/CMakeFiles/genericChainController.dir/flags.make

genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o: genericChainController/CMakeFiles/genericChainController.dir/flags.make
genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o: genericChainController/main.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/icub/Desktop/Akira/iCub/work/iKin/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o"
	cd /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/genericChainController.dir/main.cpp.o -c /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController/main.cpp

genericChainController/CMakeFiles/genericChainController.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/genericChainController.dir/main.cpp.i"
	cd /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController/main.cpp > CMakeFiles/genericChainController.dir/main.cpp.i

genericChainController/CMakeFiles/genericChainController.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/genericChainController.dir/main.cpp.s"
	cd /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController/main.cpp -o CMakeFiles/genericChainController.dir/main.cpp.s

genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.requires:
.PHONY : genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.requires

genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.provides: genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.requires
	$(MAKE) -f genericChainController/CMakeFiles/genericChainController.dir/build.make genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.provides.build
.PHONY : genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.provides

genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.provides.build: genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o

# Object files for target genericChainController
genericChainController_OBJECTS = \
"CMakeFiles/genericChainController.dir/main.cpp.o"

# External object files for target genericChainController
genericChainController_EXTERNAL_OBJECTS =

genericChainController/genericChainController: genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o
genericChainController/genericChainController: genericChainController/CMakeFiles/genericChainController.dir/build.make
genericChainController/genericChainController: /home/icub/icub-main/build/lib/libiKin.a
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_OS.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_sig.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_math.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_dev.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_init.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_name.so.2.3.64.13
genericChainController/genericChainController: /home/icub/icub-main/build/lib/libctrlLib.a
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_math.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_dev.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_sig.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_init.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_name.so.2.3.64.13
genericChainController/genericChainController: /home/icub/yarp/build/lib/libYARP_OS.so.2.3.64.13
genericChainController/genericChainController: /usr/lib/libgsl.so
genericChainController/genericChainController: /usr/lib/libgslcblas.so
genericChainController/genericChainController: /home/icub/Ipopt-3.12.4/lib/libipopt.so
genericChainController/genericChainController: /home/icub/Ipopt-3.12.4/lib/libcoinmumps.so
genericChainController/genericChainController: /home/icub/Ipopt-3.12.4/lib/libcoinmumps.so
genericChainController/genericChainController: /home/icub/Ipopt-3.12.4/lib/libcoinmetis.so
genericChainController/genericChainController: genericChainController/CMakeFiles/genericChainController.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable genericChainController"
	cd /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/genericChainController.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
genericChainController/CMakeFiles/genericChainController.dir/build: genericChainController/genericChainController
.PHONY : genericChainController/CMakeFiles/genericChainController.dir/build

genericChainController/CMakeFiles/genericChainController.dir/requires: genericChainController/CMakeFiles/genericChainController.dir/main.cpp.o.requires
.PHONY : genericChainController/CMakeFiles/genericChainController.dir/requires

genericChainController/CMakeFiles/genericChainController.dir/clean:
	cd /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController && $(CMAKE_COMMAND) -P CMakeFiles/genericChainController.dir/cmake_clean.cmake
.PHONY : genericChainController/CMakeFiles/genericChainController.dir/clean

genericChainController/CMakeFiles/genericChainController.dir/depend:
	cd /home/icub/Desktop/Akira/iCub/work/iKin && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/icub/Desktop/Akira/iCub/work/iKin /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController /home/icub/Desktop/Akira/iCub/work/iKin /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController /home/icub/Desktop/Akira/iCub/work/iKin/genericChainController/CMakeFiles/genericChainController.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : genericChainController/CMakeFiles/genericChainController.dir/depend

