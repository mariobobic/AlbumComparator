# 📷 Google Photos vs Local/SSH Album Comparator
This tool helps you compare media filenames in albums stored on:
- Google Photos
- Local directories
- Remote servers over SSH

It supports all combinations (Google ↔ SSH, Local ↔ SSH, Google ↔ Local), with filename output and diffing to help identify missing items.

---

## 🚀 Features
- Google OAuth 2.0 authentication
- SSH access with password-based login
- Local directory scanning
- Auto-export filenames to text files
- Compare two sources and show missing/surplus files
- Skips directories; only lists actual media files
- Strips date prefixes (e.g. `YYYY-MM-DD Device Name`)
- Sorted output filenames saved under `./exported`

---

## 📦 Project structure
```
AlbumComparator/
├── config/
│   ├── local_config.json        # Local root folder
│   └── ssh_config.json          # SSH credentials and path
├── creds/
│   ├── credentials.json         # Google API OAuth client
│   └── token.pickle             # OAuth token cache
├── exported/                    # Output filenames are saved here
├── *.py                         # Project source code
├── .gitignore
└── README.md
```

---

## 🛠 Setup
### 1. Google API Setup
- Create a project at https://console.cloud.google.com/
- Enable **Google Photos Library API**
- Download `credentials.json` and place it in `./creds/`

### 2. Install required Python libraries
Make sure you have Python 3.9+ installed, then install the required dependencies using pip:
```
pip install -r requirements.txt
```

You can also use a virtual environment for isolation:
```
python -m venv .venv source .venv/bin/activate # On Linux/macOS
.venv\Scripts\activate # On Windows
```

### 3. Config files
File: config/ssh_config.json
```
{
"host": "your.server.com",
"username": "your_user",
"password": "your_password",
"port": 22,
"remote_root": "~/Photos/PhoneAlbums"
}
```

File: config/local_config.json
```
{
"root_directory": "/Users/yourname/Pictures/PhoneAlbums"
}
```

---

## ▶️ Usage
Basic command:
```
python main.py --source1 google --source2 ssh
```

### Options
```
--source1        First source: google, ssh, or local  
--source2        Second source: google, ssh, or local  
--exclude        Names of folders to exclude from comparison
```

### Example
Let's assume that the contents of your root directory `/Users/yourname/Pictures/PhoneAlbums/` is as follows:
```
/Users/yourname/Pictures/PhoneAlbums/
├── .thumbnails
├── @SomeSystemFolder
├── 2011-03-15 Nokia N9
├── 2013-08-02 Motorola RAZR XT910
├── 2015-06-21 LG Optimus G Pro
├── 2016-11-05 Huawei Ascend Mate 7
├── 2017-10-30 Google Pixel 2 XL
├── 2018-07-12 Sony Xperia XZ2
├── 2019-04-03 HTC U12 Plus
├── 2020-09-17 Xiaomi Mi 10T Pro
├── 2021-12-01 Asus ROG Phone 5
├── 2023-05-22 Fairphone 4
```

The command to use is the following:
```
python main.py --source1 google --source2 ssh --exclude .thumbnails @SomeSystemFolder
```

---

## 📤 Output
Each album creates two files in ./exported/:
- Samsung_Galaxy_S8_list_google.txt
- Samsung_Galaxy_S8_list_ssh.txt

Differences are printed in the terminal.

---

## 📎 Notes
- Album folder names must end with device name (e.g., `2018-04-20 Samsung Galaxy S8`)
- Only filenames are compared (not file sizes or hashes)
- Designed for consistency-checking backups
