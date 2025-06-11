## 1. Setup System

### <----- _MacOS_ ----->
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3 and MongoDB
brew install python@3.9
brew tap mongodb/brew
brew install mongodb-community@7.0

# Start MongoDB
brew services start mongodb/brew/mongodb-community
```

---

### <----- _Ubuntu_ ----->
```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip -y

# Install MongoDB
sudo apt install gnupg curl -y
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
  --dearmor

echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## 2. Setup virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Trên Ubuntu hoặc MacOS
```

---

## 3. Install library python
```bash
pip install gradio langchain langchain-community langchain-openai openai pymongo python-dotenv
```

---

## 4. Start project
```bash
python app.py
```
