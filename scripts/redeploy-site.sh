#!/bin/bash
tmux kill-server
cd ~
cd portfolio-website/alyssas-mlh-portfolio-site
git fetch && git reset origin/main --hard
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
deactivate
tmux new-session -d -s "portfolio-server" \ "cd ~/portfolio-website/alyssas-mlh-portfolio-site && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0 --port=5000"