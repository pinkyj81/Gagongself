#!/usr/bin/env bash
# Render 빌드 스크립트

set -o errexit

# Python 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt

# SQL Server 2008 호환을 위한 시스템 패키지 설치 (선택사항)
# apt-get update
# apt-get install -y freetds-dev unixodbc-dev

echo "빌드 완료!"
