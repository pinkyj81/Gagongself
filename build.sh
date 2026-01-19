#!/usr/bin/env bash
# Render 빌드 스크립트

set -o errexit

# Python 패키지 설치 (python-tds는 순수 Python이라 시스템 패키지 불필요)
pip install --upgrade pip
pip install -r requirements.txt

echo "빌드 완료!"
