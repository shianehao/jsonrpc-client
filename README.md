# JSONRPC Client

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
