import argparse
from common.config import get_dest_url
from common.requester import send_request

def parse_arguments():
    parser = argparse.ArgumentParser(description="Shutdown task")
    parser.add_argument('-d', '--dest', required=True, choices=['1', '2'], help="destination (1 or 2)")
    parser.add_argument('-p', '--passwd', required=True, help="password for authentication")
    args = parser.parse_args()
    return args.dest, args.passwd

def main():
    # 명령줄 인자 파싱
    dest, pwd = parse_arguments()

    url = f"{get_dest_url(dest)}/shutdown"  # shutdown 작업을 위한 URL

    # 요청 보내기
    status_code, response_text = send_request(url, pwd, "shutdown")

    if status_code:
        print(f"Request succeeded: {status_code}\n{response_text}")
    else:
        print(f"Request failed: {response_text}")

if __name__ == "__main__":
    main()
