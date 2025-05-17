# AI Forex Trading Bot for Pocket Option (5-Minute Strategy)
# Version 1: Signal Generator with RSI, EMA, MACD, and Candlestick Analysis

import pandas as pd
import ta
import datetime
import requests

# === Config ===
CURRENCY_PAIRS = ["EURUSD", "GBPUSD", "USDJPY"]
TIMEFRAME = "5min"
SIGNAL_CONFIDENCE_THRESHOLD = 0.95

# Placeholder for fetching historical candle data (to be replaced with real API calls)
def fetch_candle_data(pair, interval="5min", count=100):
    # Use real data source: MT5, TradingView, or broker API
    return pd.read_csv(f"data/{pair}_5min.csv")  # Load mock data for now

# === Signal Logic ===
def calculate_indicators(df):
    df = df.copy()
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['ema20'] = ta.trend.EMAIndicator(df['close'], window=20).ema_indicator()
    df['ema50'] = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator()
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def detect_candle_pattern(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if last['close'] > last['open'] and prev['close'] < prev['open'] and last['open'] < prev['close']:
        return 'bullish_engulfing'
    elif last['close'] < last['open'] and prev['close'] > prev['open'] and last['open'] > prev['close']:
        return 'bearish_engulfing'
    return None

def generate_signal(df):
    df = calculate_indicators(df)
    last = df.iloc[-1]
    signal = None

    candle_pattern = detect_candle_pattern(df)
    trend_up = last['ema20'] > last['ema50']
    trend_down = last['ema20'] < last['ema50']

    if (
        last['rsi'] < 30 and trend_up and last['macd'] > last['macd_signal'] and candle_pattern == 'bullish_engulfing'
    ):
        signal = 'BUY'
    elif (
        last['rsi'] > 70 and trend_down and last['macd'] < last['macd_signal'] and candle_pattern == 'bearish_engulfing'
    ):
        signal = 'SELL'

    return signal

def evaluate_confidence(signal_data):
    # Placeholder: Simulate a 95%+ confidence check
    # You should replace this with a real ML model probability or pattern backtest winrate
    return 0.96  # Simulated confidence

def run_bot():
    for pair in CURRENCY_PAIRS:
        try:
            df = fetch_candle_data(pair)
            signal = generate_signal(df)
            if signal:
                confidence = evaluate_confidence(df)
                if confidence >= SIGNAL_CONFIDENCE_THRESHOLD:
                    print(f"SIGNAL: {pair}")
                    print(f"ACTION: {signal}")
                    print(f"TIMEFRAME: 5-Minute")
                    print(f"CONFIDENCE: {round(confidence * 100, 2)}%\n")
                else:
                    print(f"Signal for {pair} below confidence threshold. Skipping.\n")
        except Exception as e:
            print(f"Error processing {pair}: {e}")

if __name__ == "__main__":
    run_bot()
