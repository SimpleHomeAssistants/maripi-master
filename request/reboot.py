import argparse
from common.config import get_dest_url, get_pwd
from common.requester import send_request

def parse_arguments():
    parser = argparse.ArgumentParser(description="Shutdown task")
    parser.add_argument('-d', '--dest', required=True, choices=['1', '2'], help="destination (1 or 2)")
    parser.add_argument('-p1', '--passwd1', required=True, help="password for authentication")
    parser.add_argument('-p2', '--passwd2', required=True, help="password for authentication")
    args = parser.parse_args()
    return args.dest, args.passwd1, args.passwd2

def main():
    # 명령줄 인자 파싱
    dest, pwd1, pwd2 = parse_arguments()

    # 비밀번호 일치 확인
    if pwd1 != get_pwd():
        print("Invalid password")
        return

    url = f"{get_dest_url(dest)}/reboot"  # shutdown 작업을 위한 URL

    # 요청 보내기
    status_code, response_text = send_request(url, pwd2, "reboot")

    if status_code:
        print(f"Request succeeded: {status_code}\n{response_text}")
    else:
        print(f"Request failed: {response_text}")

if __name__ == "__main__":
    main()
