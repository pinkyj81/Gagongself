#!/usr/bin/env bash
# Render 빌드 스크립트 - SQL Server 연결을 위한 시스템 패키지 설치

set -o errexit

# FreeTDS 및 의존성 설치 (pymssql 빌드에 필요)
apt-get update
apt-get install -y freetds-dev freetds-bin unixodbc-dev

# Python 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt

echo "빌드 완료!"
