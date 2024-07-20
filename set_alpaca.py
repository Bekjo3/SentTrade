from alpaca_trade_api.rest import REST

def setup_alpaca(api_key, secret_key, base_url='https://paper-api.alpaca.markets'):
    alpaca = REST(api_key, secret_key, base_url)
    return alpaca

def get_current_positions(alpaca):
    positions = alpaca.list_positions()
    return {position.symbol: int(position.qty) for position in positions}

def trade_stock(alpaca, sentiment_score, stock_symbol, min_sentiment_threshold=-0.5):
    positions = get_current_positions(alpaca)
    
    try:
        if sentiment_score > 0:
            print(f"Buying {stock_symbol}")
            alpaca.submit_order(
                symbol=stock_symbol,
                qty=10,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        elif sentiment_score < min_sentiment_threshold and stock_symbol in positions and positions[stock_symbol] > 0:
            print(f"Selling {stock_symbol}")
            alpaca.submit_order(
                symbol=stock_symbol,
                qty=positions[stock_symbol],
                side='sell',
                type='market',
                time_in_force='gtc'
            )
    except Exception as e:
        print(f"Error trading stock {stock_symbol}: {e}")
