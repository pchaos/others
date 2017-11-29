conda install -y matplotlib

#设置matplotlib的backend（没有图形化界面的情况下）
echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc

pip install -U pip setuptools cython

sudo yum install gcc-c++
pip install bcolz

# install TA-lib


pip install rqalpha

rqalpha version

rqalpha update_bundle
cd .rqalpha
rqalpha examples -d ./
