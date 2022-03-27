#!/usr/bin/env bash

# build hikyuu
# . ./hikyuuEnv.sh
./10_SetUpBasicEnvironment.sh
./00_hikyuu.sh
if [[ ! -d "*/stage" ]]
then
./15_buildboost.sh
fi
./30_buildhikyuu.sh

