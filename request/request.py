import configparser
import requests
import argparse

# 설정 파일 경로
SETTINGS_FILE = '../settings.ini'

# 설정 읽기 함수
def read_config():
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    
    # DEFAULT 섹션의 값 읽기
    port = config.get('DEFAULT', 'port', fallback=None)
    passwd = config.get('DEFAULT', 'passwd', fallback=None)
    
    # DESTINATION 섹션의 값 읽기
    dest1_url = config.get('DESTINATION', 'dest1', fallback=None)
    dest2_url = config.get('DESTINATION', 'dest2', fallback=None)
    
    return port, passwd, dest1_url, dest2_url

# URL에 HTTP 요청 보내는 함수
def send_request(url, passwd, action):
    headers = {
        "Content-Type": "application/json",
        "passwd": passwd
    }
    
    try:
        response = requests.post(url, headers=headers, json={"action": action})
        response.raise_for_status()  # 오류가 있을 경우 예외를 발생시킴
        return response.status_code, response.text
    except requests.RequestException as e:
        return None, str(e)

# 인자 처리 함수
def parse_arguments():
    parser = argparse.ArgumentParser(description="Shutdown, reboot, or shutdown cancel tasks")
    parser.add_argument('-d', '--dest', required=True, help="destination (dest1 or dest2)")
    parser.add_argument('-p', '--passwd', required=True, help="password for authentication")
    parser.add_argument('-a', '--action', required=True, help="action to perform (shutdown, reboot, or shutdown_cancel)")
    
    args = parser.parse_args()
    return args.dest, args.passwd, args.action

# 메인 처리 함수
def main():
    # 설정 값 읽기
    port, passwd, dest1_url, dest2_url = read_config()
    
    # 명령줄 인자 파싱
    dest, action_passwd, action = parse_arguments()
    
    # 비밀번호 일치 확인
    if passwd != action_passwd:
        print("Invalid password")
        return
    
    # 대상 URL 선택
    if dest == "dest1":
        url = f"{dest1_url}/{action}"
    elif dest == "dest2":
        url = f"{dest2_url}/{action}"
    else:
        print("Invalid destination.")
        return
    
    # 요청 보내기
    status_code, response_text = send_request(url, passwd, action)
    
    if status_code:
        print(f"Request succeeded: {status_code}\n{response_text}")
    else:
        print(f"Request failed: {response_text}")

if __name__ == "__main__":
    main()
