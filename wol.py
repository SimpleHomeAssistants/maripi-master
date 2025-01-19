import socket
import struct
import sys

def send_wol_packet(mac_address):
    # MAC 주소를 ':' 없이 제거하고, 대문자로 변환
    mac_address = mac_address.replace(":", "").upper()

    # Magic Packet을 위해, 매직 패킷의 형식으로 MAC 주소 반복
    if len(mac_address) != 12:
        print("MAC 주소는 12자의 유효한 형식이어야 합니다.")
        sys.exit(1)

    # 매직 패킷을 생성합니다.
    # 6바이트 0xFF + 16번의 MAC 주소 반복
    packet = b'\xff' * 6 + (bytes.fromhex(mac_address) * 16)

    # UDP 패킷을 보내기 위한 소켓 설정
    broadcast_ip = '255.255.255.255'  # 브로드캐스트 주소
    port = 9  # WOL 기본 포트 (일반적으로 9 포트 사용)

    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # WOL 패킷을 브로드캐스트 주소로 전송
    sock.sendto(packet, (broadcast_ip, port))
    sock.close()

    print(f"MAC 주소 {mac_address}으로 WOL 패킷을 전송하였습니다.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python wol_script.py [MAC 주소]")
        sys.exit(1)

    # 프로그램 인자로 MAC 주소 받기
    mac_address = sys.argv[1]

    # WOL 패킷을 보내기
    send_wol_packet(mac_address)

if __name__ == '__main__':
    main()
