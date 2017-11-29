# python 首次安装执行脚本

conda update conda
conda update --all

conda install numexpr numpy pandas lxml matplotlib beautifulsoup4 scrapy
conda install sqlalchemy sqlite
conda install scikit-learn
conda install bcolz

# install talib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure
make
sudo make install
pip install TA-Lib

pip install fake-useragent 
pip install pandas_datareader

