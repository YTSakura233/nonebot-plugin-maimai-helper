import socket
import ssl

from urllib3.util import Url


class HttpClient:
    @staticmethod
    def post(uri: Url, headers, body, timeout: float = 3):
        host = uri.hostname
        port = uri.port
        context = ssl._create_unverified_context()

        # 构建请求头
        headers["Content-Length"] = len(body)
        headers["Host"] = host
        request = f"POST {uri.path} HTTP/1.1\r\n"
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
        request += "\r\n"

        # 连接服务器
        if uri.scheme == "http":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host)
        sock.connect((host, port))
        sock.settimeout(timeout)

        # 发送请求
        sock.send(request.encode() + body)

        # 接收响应
        response = b''
        response_headers = {}
        response_code = 0

        data = sock.recv(4096)

        for line in data.split(b'\r\n\r\n')[0].split(b'\r\n'):
            if b'HTTP' in line:
                response_code = int(line.split(b' ')[1].decode())
            else:
                response_headers[line.split(b': ')[0].decode().strip()] = line.split(b': ')[1].decode().strip()

        content_length = int(response_headers.get('Content-Length', 0))

        response += data.split(b'\r\n\r\n')[1]
        current_length = len(response)

        while current_length < content_length:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                response += data
                current_length = len(response)
            except:
                break

        sock.close()

        return {
            "status_code": response_code,
            "headers": response_headers,
            "body": response
        }
