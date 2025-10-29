# File: features/stock_data.feature
Feature: Stock Data Provider for Daily War Report
  As a trader,
  In order to generate the "Daily War Report" (戰情日報),
  I need to fetch and calculate key market data for my target stocks.

Background:
  Given the system is running on a valid market date

Scenario Outline: Successfully fetch latest market data for a stock
  Given I have a target stock ticker "<Ticker>"
  When I execute the "Data Fetching" process
  Then I should receive a data structure
  And this structure must contain valid data for the following columns:
    | column      |
    | Close       |
    | 5MA         |
    | 20MA        |
    | 60MA        |
    | 120MA       |
    | RSI         |
    | 20MA_Volume |

  Examples:
    | Ticker    |
    | 2330.TW   |
    | 3017.TW   |
    | 2382.TW   |

Scenario: Handle data fetching failure for an invalid stock
  Given I have an invalid stock ticker "INVALID_CODE.TW"
  When I execute the "Data Fetching" process
  Then the system should raise a "DataFetchError"