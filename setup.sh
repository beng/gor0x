VPATH=`dirname $0`/virtual
mkdir -p $VPATH
virtualenv --distribute --python=`which python2.7` $VPATH
source $VPATH/bin/activate
pip install -Ur requirements.txt