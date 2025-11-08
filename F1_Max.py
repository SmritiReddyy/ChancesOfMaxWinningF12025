import numpy as np
import pandas as pd 
from itertools import combinations_with_replacement
import matplotlib.pyplot as plt
from collections import defaultdict

class F1ChampionshipPredictor:
    """
    Dynamic F1 Championship predictor - just update the standings and races!
    """
    
    def __init__(self, standings, races_remaining, sprint_races_remaining):
        """
        Initialize with current standings and remaining races
        
        Args:
            standings: dict with driver names as keys, points as values
                      e.g. {'Piastri': 346, 'Norris': 332, 'Verstappen': 306}
            races_remaining: int, number of regular races left
            sprint_races_remaining: int, number of sprint races left
        """
        self.standings = standings.copy()
        self.races_remaining = races_remaining
        self.sprint_races_remaining = sprint_races_remaining
        
        # Points systems (these are constant in F1)
        self.race_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
        self.sprint_points = [8, 7, 6, 5, 4, 3, 2, 1]
        
        # Get driver names
        self.drivers = list(standings.keys())
        self.num_drivers = len(self.drivers)
        
        # Calculate performance probabilities from current standings
        self.performance_probs = self._calculate_performance_probabilities()
    
    def _calculate_performance_probabilities(self):
        """Calculate win probabilities based on current standings"""
        total_points = sum(self.standings.values())
        probs = {}
        
        for driver in self.drivers:
            # Weight by current points (leaders more likely to perform well)
            weight = self.standings[driver] / total_points
            
            # Adjust probabilities
            probs[driver] = {
                'win': min(0.50, weight * 1.5),  # Cap at 50%
                'podium': 0.35,
                'top5': 0.10,
                'other': 0.05
            }
            
            # Normalize to sum to 1
            total = sum(probs[driver].values())
            for key in probs[driver]:
                probs[driver][key] /= total
        
        return probs
    
    def update_standings(self, new_standings):
        """Update standings after a race"""
        self.standings = new_standings.copy()
        self.performance_probs = self._calculate_performance_probabilities()
    
    def update_races_remaining(self, races, sprints):
        """Update number of races remaining"""
        self.races_remaining = races
        self.sprint_races_remaining = sprints
    
    def get_max_points_available(self):
        """Calculate maximum points still available"""
        return (self.races_remaining * 25) + (self.sprint_races_remaining * 8)
    
    def generate_all_possible_scenarios(self):
        """
        Generate ALL possible race outcome scenarios
        Returns a DataFrame with every possible combination of wins
        """
        scenarios = []
        
        # Generate all possible combinations of race wins
        for race_combo in self._generate_win_combinations(self.races_remaining, self.num_drivers):
            # For each race combination, generate sprint combinations
            for sprint_combo in self._generate_win_combinations(self.sprint_races_remaining, self.num_drivers):
                # Calculate final points for this scenario
                final_points = self.standings.copy()
                
                # Add race wins
                for driver_idx, wins in enumerate(race_combo):
                    driver = self.drivers[driver_idx]
                    final_points[driver] += wins * 25
                    
                    # Add P2/P3 points for non-wins (simplified assumption)
                    non_wins = self.races_remaining - wins
                    p2_count = non_wins // 2
                    p3_count = non_wins - p2_count
                    final_points[driver] += (p2_count * 18) + (p3_count * 15)
                
                # Add sprint wins
                for driver_idx, wins in enumerate(sprint_combo):
                    driver = self.drivers[driver_idx]
                    final_points[driver] += wins * 8
                    
                    # Add P2/P3 points for non-wins
                    non_wins = self.sprint_races_remaining - wins
                    p2_count = non_wins // 2
                    p3_count = non_wins - p2_count
                    final_points[driver] += (p2_count * 7) + (p3_count * 6)
                
                # Determine winner
                winner = max(final_points, key=final_points.get)
                
                # Create scenario entry
                scenario = {}
                for driver_idx, driver in enumerate(self.drivers):
                    scenario[f'{driver}_race_wins'] = race_combo[driver_idx]
                    scenario[f'{driver}_sprint_wins'] = sprint_combo[driver_idx]
                    scenario[f'{driver}_total'] = final_points[driver]
                
                scenario['winner'] = winner
                scenarios.append(scenario)
        
        return pd.DataFrame(scenarios)
    
    def _generate_win_combinations(self, total_races, num_drivers):
        """Generate all ways to distribute race wins among drivers"""
        combinations = []
        
        def generate(remaining, drivers_left, current):
            if drivers_left == 1:
                combinations.append(current + [remaining])
                return
            
            for i in range(remaining + 1):
                generate(remaining - i, drivers_left - 1, current + [i])
        
        generate(total_races, num_drivers, [])
        return combinations
    
    def analyze_scenarios(self, target_driver=None):
        """
        Analyze all scenarios and provide insights
        
        Args:
            target_driver: Name of driver to analyze (default: current leader)
        """
        if target_driver is None:
            target_driver = max(self.standings, key=self.standings.get)
        
        print("=" * 80)
        print("F1 CHAMPIONSHIP SCENARIO ANALYSIS")
        print("=" * 80)
        print()
        
        # Current standings
        print("CURRENT STANDINGS:")
        print("-" * 80)
        sorted_standings = sorted(self.standings.items(), key=lambda x: x[1], reverse=True)
        for pos, (driver, points) in enumerate(sorted_standings, 1):
            print(f"P{pos}. {driver:20} {points:4} points")
        print()
        
        # Race info
        print("REMAINING RACES:")
        print("-" * 80)
        print(f"Regular races:     {self.races_remaining}")
        print(f"Sprint races:      {self.sprint_races_remaining}")
        print(f"Total events:      {self.races_remaining + self.sprint_races_remaining}")
        print(f"Max points available: {self.get_max_points_available()}")
        print()
        
        # Generate all scenarios
        print("Generating all possible scenarios...")
        df = self.generate_all_possible_scenarios()
        print(f"Total scenarios analyzed: {len(df)}")
        print()
        
        # Overall statistics
        print("CHAMPIONSHIP PROBABILITIES (All Scenarios):")
        print("-" * 80)
        winner_counts = df['winner'].value_counts()
        for driver in self.drivers:
            count = winner_counts.get(driver, 0)
            percentage = (count / len(df)) * 100
            print(f"{driver:20} {count:5} / {len(df):5} = {percentage:6.2f}%")
        print()
        
        # Analyze specific driver
        print(f"DETAILED ANALYSIS FOR {target_driver.upper()}:")
        print("-" * 80)
        
        target_wins = df[df['winner'] == target_driver]
        
        if len(target_wins) == 0:
            print(f"WARNING: {target_driver} does NOT win in ANY scenario!")
            print()
            
            # Show what they need
            current_points = self.standings[target_driver]
            leader = max(self.standings, key=self.standings.get)
            leader_points = self.standings[leader]
            gap = leader_points - current_points
            
            print(f"Current gap to leader ({leader}): {gap} points")
            print(f"Maximum available points: {self.get_max_points_available()}")
            
            if gap >= self.get_max_points_available():
                print("Mathematically ELIMINATED (gap larger than max points)")
            else:
                print("Still mathematically possible, but needs near-perfect execution")
        else:
            print(f"{target_driver} wins in {len(target_wins)} scenarios ({len(target_wins)/len(df)*100:.1f}%)")
            print()
            print("-" * 80)
            
            # Minimum requirements - find the scenario with fewest total wins
            target_wins = target_wins.copy()  # Fix pandas warning
            target_wins['total_wins'] = target_wins[f'{target_driver}_race_wins'] + target_wins[f'{target_driver}_sprint_wins']
            min_total_wins_row = target_wins.loc[target_wins['total_wins'].idxmin()]
    
            
            print("MINIMUM WINNING SCENARIO (fewest total wins):")
            print("  Race wins: {min_race_wins} out of {self.races_remaining}")
            print("  Sprint wins: {min_sprint_wins} out of {self.sprint_races_remaining}")
            print("  Total events won: {min_race_wins + min_sprint_wins} out of {self.races_remaining + self.sprint_races_remaining}")
            print()
            print("-" * 80)
            
            # Show range
            abs_min_races = target_wins[f'{target_driver}_race_wins'].min()
            abs_max_races = target_wins[f'{target_driver}_race_wins'].max()
            abs_min_sprints = target_wins[f'{target_driver}_sprint_wins'].min()
            abs_max_sprints = target_wins[f'{target_driver}_sprint_wins'].max()
            
            print(f"RANGE OF WINNING COMBINATIONS:")
            print(f"  Race wins: {abs_min_races} to {abs_max_races}")
            print(f"  Sprint wins: {abs_min_sprints} to {abs_max_sprints}")
            print()
            print("-" * 80)
            
            # Count scenarios by race wins
            print(f"BREAKDOWN OF WINNING SCENARIOS:")
            for races in range(abs_min_races, abs_max_races + 1):
                race_scenarios = target_wins[target_wins[f'{target_driver}_race_wins'] == races]
                if len(race_scenarios) > 0:
                    sprint_range = f"{race_scenarios[f'{target_driver}_sprint_wins'].min()}-{race_scenarios[f'{target_driver}_sprint_wins'].max()}"
                    print(f"  {races} race wins: {len(race_scenarios)} scenarios (sprint wins needed: {sprint_range})")
            print()
            print("-" * 80)
            
            # Win rate by race wins
            print("Win probability by race wins:")
            print("-" * 80)
            for race_wins in range(self.races_remaining + 1):
                subset = df[df[f'{target_driver}_race_wins'] == race_wins]
                if len(subset) > 0:
                    wins = len(subset[subset['winner'] == target_driver])
                    print(f"{race_wins} race wins: {wins:3}/{len(subset):3} = {wins/len(subset)*100:5.1f}%")
            print()
            print("-" * 80)
            
            # Show example scenarios
            print(f"ALL WINNING SCENARIOS FOR {target_driver.upper()}:")
            print("=" * 80)
            print()
            print("-" * 80)
            
            # Show all winning scenarios with clear breakdown
            for idx, row in target_wins.iterrows():
                scenario_num = list(target_wins.index).index(idx) + 1
                print(f"\nScenario {scenario_num}:")
                print("-" * 80)
                
                # Race wins breakdown with positions
                print("RACE RESULTS (5 races):")
                race_wins = {driver: int(row[f'{driver}_race_wins']) for driver in self.drivers}
                
                # Calculate remaining positions
                total_races = self.races_remaining
                races_distributed = sum(race_wins.values())
                
                # Show who wins what
                for driver in self.drivers:
                    wins = race_wins[driver]
                    non_wins = total_races - wins
                    
                    # Simplified: assume even P2/P3 split for non-wins
                    p2s = non_wins // 2
                    p3s = non_wins - p2s
                    
                    result_str = []
                    if wins > 0:
                        result_str.append(f"{wins}xP1")
                    if p2s > 0:
                        result_str.append(f"{p2s}xP2")
                    if p3s > 0:
                        result_str.append(f"{p3s}xP3")
                    
                    print(f"  {driver:15} {', '.join(result_str) if result_str else 'No points'}")
                
                print()
                print("-" * 80)
                print("\nSPRINT RESULTS (2 sprints):")
                sprint_wins = {driver: int(row[f'{driver}_sprint_wins']) for driver in self.drivers}
                
                for driver in self.drivers:
                    wins = sprint_wins[driver]
                    non_wins = self.sprint_races_remaining - wins
                    
                    p2s = non_wins // 2
                    p3s = non_wins - p2s
                    
                    result_str = []
                    if wins > 0:
                        result_str.append(f"{wins}xP1")
                    if p2s > 0:
                        result_str.append(f"{p2s}xP2")
                    if p3s > 0:
                        result_str.append(f"{p3s}xP3")
                    
                    print(f"  {driver:15} {', '.join(result_str) if result_str else 'No points'}")
                
                print()
                print("-" * 80)
                print("\nFINAL CHAMPIONSHIP STANDINGS:")
                final_points = [(driver, int(row[f'{driver}_total'])) for driver in self.drivers]
                final_points.sort(key=lambda x: x[1], reverse=True)
                for pos, (driver, points) in enumerate(final_points, 1):
                    current_pts = self.standings[driver]
                    gained = points - current_pts
                    marker = " <- CHAMPION" if driver == target_driver else ""
                    print(f"  P{pos}. {driver:15} {points} points (+{gained} from current){marker}")
                
                print()
                print("-" * 80)
                # Calculate gaps
                target_points = int(row[f'{target_driver}_total'])
                print("\nCHAMPIONSHIP MARGIN:")
                gaps = []
                for driver in self.drivers:
                    if driver != target_driver:
                        rival_points = int(row[f'{driver}_total'])
                        gap = target_points - rival_points
                        gaps.append(f"{driver}: +{gap}")
                print(f"  {target_driver} wins by: {', '.join(gaps)}")
            
            print("\n" + "=" * 80)
        
        print()
        print("=" * 80)
        
        return df
    
    def run_monte_carlo(self, n_simulations=10000):
        """Run Monte Carlo simulation based on performance probabilities"""
        winners = defaultdict(int)
        
        for _ in range(n_simulations):
            final_points = self.standings.copy()
            
            # Simulate races
            for _ in range(self.races_remaining):
                race_result = self._simulate_single_event(is_sprint=False)
                for driver, points in race_result.items():
                    final_points[driver] += points
            
            # Simulate sprints
            for _ in range(self.sprint_races_remaining):
                sprint_result = self._simulate_single_event(is_sprint=True)
                for driver, points in sprint_result.items():
                    final_points[driver] += points
            
            winner = max(final_points, key=final_points.get)
            winners[winner] += 1
        
        probabilities = {driver: (count / n_simulations) * 100 
                        for driver, count in winners.items()}
        
        return probabilities
    
    def _simulate_single_event(self, is_sprint=False):
        """Simulate a single race or sprint"""
        points_system = self.sprint_points if is_sprint else self.race_points
        results = {}
        
        for driver in self.drivers:
            rand = np.random.random()
            probs = self.performance_probs[driver]
            
            if rand < probs['win']:
                results[driver] = points_system[0]
            elif rand < probs['win'] + probs['podium']:
                rng = np.random.default_rng(seed=42)  # Replace 42 with your desired seed value
                results[driver] = rng.choice([points_system[1], points_system[2]])
            elif rand < probs['win'] + probs['podium'] + probs['top5']:
                rng = np.random.default_rng(seed=42)
                results[driver] = rng.choice(points_system[3:5])
            else:
                rng = np.random.default_rng(seed=42)  
                results[driver] = rng.choice(points_system[5:])
        
        return results
    
    def print_full_report(self, target_driver=None):
        """Print comprehensive analysis report"""
        # Scenario analysis
        df = self.analyze_scenarios(target_driver)
        
        # Monte Carlo
        print()
        print("MONTE CARLO SIMULATION (10,000 iterations):")
        print("-" * 80)
        mc_probs = self.run_monte_carlo(10000)
        for driver in sorted(mc_probs, key=mc_probs.get, reverse=True):
            print(f"{driver:20} {mc_probs[driver]:6.2f}%")
        
        print()
        print("=" * 80)
        print("Analysis complete!")
        print("=" * 80)
        
        # Save to CSV
        df.to_csv('f1_all_scenarios.csv', index=False)
        print("\nAll scenarios saved to 'f1_all_scenarios.csv'")
        
        return df

if __name__ == "__main__":

    # CHANGE THESE VALUES AFTER EACH RACE
    # After Austin 
    # current_standings = {
    #     'Piastri': 346,
    #     'Norris': 332,
    #     'Verstappen': 306
    # }
    
    # races_remaining = 5  # Regular grand prix races left
    # sprint_races_remaining = 2  # Sprint races left

    # After Mexico 

    # current_standings = {
    #     'Piastri': 356,
    #     'Norris': 357,
    #     'Verstappen': 321
    # }
    
    # races_remaining = 4  # Regular grand prix races left
    # sprint_races_remaining = 2  # Sprint races left

    current_standings = {
        'Piastri': 356,
        'Norris': 365,
        'Verstappen': 326
    }
    
    races_remaining = 4  # Regular grand prix races left
    sprint_races_remaining = 1  # Sprint races left

    predictor = F1ChampionshipPredictor(
        standings=current_standings,
        races_remaining=races_remaining,
        sprint_races_remaining=sprint_races_remaining
    )
    
    # Analyze Verstappen only
    print("=" * 80)
    print("VERSTAPPEN CHAMPIONSHIP ANALYSIS")
    print("=" * 80)
    predictor.analyze_scenarios(target_driver='Verstappen')
    
    