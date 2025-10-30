# 檔案: tests/test_data_processor.py
import pytest
import pandas as pd
import numpy as np # 用來生成假數據

# 導入我們「即將」建立的模組
from data_processor import add_technical_indicators

@pytest.fixture
def sample_raw_data() -> pd.DataFrame: # <-- (已補上你建議的 Type Hint)
    """
    [Fixture 夾具] 建立一個可重用的「假數據 (Mock Data)」產生器。

    我們模擬 DataFetcher 抓了 200 天的數據，
    以確保「足夠」計算 BDD 規格中最長天期的 120MA。
    """
    days = 200 
    data = {
        'Open': np.random.rand(days) * 100 + 100,
        'High': np.random.rand(days) * 10 + 110,
        'Low': np.random.rand(days) * 10 + 90,
        'Close': np.random.rand(days) * 10 + 100,
        'Volume': np.random.randint(1000, 5000, size=days)
    }
    index = pd.date_range(start='2024-01-01', periods=days, freq='B') 
    return pd.DataFrame(data, index=index)

def test_add_technical_indicators(sample_raw_data: pd.DataFrame): # <-- (已補上 Type Hint)
    """
    [TDD 測試] 驗證 'add_technical_indicators' 函式 (我們的「廚師」) 
    是否能 100% 滿足 BDD 規格。
    """
    # ---
    # 1. 準備 (Arrange)
    # ---
    # Pytest 會自動執行 @pytest.fixture 並注入 'sample_raw_data' (一個 200 天的 DataFrame)

    # ---
    # 2. 執行 (Act)
    # ---
    # 呼叫我們「即將」建立的函式 (src/data_processor.py)
    processed_df = add_technical_indicators(sample_raw_data)

    # ---
    # 3. 斷言 (Assert) - 執行「穩健性」驗證
    # ---

    # 3a. 驗證「型別」：確保函式回傳的是我們預期的 DataFrame 物件。
    assert isinstance(processed_df, pd.DataFrame)

    # 3b. 驗證「BDD 規格 (契約)」：
    # 確保 BDD feature 檔中要求的所有欄位都「被新增」了。
    expected_columns = [
        'Close', '5MA', '20MA', '60MA', '120MA', 'RSI', '20MA_Volume'
    ]
    for col in expected_columns:
        assert col in processed_df.columns

    # 3c. 驗證「穩健性」：
    #
    # [架構師筆記：為什麼用「屬性驗證」而不是「固定值驗證」？]
    # 1. (信任依賴) 我們的 TDD **不是**要測試 'pandas-ta' 的數學對不對
    #    (那是 'pandas-ta' 自己的責任)。
    # 2. (職責分離) 我們的 TDD **是**要測試「我們的程式碼 ('add_technical_indicators')」
    #    是否「正確地呼叫了 'pandas-ta'」並「正確地新增了欄位」。
    # 3. (避免脆弱) 如果 'pandas-ta' 未來升級、改變了四捨五入邏輯，
    #    「固定值測試」(e.g., assert ma == 102.5) 會「錯誤地失敗」，
    #    導致我們浪費時間去 Debug 一個「不存在的 Bug」。
    # 4. (穩健策略) 因此，我們只驗證「屬性 (Property)」：
    #    我們斷言「RSI 必須介於 0-100 之間」、「MA 必須大於 0」。
    #    這證明了 'pandas-ta' 確實被呼叫了、且回傳了「合法」的數值。

    # (因為 MA 和 RSI 在計算初期會是 NaN (空值), 
    #  我們使用 .dropna() 來只驗證「有值」的部分)

    assert processed_df['RSI'].dropna().between(0, 100).all()
    assert processed_df['5MA'].dropna().gt(0).all()
    assert processed_df['120MA'].dropna().gt(0).all() # (驗證最長的)
    assert processed_df['20MA_Volume'].dropna().gt(0).all()