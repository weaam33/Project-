# Africa Map Coloring — CSP Game

A visual, interactive **Constraint Satisfaction Problem (CSP)** game built with **Pygame**.  
Color the map of Africa so that no two adjacent countries share the same color — or watch the AI solve it step by step.

---

## Features

-  **Interactive Africa map** with 54 countries and real adjacency data
-  **Two AI algorithms**: Backtracking and Forward Checking
-  **Three toggleable heuristics**: MRV, Degree Heuristic, LCV
-  **Manual mode**: color the map yourself and see if you can solve it
-  **Step-by-step AI visualization** with speed control
-  **3–6 color options** to adjust difficulty


```
## How to Play

### Manual Mode
1. Select **Manual** on the menu screen
2. Choose the number of colors (3–6)
3. Click any country on the map → a color picker appears
4. Pick a color — adjacent countries **must not** share the same color
5. Complete the whole map without conflicts to win!



### AI Mode
1. Select **AI** on the menu screen
2. Choose an **Algorithm** (Backtracking or Forward Checking)
3. Toggle **Heuristics** on or off (see below)
4. Press **Start ▶**
5. In the game screen:
   - **AI Step ▷** — advance one step at a time
   - **Run AI ▶** — run automatically
   - **Pause ⏸** — pause/resume
   - **← → arrow keys** — adjust speed



## Algorithms

| Algorithm            | Description                                                                                                                                 |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| **Backtracking**     | Classic recursive search. Assigns colors one country at a time; undoes (backtracks) when a conflict is found.                               |
| **Forward Checking** | After each assignment, removes the assigned color from all uncolored neighbors' domains. Detects dead-ends earlier than plain backtracking. |


## Heuristics

Heuristics guide *which* variable to assign next and *which* value to try first. They can be toggled independently on the menu screen.

| Heuristic                          | What it does                                                                                                               |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| **MRV** (Min Remaining Values)     | Pick the country with the **fewest legal colors** remaining. Finds failures faster.                                        |
| **Degree Heuristic**               | Among MRV ties, pick the country with the **most uncolored neighbors**. Used as a tiebreaker after MRV.                    |
| **LCV** (Least Constraining Value) | Try the color that **eliminates the fewest options** from neighboring countries first. Keeps more flexibility for later assignments. |

Combining all three heuristics typically produces the **fewest backtracks** and fastest solutions.


### Key Components inside `map_coloring.py`

| Section          | Description |
|---               |---                                                            |
| `COUNTRY_POLYS`  | Lon/lat polygon data for all 54 African countries             |
| `ADJACENCY`      | Hand-coded land-border adjacency graph                        |
| `CSPSolver`      | Core solver: backtracking, forward checking, MRV, Degree, LCV |
| `AfricaMapGame`  | Pygame game loop, rendering, manual & AI interaction          |

---

## Win / Lose Conditions

-  **Win** — Every country is colored and **no two adjacent countries share a color**
-  **Lose** — Two neighboring countries have the **same color** (manual mode only)

---

## Tips

- Start with **4 colors** — the classic map-coloring theorem guarantees a solution always exists with 4.
- Use **3 colors** for a harder challenge (not always solvable for all map shapes).
- Enable **all three heuristics** in AI mode to see the fastest, most efficient solve.
- Use **AI Step** mode to learn how backtracking and forward checking work in practice.

---

## License

MIT — free to use, modify, and share.
