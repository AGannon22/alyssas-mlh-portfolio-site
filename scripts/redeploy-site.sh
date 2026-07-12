#!/bin/bash
set -e
cd ~
cd portfolio-website/alyssas-mlh-portfolio-site
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart myportfolio
