# 檔案: conftest.py
import os
import sys

# (關鍵) 將 'src' 目錄添加到 Python 的模組搜索路徑中 (list 的最前面)
# 這讓我們在 tests/ 裡的測試檔可以寫: 'from data_fetcher import ...'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
