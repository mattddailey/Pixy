sudo pip3 install -r backend/requirements.txt

git submodule update --init --recursive
git config matrix.ignore all

echo "$(tput setaf 4)Running rgbmatrix installation...$(tput setaf 9)"

cd matrix/bindings/python/rgbmatrix/ || exit

python3 -m pip install --no-cache-dir cython
python3 -m cython -2 --cplus *.pyx

cd ../../../ || exit

make build-python PYTHON="$(command -v python3)"
sudo make install-python PYTHON="$(command -v python3)"

cd ../ || exit

git reset --hard
git fetch origin --prune
git pull

echo "$(tput setaf 4)Running Make...$(tput setaf 9)"

make