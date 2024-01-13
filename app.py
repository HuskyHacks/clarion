from flask import Flask, request, send_file
import os
import uuid
from PIL import Image
from io import BytesIO
import requests
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

pixel_filename = f"{uuid.uuid4()}.png"

app = Flask(__name__)

# Function to create a single pixel image
def create_pixel():
    image = Image.new('RGB', (1, 1), color = (255, 255, 255))
    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    return byte_io

# Function to get public IP address
def get_public_ip():
    try:
        response = requests.get('http://ipv4.icanhazip.com', timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error obtaining public IP: {e}")
        return None


# Route to serve the pixel image
@app.route(f'/{pixel_filename}')
def pixel():
    # Identify the requesting host
    requester = request.remote_addr

    # Warn if the requester is not from microsoft.com
    # Note: This is a simplistic check and may not be reliable for all cases
    if 'microsoft.com' not in requester:
        app.logger.warning(f"Non-Microsoft host detected: {requester}")

    # Serve the pixel image
    return send_file(create_pixel(), mimetype='image/png')

def main():
    # Check if certificate files exist
    if not (os.path.exists('cert.pem') and os.path.exists('key.pem')):
        print("[-] SSL certificates not found. Please generate them using OpenSSL.\n  \\\\--> openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365")
    else:
        public_ip = get_public_ip()
        if public_ip:
            print(f"{Fore.CYAN}[*] Your public IP address is:{Style.RESET_ALL} {Fore.GREEN}{public_ip}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Embed this pixel in your CSS file with the following code:{Style.RESET_ALL}\n")
            print(f"{Fore.MAGENTA}body {{")
            print(f"{Fore.MAGENTA}    background-image: url('https://{public_ip}/{pixel_filename}');")
            print(f"{Fore.MAGENTA}    background-size: 0 0;")
            print(Fore.MAGENTA + "}" + Style.RESET_ALL)
            
            print()

            app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=443, debug=True)


if __name__ == "__main__":
    main()
