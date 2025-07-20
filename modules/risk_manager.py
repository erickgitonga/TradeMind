# modules/risk_manager.py

def calculate_position_size(capital, risk_percent, entry_price, stop_loss_price):
    """
    Calculates position size based on capital and risk tolerance.
    """
    risk_amount = capital * (risk_percent / 100)
    stop_loss_per_unit = abs(entry_price - stop_loss_price)
    
    if stop_loss_per_unit == 0:
        return 0
    
    position_size = risk_amount / stop_loss_per_unit
    return round(position_size, 6)


# modules/risk_manager.py

def apply_risk_management(signal, entry_price, current_price, stop_loss_pct, take_profit_pct):
    if signal not in ['BUY', 'SELL']:
        return "NO_ACTION"

    stop_loss_price = entry_price * (1 - stop_loss_pct / 100)
    take_profit_price = entry_price * (1 + take_profit_pct / 100)

    if current_price <= stop_loss_price:
        return "STOP_LOSS_TRIGGERED"
    elif current_price >= take_profit_price:
        return "TAKE_PROFIT_TRIGGERED"
    else:
        return "HOLD_POSITION"
