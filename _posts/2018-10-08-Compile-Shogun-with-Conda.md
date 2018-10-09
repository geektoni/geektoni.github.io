---
layout: post
title: Compile Shogun 6.1.3 with Miniconda.
date: 2018-10-08 9:00
excerpt: Compile Shogun 6.1.3 with Miniconda.
tags: [conda,miniconda,python,shogun,toolbox,machine learning]
---

# Compile Shogun 6.1.3 with Miniconda.

It just happened to me to have to compile the Python interface of Shogun 6.1.3
by using Miniconda as Python environment. I will report here the steps needed
to do it just in case somebody else needs it (or in case I'll need them
again in a not so far away future).

Everything was done on a Debian GNU/Linux 9 machine. My `conda`'s version
is the 4.5.11.

Since I wanted to use Python 3.5, I needed to create a new conda environment.
Then I needed to activate it in order to be able to use it correctly:
```bash
conda create -n python3.5 python=3.5
source activate python3.5
```
Remember that all the instructions below will work only when inside the new
conda environment. In fact, this will enable Shogun only for Python 3.5.

Secondly, we have to download and extract the packages (both the toolbox and gpl code):
```bash
wget https://github.com/shogun-toolbox/shogun/archive/shogun_6.1.3.tar.gz
wget https://github.com/shogun-toolbox/shogun-gpl/archive/v6.1.3.tar.gz
tar -xvf shogun_6.1.3.tar.gz -C shogun_6_1_3
tar -xvf v6.1.3.tar.gz -c shogun_6_1_3/src/gpl
```

Then, we have to build the toolbox (here `$MINICONDADIR` indicates the directory
where you installed miniconda). The build process will leave out the
test suite, the meta examples and it will compile Shogun in release mode.
It will also install Shogun in a custom directory in a way to avoid using
`sudo`.
```bash
cd shogun_6_1_3/
mkdir build/
cd build/
cmake -DCMAKE_INSTALL_PREFIX=/path/to/shogun/install/dir \
-DPYTHON_INCLUDE_DIR=$MINICONDADIR/envs/python3.5/include/python3.5m \
-DPYTHON_LIBRARY=$MINICONDADIR/envs/python3.5/lib/libpython3.5m.so \
-DPYTHON_EXECUTABLE:FILEPATH=$MINICONDADIR/envs/python3.5/bin/python \
-DPYTHON_PACKAGES_PATH=$MINICONDADIR/envs/python3.5/lib/python3.5 \
-DINTERFACE_PYTHON=ON \
-DBUILD_META_EXAMPLES=OFF \
-DENABLE_TESTING=OFF \
-DCMAKE_BUILD_TYPE=Release ../
make install
```

Remember to add the following lines to your `.bashrc` file in order
to set the library and interface locations:
```bash
export LD_LIBRARY_PATH="/path/to/shogun/install/dir/lib:$LD_LIBRARY_PATH"
export PYTHONPATH="/path/to/shogun/install/dir/lib/python3.5/site-packages/shogun.py:$PYTHONPATH"
```

Ff you reached this point without errors then you are done!
You should be able to access Shogun 6.1.3 from your conda's environment.
