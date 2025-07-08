JSONRPC Client
==============

jsonrpc client is the [JSONRPC](https://www.jsonrpc.org/) client for HMI/PLC master-slave architecture JSONRPC server.
This code is used python3.12 and [pyside6](https://doc.qt.io/qtforpython-6/index.html) as GUI.


https://github.com/user-attachments/assets/b9056e5e-a25b-4ab4-9df0-db2a35682987

### 安裝
* git client - git clone code 到本地工作目錄
* python 3 - 現是以3.12開發
* 以python venv module建置工作環境並啟動, 先切換到source 目錄下
   * Windows
  ```sh
  python3 -m venv venv
  venv\Script\Activate
  ```
     * Linux
  ```sh
  python3 -m venv venv
  source venv/bin/active
  ```
* 以pip 安裝程式，這一個venv環境只要做一次
  ```sh
  pip install -e .
  python gen_dialog.py
  ```

### 測試
* 啟動osprey後，設定IPC的TCP server 設定其IP和port。如 IP 127.0.0.1/port 51820
```sh
python client.py 127.0.0.1 51820
```

### 主畫面編輯
畫面設計檔其副檔名為ui
```sh
pyside6-designer ui/main_window.ui
```

### 打包成執行檔 - WINDOWS和Linux皆可支援, 以下以WINDOWS 終端機演示

#### 環境架設及安裝 - venv 和  pyinstaller

在source code 工作目錄下執行以下指命
```sh
python -m venv venv
venv\Scripts\activate
pip install -e .
pip install pyinstaller
```

#### 更新UI
在source code 工作目錄下執行以下指命且已進入venv模式
```sh
python gen_dialog.py
```

#### 打包指命

在source code 工作目錄下執行以下指命且已進入venv模式
```sh
pyinstaller -F client.py
```
執行完後在dist有打包後執行檔



