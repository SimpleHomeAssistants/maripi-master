#!/bin/bash

# 설정 파일 경로
SETTINGS_FILE="../settings.ini"

# 파일 경로가 올바른지 확인
if [ ! -f "$SETTINGS_FILE" ]; then
  echo "Error: 설정 파일을 찾을 수 없습니다."
  exit 1
fi

# 설정 파일에서 값을 읽어오는 함수
read_config() {
  local key=$1
  local section=$2
  local value=$(sed -n "/\[$section\]/,/\[.*\]/p" "$SETTINGS_FILE" | grep -E "^$key=" | cut -d '=' -f2- | tr -d '[:space:]')
  echo "$value"
}

# [DEFAULT] 섹션에서 값 읽기
port=$(read_config "port" "DEFAULT")
passwd=$(read_config "passwd" "DEFAULT")

# [DESTINATION] 섹션에서 값 읽기
dest1_url=$(read_config "dest1" "DESTINATION")
dest2_url=$(read_config "dest2" "DESTINATION")

# 확인
echo "port: $port"
echo "passwd: $passwd"
echo "dest1_url: $dest1_url"
echo "dest2_url: $dest2_url"

# dest 확인 함수 (예시: dest1 또는 dest2로 처리)
get_destination() {
  if [ "$dest" = "dest1" ]; then
    dest_url=$dest1_url
  elif [ "$dest" = "dest2" ]; then
    dest_url=$dest2_url
  else
    echo "Invalid destination."
    exit 1
  fi
}

# 인자 처리
while getopts "d:p:a:" opt; do
  case $opt in
    d) dest=$OPTARG ;;
    p) passwd=$OPTARG ;;
    a) action=$OPTARG ;;
    \?) echo "Usage: $0 -d dest -p passwd -a action" ;;
  esac
done

# 필수 인자 확인
if [ -z "$dest" ] || [ -z "$passwd" ] || [ -z "$action" ]; then
  echo "Error: Missing required arguments."
  exit 1
fi

# 서버 요청 전송
get_destination
echo "Requesting action: $action with password: $passwd to destination: $dest_url"
