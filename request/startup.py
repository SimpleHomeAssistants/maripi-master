import argparse
import subprocess
from common.config import get_dest_mac
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
    mac_address = get_dest_mac(dest);

    # wol.py 실행: MAC 주소를 인자로 사용
    try:
        subprocess.run(['python', '../wol.py', mac_address], check=True)
        print(f"Wake-on-LAN sent to {mac_address}")
    except subprocess.CalledProcessError as e:
        print(f"Error while executing wol.py: {e}")

if __name__ == "__main__":
    main()
