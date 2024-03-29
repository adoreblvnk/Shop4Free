<div align="center">
    <img src="./static/image/S4FLogo.png" width=100> <!-- Logo -->
    <h1>Shop4Free</h1> <!-- Title -->
    <p>
      An applications security project focused on tackling common vulnerabilities present in e-commerce sites.
    </p> <!-- Description -->
    <p>
      Built With: Flask • Wamp64 • Twilio • Stripe
    </p> <!-- Built With -->
</div>

---

<details>
<summary>Table of Contents</summary>

- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Execution](#execution)
</details>

## Demo

**Failed Login Attempts**

[![failed login attempts](https://i.imgur.com/wpfDPTw.png)](https://streamable.com/xrhlvq)

Custom error page after 3 failed logins.

**2FA**

[![2FA](https://i.imgur.com/eQ7wVGo.png)](https://streamable.com/antb1q)

Built with Twilio.

**Payment**

[![payment](https://i.imgur.com/M4VpAPl.png)](https://streamable.com/tzq63z)

Built with Stripe.

**Admin Logging**

[![admin](https://i.imgur.com/nxg8hgN.png)](https://streamable.com/3kc075)

Detecting attempted SQL injections, and highlighting them in red.

## Getting Started

### Prerequisites

- OpenSSL

### Installation

**SSL**

- The PEM password for running Shop4Free is `rnndmm`.

**reCaptcha**

1. Sign up @ [reCaptcha](https://www.google.com/recaptcha/).
2. Select `v2 Tickbox` as the reCaptcha type.
3. Type `127.0.0.1` as the domain.
4. Save.
5. Copy the private & public keys into `RECAPTCHA_PRIVATE_KEY` & `RECAPTCHA_PUBLIC_KEY` respectively.
6. Run the application.

**Stripe**

Stripe is a 3rd-party payment processor & payment gateway. Stripe composes of an API & CLI.

Stripe Cards:

1. Success: 4000 0027 6000 3184
2. Decline: 4000 0000 0000 0002

Steps to Generate Endpoint Secret in Stripe:

1. From terminal (where `stripe.exe` is located), generate command `stripe listen --forward-to 127.0.0.1:5000/stripe_webhook` to get endpoint secret.
2. Login into Stripe if necessary.
3. Paste endpoint secret into Stripe webhook function in `app.py`.

### Execution

    py app.py

## License <!-- omit in toc -->

This project is licensed under the terms of the MIT license.

## Credits <!-- omit in toc -->

- Joseph
- Aden
- Hao Yu
- Jayden
- blvnk
