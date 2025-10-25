
*Last updated: October 24, 2025*
*I will add a new file with the new outputs after each race and recalcualte everything* 

# F1 2025 Championship Predictor: Max Verstappen's Chances

A Python-based machine learning model to predict Max Verstappen's chances of winning the 2025 F1 World Championship using exhaustive scenario analysis and Monte Carlo simulation.

## Overview

This project analyzes all possible race outcomes for the remainder of the 2025 F1 season to determine the probability of Max Verstappen winning the championship. The model considers:
- Current championship standings
- Remaining races (both regular Grand Prix and Sprint races)
- All possible win combinations
- Points distribution scenarios

## Features

- **Exhaustive Scenario Analysis**: Generates every possible combination of race outcomes
- **Monte Carlo Simulation**: Runs 10,000 probabilistic simulations based on current form
- **Dynamic Updates**: Easily update standings after each race
- **Detailed Breakdown**: Shows exact requirements for championship victory
- **Winner Scenario Analysis**: Lists all specific scenarios where a driver wins

## Current Situation (Pre-Mexico GP)
```
P1. Piastri     346 points
P2. Norris      332 points  (-14)
P3. Verstappen  306 points  (-40)
```

**Races Remaining**: 5 regular races + 2 sprint races = 141 points available


## Key Findings

Based on current analysis (pre-Mexico GP):

### Championship Probabilities
- **Piastri**: 68.25% (86/126 scenarios)
- **Norris**: 26.98% (34/126 scenarios)
- **Verstappen**: 4.76% (6/126 scenarios)

### Verstappen's Requirements
- **Must win**: ALL 5 remaining races (100% win rate required)
- **Sprint races**: Can win 0-2 sprints (optional with all race wins)
- **Total scenarios**: Only 6 out of 126 possible scenarios result in Verstappen championship

### Critical Insight
Even if Max wins all 5 remaining races, he can still lose the championship if:
- Piastri consistently finishes P2 behind him
- The final margin could be as close as 3-4 points

## Sample Output
```
VERSTAPPEN CHAMPIONSHIP ANALYSIS
================================================================================

Scenario 1:
--------------------------------------------------------------------------------
RACE RESULTS (5 races):
  Piastri         3xP2, 2xP3
  Norris          2xP2, 3xP3
  Verstappen      5xP1

SPRINT RESULTS (2 sprints):
  Piastri         1xP2, 1xP3
  Norris          1xP2, 1xP3
  Verstappen      2xP1

FINAL CHAMPIONSHIP STANDINGS:
  P1. Verstappen      447 points (+141 from current) <- CHAMPION
  P2. Piastri         443 points (+97 from current)
  P3. Norris          426 points (+94 from current)

CHAMPIONSHIP MARGIN:
  Verstappen wins by: Piastri: +4, Norris: +21
```



## Technical Details

### Methodology
1. **Scenario Generation**: Creates all possible combinations of race wins that sum to total remaining races
2. **Points Calculation**: Applies F1 points system (25-18-15-12-10-8-6-4-2-1 for races, 8-7-6-5-4-3-2-1 for sprints)
3. **Assumption**: For non-wins, drivers receive even split of P2/P3 finishes
4. **Monte Carlo**: Uses weighted probabilities based on current standings

### Limitations
- Assumes simplified P2/P3 distribution for non-race-winners
- Does not account for DNFs, penalties, or weather conditions
- Does not consider track-specific performance characteristics
- Team orders and strategy not explicitly modeled

## Race Calendar (Remaining)

| Race | Date | Sprint? |
|------|------|---------|
| Mexico City GP | Oct 27 | No |
| São Paulo GP | Nov 3 | Yes |
| Las Vegas GP | Nov 23 | No |
| Qatar GP | Nov 30 | Yes |
| Abu Dhabi GP | Dec 8 | No |


Feel free to fork this repository and submit pull requests for:
- Enhanced prediction models
- Track-specific adjustments
- Improved visualization
- Additional analysis features

## License

MIT License - feel free to use and modify for your own analysis!

## Author

**Smriti Reddy** - [SmritiReddyy](https://github.com/SmritiReddyy)

## Acknowledgments

- F1 points system and race data
- Inspired by the dramatic 2025 championship battle
- Built with Python, NumPy, and Pandas

---


**Verdict**: Verstappen needs perfection. 5 wins out of 5. No room for error. 
