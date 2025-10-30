# 檔案: src/data_processor.py
import pandas as pd
import pandas_ta as ta

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    使用 pandas_ta 套件, 在原始 DataFrame 上計算並新增
    BDD 規格中所需的所有技術指標。

    :param df: 包含 OHLCV 原始數據的 DataFrame (來自 DataFetcher)
    :return: 一個**新的** DataFrame, 包含了原始數據 + 所有技術指標
    """

    # 複製一份 DataFrame, 避免修改到原始傳入的 data
    # (這叫做「無副作用 (No Side-effects)」, 
    #  是 'Effective Python' 的核心原則)
    data = df.copy()

    # --- 1. 計算 BDD 規格中的價格指標 ---

    # (BDD: 5MA, 20MA, 60MA, 120MA)
    # .ta.sma() 會自動尋找 'Close' 欄位來計算
    data.ta.sma(length=5, append=True, col_names='5MA')
    data.ta.sma(length=20, append=True, col_names='20MA')
    data.ta.sma(length=60, append=True, col_names='60MA')
    data.ta.sma(length=120, append=True, col_names='120MA')

    # (BDD: RSI)
    data.ta.rsi(length=14, append=True, col_names='RSI')

    # --- 2. 計算 BDD 規格中的量能指標 ---

    # (BDD: 20MA_Volume)
    # .ta.sma() 可以指定要計算的欄位 (on='Volume')
    data.ta.sma(length=20, on='Volume', append=True, col_names='20MA_Volume')

    # (TDD 測試 'test_add_technical_indicators' 
    #  會自動驗證這些欄位是否都已成功新增)

    return data