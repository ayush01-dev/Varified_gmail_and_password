
# Gmail & Password Verification System


## Project Structure
```
├── otp.py               # Handles OTP generation and verification
├── server.py            # Main server logic (Flask or similar)
├── users.json           # Stores registered user data
├── templates/           # HTML templates for registration and verification
│   ├── register.html
│   └── verify.html
└── __pycache__/         # Python cache files
```

## How It Works
1. **Register:** Users enter their Gmail and password on the registration page.
2. **OTP Sent:** An OTP is sent to the provided Gmail address.
3. **Verify:** Users enter the OTP to verify their email and complete registration.

## Setup & Usage
1. **Clone the repository:**
   ```powershell
   git clone <repo-url>
   cd Varified_gmail_and_password
   ```
2. **Install dependencies:**
   ```powershell
   pip install flask
   ```
3. **Run the server:**
   ```powershell
   python server.py
   ```
4. **Access the app:**
   Open your browser and go to `http://localhost:5000`


## Technologies Used
- Python
- Flask (or similar web framework)
- HTML/CSS

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is open source and available under the [MIT License](LICENSE).
