#!/usr/bin/env bash

boostdir="boost_1_${boostver}_0"
if [[ -d ${boostdir} ]]
then
  cd ${boostdir}
  sudo ./b2 uninstall
  cd .. && rm -rf "${boostdir}"
fi
rm -rf hikyuu

unset BOOST_LIB
