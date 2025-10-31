# File: features/global_risk.feature
Feature: Global Risk Monitor Data Provider
  As a trader,
  In order to generate the "Global Risk Report" (全域風控日報),
  I need to fetch key market indicators.

Background:
  Given the system is running on a valid market date

Scenario Outline: Successfully fetch latest global risk indicators
  Given I have a target market indicator "<Indicator>"
  And its yfinance ticker is "<Ticker>"
  When I execute the "Global Risk Fetching" process
  Then I should receive a single, valid numerical value for this indicator
  And this value must be greater than 0

  Examples:
    | Indicator   | Ticker    |
    | TAIEX Index | ^TWII     |
    | VIX         | ^VIX      |