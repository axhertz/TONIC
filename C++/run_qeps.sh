
#!/bin/bash

cd analysePlainAndFilter
rm -rf CMakeFiles
rm CMakeCache.txt
rm cmake_install.cmake
rm Makefile
cd ..

cd analyseSelAwareQEPS
rm -rf CMakeFiles
rm CMakeCache.txt
rm cmake_install.cmake
rm Makefile
cd ..


cmake build  -B./analysePlainAndFilter -S./analysePlainAndFilter/ -DCMAKE_BUILD_TYPE=Release
cmake --build ./analysePlainAndFilter/

cmake build  -B./analyseSelAwareQEPS -S./analyseSelAwareQEPS/ -DCMAKE_BUILD_TYPE=Release
cmake --build ./analyseSelAwareQEPS/


./analysePlainAndFilter/analyseQEPSplain

./analyseSelAwareQEPS/analyseQEPS

