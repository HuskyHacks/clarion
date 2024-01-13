# clarion
The clarion call tells you if someone is logging into an AitM proxy that is proxying your M365 login page

## Setup
For testing, you can use a self-signed certificate. Make sure you accept the warning about the invalid certificate in the browser that you want to test.
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

For production use, you would want a legitimate signed certificate.

Clone the repo to your publically accessible host and install the requirements:

```
$ pip3 install -r requirements.txt
```

Then run the app (you need root level permissions to bind to port 443):

```
$ [sudo] python3 app.py

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on https://127.0.0.1:443
 * Running on https://[Public IP]:443
Press CTRL+C to quit
 * Restarting with stat

[*] Your public IP address is: [Public IP]
[*] Embed this pixel in your CSS file with the following code:

body {
    background-image: url('https://[Public IP]/[pixel name].png');
    background-size: 0 0;
}

 * Debugger is active!
 * Debugger PIN: 422-205-484
```