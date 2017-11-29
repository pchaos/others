conda install -y matplotlib

#设置matplotlib的backend（没有图形化界面的情况下）
echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc

pip install -U pip setuptools cython

pip install bcolz

pip install rqalpha

rqalpha version

rqalpha update_bundle
rqalpha examples -d ./
