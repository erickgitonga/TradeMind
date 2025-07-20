# modules/position_sizer.py

def calculate_position_size(capital, risk_percent, entry_price, stop_loss_price):
    risk_amount = capital * (risk_percent / 100)
    stop_loss_per_unit = abs(entry_price - stop_loss_price)
    if stop_loss_per_unit == 0:
        return 0
    position_size = risk_amount / stop_loss_per_unit
    return round(position_size, 6)
