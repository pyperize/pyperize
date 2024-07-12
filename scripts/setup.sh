git update-index --assume-unchanged ./packages/__init__.py
python -m venv venv
source ./venv/bin/activate
sh ./scripts/install_requirements.sh
