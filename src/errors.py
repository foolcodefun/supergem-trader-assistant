# 檔案: src/errors.py
"""
存放專案自訂的 Exception 類別。
"""
class DataFetchError(ValueError):
    """當數據抓取失敗時拋出的自訂錯誤。"""
    # 我們 'pass' 是因為我們只是想定義一個「新型別」的錯誤
    # 繼承自 ValueError 是一個好的實踐
    pass