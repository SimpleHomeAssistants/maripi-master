import requests

def send_request(url, passwd, action):
    headers = {
        "Content-Type": "application/json",
        "passwd": passwd
    }

    try:
        response = requests.post(url, headers=headers, json={"action": action})
        response.raise_for_status()  # 오류 발생 시 예외 처리
        return response.status_code, response.text
    except requests.RequestException as e:
        return None, str(e)
