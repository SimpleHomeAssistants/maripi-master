#!/bin/bash

# 설정 파일을 읽어오도록 수정
. ./settings.ini  # settings.ini 경로가 한 단계 위로 설정됨

# 기본값 설정
dest_url=""
passwd=""

# 함수: dest URL을 선택하는 부분
get_destination() {
  # dest 값에 따라 선택하는 방법
  if [ "$dest" = "dest1" ]; then
    dest_url=$dest1_url
  elif [ "$dest" = "dest2" ]; then
    dest_url=$dest2_url
  else
    echo "Invalid destination."
    exit 1
  fi
}

# 서버로 요청 보내기 (curl 사용)
send_request() {
  # API 엔드포인트 URL에 추가할 path
  url="${dest_url}/${action}"

  # POST 요청 보내기
  response=$(curl -s -o response.txt -w "%{http_code}" -X POST "$url" -H "Content-Type: application/json" -d "{\"passwd\": \"$passwd\"}")

  if [ "$response" = "200" ]; then
    echo "Request successful"
    cat response.txt
  else
    echo "Error: $response"
    cat response.txt
    exit 1
  fi
}

# 인자 처리
while getopts "d:p:a:" opt; do
  case $opt in
    d)
      dest=$OPTARG
      ;;
    p)
      passwd=$OPTARG
      ;;
    a)
      action=$OPTARG
      ;;
    \?)
      echo "Usage: $0 -d dest -p passwd -a action"
      exit 1
      ;;
  esac
done

# 필수 인자 확인
if [ -z "$dest" ] || [ -z "$passwd" ] || [ -z "$action" ]; then
  echo "Error: Missing required arguments."
  echo "Usage: $0 -d dest -p passwd -a action"
  exit 1
fi

# destination URL 결정
get_destination

# 서버 요청
send_request
