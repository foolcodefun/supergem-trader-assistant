# 檔案: tests/test_data_fetcher.py
import pandas as pd
import pytest
import yfinance as yf  # 雖然我們不會真的呼叫它，但 mocker 需要它

# 導入我們「即將」建立的模組
from data_fetcher import get_raw_data
from errors import DataFetchError


def test_get_raw_data_success(mocker):
    """
    測試 (情境1): 當 yfinance 成功回傳數據時,
    函式應能正確回傳一個 pandas DataFrame。
    """
    # 1. 準備 (Arrange)
    # 建立一個「假」的 yfinance 回傳數據
    mock_df = pd.DataFrame({"Close": [100, 101, 102]})

    # (關鍵) 模擬 yfinance.Ticker 物件
    mock_ticker = mocker.MagicMock()
    mock_ticker.history.return_value = mock_df

    # (關鍵) 「劫持」yfinance 模組的 Ticker 類別
    # 告訴 pytest:「當程式碼中出現 'yfinance.Ticker' 時,
    # 不要真的去執行它, 而是回傳我指定的 mock_ticker」
    mocker.patch("yfinance.Ticker", return_value=mock_ticker)

    # 2. 執行 (Act)
    result = get_raw_data("2330.TW")

    # 3. 斷言 (Assert)
    assert isinstance(result, pd.DataFrame)  # 驗證型別
    assert not result.empty  # 驗證不為空
    assert result["Close"].iloc[0] == 100  # 驗證內容
    yf.Ticker.assert_called_with("2330.TW")  # 驗證 Ticker 被正確呼叫
    mock_ticker.history.assert_called_with(period="1y")  # 驗證我們抓了 1 年數據


def test_get_raw_data_failure_empty(mocker):
    """
    測試 (情境2): 當 yfinance 回傳「空」數據 (例如無效 Ticker) 時,
    函式應拋出我們自訂的 DataFetchError。
    """
    # 1. 準備 (Arrange)
    mock_df = pd.DataFrame()  # 模擬空的回傳
    mock_ticker = mocker.MagicMock()
    mock_ticker.history.return_value = mock_df
    mocker.patch("yfinance.Ticker", return_value=mock_ticker)

    # 2. 執行 (Act) & 3. 斷言 (Assert)
    # (關鍵) 我們「預期」這段程式碼會拋出 DataFetchError
    # 'match' 參數會驗證錯誤訊息中是否包含 "No data found"
    with pytest.raises(DataFetchError, match="No data found"):
        get_raw_data("INVALID_CODE")
