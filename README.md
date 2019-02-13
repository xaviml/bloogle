# bloogle: A Blog Search Engine

## Set up
To run this, you need python >= 3.6.x and install the requirements:
```
pip install -r requirements.txt
```

### Linux
As an additional step, you need to install chromedriver, for linux follow these commands:
```
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

### Windows
As an additional step, you need to install chromedriver, for windows follow these steps:
* Download: https://chromedriver.storage.googleapis.com/2.41/chromedriver_win32.zip
* Place *chromedriver.exe* in "C:\\Windows\\chromedriver.exe"