import pandas as pd
import yfinance as yf

from errors import DataFetchError  # 導入我們剛建立的自訂錯誤


# 這裡的 : str 和 -> pd.DataFrame 就是「型別提示 (Type Hinting)」
# 這是給 VS Code (Pylance) 看的「君子協定」
def get_raw_data(ticker_symbol: str) -> pd.DataFrame:
    """
    從 yfinance 獲取指定 Ticker 的原始歷史數據。
    抓取 1 年數據以確保足夠計算所有 MA 和 RSI。
    (此 period="1y" 是由 tests/test_data_fetcher.py 所驅動的)
    """
    try:
        # 這是 TDD 測試中被 'mocker.patch' 攔截的地方
        ticker = yf.Ticker(ticker_symbol)

        # 這是 TDD 測試中 'mock_ticker.history' 被呼叫的地方
        data = ticker.history(period="1y")

        if data.empty:
            # 這是 'test_get_raw_data_failure_empty' 所測試的情境
            raise DataFetchError(f"No data found for ticker {ticker_symbol}")

        return data

    except Exception as e:
        # 這是為了穩健性：捕獲 yfinance 可能的其他錯誤
        # 我們把它「包裝」成我們自訂的錯誤
        raise DataFetchError(f"Failed to fetch data for {ticker_symbol}: {e}")
