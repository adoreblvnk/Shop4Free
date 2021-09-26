# Shop4Free_Master

an Applications Security Project.\
prod by Joseph, Aden, Hao Yu, Jayden.\
mastered by Joseph.

---

## Setup Instructions

### HTTPS

Shop4Free uses a self-signed certificate, in which the signature is generated using private key that's associated with same certificate. This trust relationship allows the client to validate server certificate. A self-signed certificate is used instead of a certificate signed by a Certification Authority, because for "localhost", nobody uniquely owns it, and it’s not rooted in a top level domain like ".com" or ".net".

Steps to Generate Self-Signed Certificate (Optional):

1. Install OpenSSL.
2. Generate the key with the following command: `openssl genrsa -des3 -out rootCA.key 2048`.
3. Generate certificate with following command: `openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1460 -out rootCA.pem`.
4. Copy `rootCA.pem` & `rootCA.key` into Shop4Free_Master if files not in Shop4Free_Master.
5. Run the application.

Steps to Run Shop4Free with HTTPS with Preinstalled Keys:

1. Enter "rnndm" (no quotes) for passphrase.
2. Run `cmd.exe` as Administrator & navigate to Shop4Free folder.
3. Run the following command to trust the certificate: `certutil -addstore -f "ROOT" rootCA.pem`.
4. (Additional Step if Certificate is Not Trusted (Firefox Mandatory)): Trust the certificate by importing `rootCA.pem` into Privacy > Certificates.

### reCaptcha

Google's reCaptcha site, [reCaptcha](https://www.google.com/recaptcha/) is used.

Steps to Generate reCaptcha (Optional):

1. Sign up @ [reCaptcha](https://www.google.com/recaptcha/).
2. Select `v2 Tickbox` as the reCaptcha type.
3. Type `127.0.0.1` as the domain.
4. Save.
5. Copy the private & public keys into `RECAPTCHA_PRIVATE_KEY` & `RECAPTCHA_PUBLIC_KEY` respectively.
6. Run the application.

### Stripe

Stripe is a 3rd-party payment processor & payment gateway. Stripe composes of an API & CLI.

Stripe Cards:

1. Success: 4000 0027 6000 3184
2. Decline: 4000 0000 0000 0002

Steps to Generate Endpoint Secret in Stripe:

1. From terminal (where `stripe.exe` is located), generate command `stripe listen --forward-to 127.0.0.1:5000/stripe_webhook` to get endpoint secret.
2. Login into Stripe if necessary.
3. Paste endpoint secret into Stripe webhook function in `app.py`.

## Footnotes

Contact josef @blvnk#9824 / @adore_blvnk for private keys. 👻
