import random

class SlotMachine:
    def __init__(self):
        self.slot_wheel = [
            '🍎', '🍊', '🍇', '🍒', '🍓', '🍑', '🍋', '⚡', '🧩', '🍉', 
            '🍗', '🍅', '🧲', '🔔', '💎', '🎗️', '🎰', '🃏', 
            '🎯', '🧿', '🔱', '💫', '🍬', '⚖️', 
            '🪝', '⚜️', '🍀', '☄️', '🧿'
        ]

    def spin(self, stakes):
        slots_results = [random.choice(self.slot_wheel) for _ in range(3)]
        winnings, breakdown = self._compute_winnings(slots_results, stakes)

        if '🃏' in slots_results and winnings > 0:
            winnings *= 3
            breakdown += '\nJoker : 3x'
            
        winnings = int(winnings)
        return slots_results, breakdown, winnings

    def _compute_winnings(self, results, stakes):
        if len(set(results)) == 1:
            # All same
            multipliers = {
                '🎰': 50,
                '💎': 100,
                'default': 30
            }
            return stakes * multipliers.get(results[0], multipliers['default']), f'Triples : {multipliers.get(results[0], multipliers["default"])}x'
        
        elif len(set(results)) == 2:
            # Two same
            base_multiplier = 3
            special_combos = {
                ('🪝', '🐟'): 15,
                ('🎰', '💎'): 18,
                ('🎰',): 6,
                ('💎',): 12
            }
            for combo, multiplier in special_combos.items():
                if all([sym in results for sym in combo]):
                    return stakes * multiplier, f'{"".join(combo)} : {multiplier}x'
            return stakes * base_multiplier, 'Doubles : 3x'
        
        else:
            # All different
            special_symbols = {
                '🎗️': -0.5,
                '🍀': 0,
                '🎰': 2,
                '💎': 4
            }
            for sym, multiplier in special_symbols.items():
                if sym in results:
                    return round(stakes * multiplier), f'{sym} : {multiplier}x'
            return -stakes, 'Nothing : -100%'
        
    def simulate(self, stakes, spins):
        total_winnings = 0
        win_count = 0

        for _ in range(spins):
            _, _, winnings = self.spin(stakes)
            total_winnings += winnings
            if winnings > 0:
                win_count += 1
        
        winrate = win_count / spins
        net_profit = total_winnings - (stakes * spins)
        avg_profit = net_profit / spins
        
        print(f"Winrate: {winrate*100:.2f}%")
        print(f"Net Profit: {net_profit}")
        print(f"Average Profit per Spin: {avg_profit:.2f}")