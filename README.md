# clarion
The clarion call tells you if someone is logging into an AitM proxy that is proxying your M365 login page

![image](https://github.com/HuskyHacks/clarion/assets/57866415/58627a15-8beb-43d5-a0f1-4172f9da8653)

## Warning
This is **extremely** experimental.

## Concept & Disclaimer
[This article](https://zolder.io/using-honeytokens-to-detect-aitm-phishing-attacks-on-your-microsoft-365-tenant/) from Zolder describes the concept quite well. This is not my original idea and the credit goes to them for it.

M365 allows you to inject custom CSS into the M365 login screen through the Company Branding settings. Ostensibly, this allows you to put a cool background image on your login page.

We can take advantage of this to detect when a user is logging into an Adversary in the Middle (AitM) proxy like Evilginx that is mimicking your legitimate login page.

Clarion creates and hosts a small tracking pixel that we can embed into our custom company branding CSS file. When a normal login occurs, this CSS is retrieved dynamically and rendered on the M365 login page. When that happens during a routine login, the referer header for the CSS retrieval is "login.microsoft.com"

However, if a threat actor has created an AitM domain and login page, the referer header will be their own domain. If our tracking pixel is ever requested with a referer header that is NOT login.microsoft.com, it is highly likely that someone is logging into a transparent proxy.

Zolder uses their own site, [didsomeoneclone.me](https://didsomeoneclone.me/) as their proof of concept. It works like a charm! But I wanted to create the whole system to learn more about it and demonstrate the entire process, start to finish. Thank you to Zolder for their work on this! Really cool concept and great work.
 
## Setup
For testing, you can use a self-signed certificate. 

```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

**Important:** Make sure you accept the warning about the invalid certificate in the browser that you want to test if using a self-signed cert. If you don't, the client browser will throw an error when trying to load the remote CSS and will not trigger the clarion call.

![image](https://github.com/HuskyHacks/clarion/assets/57866415/2d66f9aa-09c5-4d15-974e-3f71e2ddcf50)

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

[some CSS element] {
    background-image: url('https://[Public IP]/[pixel name].png');
    background-size: 0 0;
}

 * Debugger is active!
 * Debugger PIN: 422-205-484
```

Take this custom CSS pixel element and add it to your M365 Company Branding as a custom CSS file:

![image](https://github.com/HuskyHacks/clarion/assets/57866415/c94192ed-6b73-43ea-a158-ca34b69f91e2)

![image](https://github.com/HuskyHacks/clarion/assets/57866415/bc24d94b-14d4-4dde-a668-09bf8482d811)

![image](https://github.com/HuskyHacks/clarion/assets/57866415/f3401d09-1bfc-4154-9971-59b07523d44e)

![image](https://github.com/HuskyHacks/clarion/assets/57866415/f9234950-9353-41d1-8b44-9b23abe69095)

The [M365 Company Branding CSS Schema](https://learn.microsoft.com/en-us/entra/fundamentals/reference-company-branding-css-template) has the list of CSS elements that the M365 login page can use. `.ext-footer` seems to be a good option to trigger the clarion call.

eg. 
```
.ext-footer {
    background-image: url(https://[Public IP]/[pixel name].png);
    background-size: 0 0;
}
```

## Future Work
I'm willing to bet that this works with login pages for any service that allows you to specify custom CSS. I don't know which ones do, so if you have any ideas, open a PR or issue and let me know!

## Ref & Acknowledgements
Thank you again to Zolder for the original article on this technique!

- https://zolder.io/using-honeytokens-to-detect-aitm-phishing-attacks-on-your-microsoft-365-tenant/
