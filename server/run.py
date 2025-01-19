from flask import Flask, request, jsonify
import requests
import configparser

# 설정 파일 경로 (동일 경로에서 읽어올 경우)
config = configparser.ConfigParser()
config.read('../settings.ini')

# settings.ini 파일에서 값 읽기
passwd = config['DEFAULT']['passwd']
port = config.getint('DEFAULT', 'port')  # port 값을 정수형으로 읽음
dest1 = config['DESTINATION']['dest1']
dest2 = config['DESTINATION']['dest2']

app = Flask(__name__)

def send_request(endpoint):
    """요청을 보내고 결과를 반환하는 함수."""
    try:
        response = requests.post(endpoint, headers={"passwd": passwd}, timeout=5)

        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "response_code": response.status_code,
                "response_text": response.text
            })
        else:
            return jsonify({
                "status": "error",
                "response_code": response.status_code,
                "response_text": response.text
            }), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "error": "Request timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

def get_destination():
    """요청된 dest 값에 따른 URL을 결정하는 함수."""
    dest = request.json.get("dest")  # POST 요청에서는 JSON 데이터로 받습니다
    if dest == "dest1":
        return dest1 + "/shutdown"
    elif dest == "dest2":
        return dest2 + "/shutdown"
    else:
        return None

@app.route('/shutdown', methods=['POST'])
def shutdown_request():
    """shutdown API."""
    url = get_destination()
    if url is None:
        return jsonify({"status": "error", "error": "Invalid destination"}), 400
    return send_request(url)

@app.route('/shutdown_cancel', methods=['POST'])
def shutdown_cancel_request():
    """shutdown_cancel API."""
    url = get_destination().replace("/shutdown", "/shutdown_cancel")  # 수정된 URL
    if url is None:
        return jsonify({"status": "error", "error": "Invalid destination"}), 400
    return send_request(url)

@app.route('/reboot', methods=['POST'])
def reboot_request():
    """reboot API."""
    url = get_destination().replace("/shutdown", "/reboot")  # 수정된 URL
    if url is None:
        return jsonify({"status": "error", "error": "Invalid destination"}), 400
    return send_request(url)

if __name__ == '__main__':
    # 변경된 포트를 사용하여 서버 실행
    app.run(debug=True, host='0.0.0.0', port=port)
