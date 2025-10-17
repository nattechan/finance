# The Game-Ready Poker Guide

## A Comprehensive 3-Day Learning Path to No-Limit Hold'em Mastery

Based on *Modern Poker Theory* by Michael Acevedo & Jonathan Little

---

## How to Use This Guide

This guide is structured for intensive learning over **3 days** (8-10 hours per day). Each day builds upon the previous:

- **Day 1**: Fundamentals, Math, and Hand Reading
- **Day 2**: GTO Principles, Preflop Strategy, and Ranges
- **Day 3**: Postflop Play, Bet Sizing, and Advanced Concepts

**Study Method**:

1. Read each section carefully
2. Work through all examples with a calculator/equity tool
3. Practice concepts with free poker software or play money games
4. Review key formulas and charts before moving to next section

**Required Tools**:

- Equity calculator: [PokerStove](http://www.pokerstove.com/) or [Equilab](https://www.pokerstrategy.com/poker-software-tools/equilab-holdem/)
- Hand range viewer: [Flopzilla](http://www.flopzilla.com/) (optional but helpful)
- Pen, paper, and calculator

---

## DAY 1: FUNDAMENTALS & MATHEMATICAL FOUNDATIONS

### Section 1.1: The Core Objective

#### Profit = Opponent Mistakes - Our Mistakes

Every decision in poker is about maximizing this equation. You have little control over opponent mistakes (except game selection), but you have complete control over minimizing your own mistakes through:

1. **Fixing leaks** in your game
2. **Understanding GTO** (Game Theory Optimal) baseline strategy
3. **Identifying and exploiting** opponent tendencies

### Section 1.2: Essential Terminology

#### Table Positions (9-handed)

**Early Position (EP)**:

- UTG (Under the Gun) - First to act preflop
- UTG+1 - Second to act
- UTG+2 - Third to act

**Middle Position (MP)**:

- Lojack (LJ) - Fourth to act
- Hijack (HJ) - Fifth to act

**Late Position (LP)**:

- Cutoff (CO) - Next-to-last to act postflop
- Button (BN) - Last to act postflop (best position)

**Blinds**:

- Small Blind (SB) - Next-to-last to act preflop, first to act postflop
- Big Blind (BB) - Last to act preflop, second to act postflop

**Key Position Rules**:

- Later position = more information = more profitable
- Position is MORE important than cards in many situations
- Being "in position" (IP) means acting last; "out of position" (OOP) means acting first

#### Critical Betting Terms

- **Raise First In (RFI)**: First person to raise when no one has entered the pot
- **3-bet**: Re-raise after someone has already raised
- **4-bet**: Re-raise after a 3-bet
- **Continuation Bet (C-bet)**: Postflop bet by the preflop aggressor
- **Donk Bet**: OOP player bets into the preflop aggressor
- **Check-Raise (x/r)**: Check, then raise after opponent bets

#### Stack Size Terminology

Always measured in **big blinds (bb)**:

- **Short Stack**: <20bb
- **Mid Stack**: 20-40bb
- **Deep Stack**: 60bb+
- **Effective Stack**: The smallest stack among active players (determines maximum pot size)

### Section 1.3: Hand Ranges and Combinatorics

#### The 13x13 Hand Grid

All 169 possible starting hands:

- **13 pocket pairs** (diagonal): AA, KK, QQ... 22
- **78 suited hands** (upper right): AKs, AQs, KQs, etc.
- **78 offsuit hands** (lower left): AKo, AQo, KQo, etc.

#### Total combinations in a 52-card deck: 1,326

#### Combinatorics Formulas

**Pocket Pairs (any rank)**:

```text
Combos = X × (X-1) / 2
```

For any pocket pair with 4 cards remaining in deck: **6 combinations**

Example: AA has 6 combinations (A♠A♥, A♠A♦, A♠A♣, A♥A♦, A♥A♣, A♦A♣)

**Unpaired Hands**:

```text
Combos = X × Y
```

Where X = number of first rank remaining, Y = number of second rank remaining

- **Suited hands**: 4 combinations (one for each suit)
- **Offsuit hands**: 12 combinations (4×4 minus 4 suited = 12)
- **Any unpaired hand** (suited + offsuit): 16 combinations

#### Example: Counting AK

- AKs: 4 combinations (A♠K♠, A♥K♥, A♦K♦, A♣K♣)
- AKo: 12 combinations (all other suit combos)
- AK total: 16 combinations

#### Card Removal Effects (Blockers)

When you hold A♠A♥, there are only **2 remaining aces** in the deck, reducing villain's AA combinations from 6 to just 1.

**Practical Application**:
If board is A♣J♥9♥ and you hold A♦3♦:

- Villain can only have 1 combo of AA (A♠A♥)
- You "block" many value hands containing an ace
- Makes villain bluffs more likely (important for river calls)

### Section 1.4: Pot Odds and Outs

#### Pot Odds Formula

#### Pot odds = Risk / (Reward + Risk)

Example: Pot is $100, villain bets $100

```text
Pot odds = 100 / (200 + 100) = 100/300 = 33.3%
```

You need to win **≥33.3%** of the time to break even on a call.

**Alternative Ratio Form**:

```text
Pot odds = 2:1 (risking $100 to win $200)
```

#### Outs and Probability

An **out** is any unseen card that improves your hand to likely best.

**Quick Mental Math for Outs**:

- **Flop to Turn**: Outs × 2 + 1 = % chance
- **Flop to River** (seeing both): Outs × 4 - 1 = % chance

**Exact Formula (Turn + River)**:

```text
Probability = 1 - [(47 - Outs) / 47] × [(46 - Outs) / 46]
```

#### Common Drawing Scenarios

| Draw Type | Outs | Turn (%) | Turn+River (%) | Ratio |
|-----------|------|----------|----------------|-------|
| Flush draw | 9 | 19.1% | 35% | 1.86:1 |
| OESD (Open-ended straight) | 8 | 17% | 31.5% | 2.17:1 |
| Gutshot (inside straight) | 4 | 8.5% | 16.5% | 5.1:1 |
| Two overcards | 6 | 12.8% | 24.1% | 3.15:1 |
| Flush draw + gutshot | 12 | 25.5% | 45% | 1.22:1 |
| Flush draw + OESD | 15 | 31.9% | 54.1% | 0.85:1 |

**Example Calculation**:

Situation: You have Q♥J♥ on A♣8♥7♥. Villain has A♠K♠ (known for example purposes).

**Outs**: 9 remaining hearts give you the flush
**Probability (Turn + River)**: 9 × 4 - 1 = **35%**

Pot is $100, villain bets $100 all-in.

- Pot odds: 33.3%
- Win probability: 35%
- **35% > 33.3% → CALL is profitable**

#### Advanced Drawing Concepts

**Backdoor Draws** (need to hit twice):

- Backdoor flush draw (BDFD): ~4.2% (equivalent to 1 out)
- Backdoor straight draw (BDSTD): ~4.2% (equivalent to 1 out)

**Dead Outs**: Outs that improve your hand but also improve villain's to a better hand.

Example: You have J♠T♠ (OESD) on Q♥9♦6♥. Any heart completing your straight ALSO gives villain with K♥x♥ a flush. Your 8 outs are reduced to **~6 live outs**.

**Implied Odds**: Expected value from future bets when you hit your draw.

**Reverse Implied Odds**: Expected loss on future streets when you hit but still lose (e.g., hitting your flush when villain has a better flush).

### Section 1.5: Equity Calculations

#### What is Equity?

**Equity** = Your share of the pot based on probability of winning if all cards were dealt out with no more betting.

#### Types of Equity

#### 1. Hand vs Hand Equity

Cannot rank hands universally - all hands are relative to opponent holdings.

Example:

- AKo beats JTs (63% vs 37%)
- 22 beats AKo (53% vs 47%)
- JTs beats 22 (52% vs 48%)

**No universal hand ranking!** (Rock-paper-scissors dynamic)

**Key Preflop Equity Matchups to Memorize**:

| Matchup | Equity |
|---------|--------|
| AA vs KK | 82% vs 18% |
| AA vs AK | 87% vs 13% |
| AK vs QQ | 43% vs 57% (coin flip) |
| AK vs AQ | 70% vs 30% (domination) |
| 22 vs AK | 52% vs 48% (coin flip) |
| Overpair vs underpair | ~82% vs 18% |
| Pair vs two overcards | ~55% vs 45% |

#### 2. Hand vs Range Equity

More practical - calculate your hand's equity against villain's estimated range.

Example:

- Villain jams 10bb from SB with tight 20% range
- You have Q♣T♠ in BB
- Pot odds: 45% (need 45% equity to call)
- Q♣T♠ vs tight 20% range: **43% equity**
- **43% < 45% → FOLD**

#### 3. Range vs Range Equity

Used for postflop analysis to see how board textures favor different ranges.

Example: CO raises 31.2% range, BB calls 56.8% range

Preflop equity: CO 58.5% vs BB 41.5%

Equity on **8♥7♠5♠** flop: CO 49.7% vs BB 50.3%

→ This "connected, low" board heavily favors BB's calling range. CO should check back frequently with overpairs like AA/KK despite having a strong hand.

### Section 1.6: Expected Value (EV)

#### The EV Formula

**EV = (%Win × $Win) - (%Lose × $Risk)**

Where:

- %Win = Your equity
- $Win = Pot + opponent's bet
- %Lose = 100% - equity
- $Risk = Amount you must call

**Critical Rules**:

- +EV = Profitable long-term
- 0EV = Break-even
- -EV = Losing long-term
- **EV of folding = 0** (money already in pot isn't yours)

#### EV Calculation Example

Setup:

- BN raises 2bb, SB (15bb stack) jams all-in
- You're in BB with A♠5♠
- SB is a regular with standard 20% rejam range

Step 1: Calculate equity

- A♠5♠ vs 20% range = **43.31% equity**

Step 2: Identify variables

- %W = 43.31%
- $W = 15bb (SB stack) + 1bb (SB dead) + 2bb (BN dead) = 18bb
- %L = 56.69%
- $R = 13bb (call amount after posting 1bb blind)

Step 3: Calculate EV

```text
EV = (0.4331 × 18) - (0.5669 × 13)
EV = 7.796 - 7.370
EV = +0.426bb
```

**Result**: Calling gains 0.426bb on average vs folding (0bb). **Call is correct**.

Over 100 hands, calling wins **42.6bb more** than folding.

#### Win Rate (bb/100)

#### bb/100 = EV × 100

In example above: 0.426 × 100 = **42.6 bb/100**

Professional win rates:

- Elite online pros: 5-10 bb/100
- Solid winning players: 3-5 bb/100
- Breakeven players: 0-2 bb/100

### Section 1.7: Fold Equity

#### Fold Equity Formula

#### FE = % Villain Folds × Pot Before Your Bet

Fold equity is the "extra" equity you gain from the possibility of opponent folding.

#### Minimum Fold Equity Required

To find breakeven fold equity for a bluff:

#### Set EV = 0 and solve for %Villain Folds

Example: You're BB (15bb) with T♦5♣

- BN raises 2bb, aggressive player with 60% range
- You consider jamming 15bb as a bluff

Setup:

- When villain folds, you win: 1bb (SB) + 2bb (BN) + 0.625bb (ante) = 3.625bb
- When villain calls, pot = 31.625bb
- You risk: 14bb
- Equity when called: ~31% (T5o vs calling range)

Calculate breakeven fold equity:

```text
0 = (FE × 3.625) + [(1 - FE) × ((0.31 × 31.625) - 14)]
0 = (FE × 3.625) + [(1 - FE) × (9.804 - 14)]
0 = (FE × 3.625) + [(1 - FE) × (-4.196)]
0 = 3.625×FE - 4.196 + 4.196×FE
4.196 = 7.821×FE
FE = 53.7%
```

Villain needs to fold **53.7%** of hands for jam to be profitable.

If villain opens 60% and calls with 28.8%, fold frequency = **52%**. Too close - **marginal jam, likely fold instead**.

### Section 1.8: Equity Realization

**Equity Realization (EqR)** = Fraction of your equity that materializes into actual EV

**Example**:

- Hand has 35% raw equity
- Due to positional disadvantage, only realizes 25% EV
- **EqR = 25% / 35% = 71.4%**

Factors affecting EqR:

**Hands that OVER-realize equity** (EqR > 100%):

- Strong made hands (sets, two-pair, straights)
- Nut draws with implied odds
- Hands in position
- Hands that can continue on many turns/rivers

**Hands that UNDER-realize equity** (EqR < 100%):

- Weak draws (gutshots)
- Medium-strength hands OOP (middle pair)
- Hands facing aggression
- Hands that struggle on many runouts

**Practical Application**:

BB vs UTG raise (40bb deep), you have 9♣5♦:

- Pot odds: 23.5% (need 23.5% equity to call)
- Raw equity vs UTG 16% range: 29.5%
- **BUT**: Facing aggression OOP with weak hand → EqR ~60%
- Realized EV: 29.5% × 0.6 = **17.7% < 23.5%**
- **FOLD despite having sufficient raw equity**

---

## Key Formulas to Memorize (Day 1)

| Concept | Formula |
|---------|---------|
| **Pot Odds (%)** | Risk / (Pot + Risk) |
| **Outs to %** (Flop→Turn) | Outs × 2 + 1 |
| **Outs to %** (Flop→River) | Outs × 4 - 1 |
| **Expected Value** | (%W × $W) - (%L × $R) |
| **Combos (Pocket Pair)** | X × (X-1) / 2 = 6 |
| **Combos (Suited)** | 4 |
| **Combos (Offsuit)** | 12 |
| **Combos (Any unpaired)** | 16 |

---

## DAY 1 Practice Exercises

**Exercise 1**: Calculate pot odds

- Pot: $50, Villain bets $25. What are pot odds?
- Answer: 25/(75+25) = 25/100 = 25%

**Exercise 2**: Calculate equity with outs

- You have flush draw (9 outs) on the flop
- What's your approximate equity to hit by river?
- Answer: 9×4-1 = 35%

**Exercise 3**: EV calculation

- 20bb effective, you have AKo in SB
- BB jams, you estimate 30% jamming range
- AKo has 52% vs range, pot is 21.5bb after you call
- Calculate EV of calling vs folding
- Answer: EV = (0.52×21.5) - (0.48×19) = 11.18 - 9.12 = +2.06bb (Call is +EV)

---

## DAY 2: GAME THEORY OPTIMAL (GTO) & PREFLOP STRATEGY

### Section 2.1: Core GTO Concepts

#### What is GTO?

**Game Theory Optimal (GTO)** = Nash Equilibrium strategy

**Nash Equilibrium**: A set of strategies where no player can improve their EV by changing strategy, assuming opponents don't change theirs.

**Key Properties of Nash Equilibrium**:

1. **Unexploitable**: Opponent cannot gain by deviating from their own Nash strategy
2. **Breakeven vs itself**: Playing Nash vs Nash results in 0EV for both players in a symmetric game
3. **Maximum exploitation protection**: Limits maximum loss against any strategy

**GTO is a BASELINE, not the goal**. You should:

- Learn GTO to understand fundamentals
- Deviate exploitatively when opponents have clear leaks
- Return to GTO vs unknown/strong opponents

#### The Indifference Principle

In GTO strategy, when you use a **mixed strategy** (sometimes do X, sometimes do Y), opponent must be **indifferent** between their options.

Example: When you bluff at the correct frequency, opponent's EV for calling = EV for folding.

This prevents them from exploiting you by always calling or always folding.

### Section 2.2: Minimum Defense Frequency (MDF)

#### MDF = Pot / (Pot + Bet)

The minimum % of your range you must continue (call or raise) to prevent opponent from profitably bluffing any two cards.

#### MDF Examples

**Example 1**: Villain bets 50% pot

```text
MDF = 100 / (100 + 50) = 66.7%
```

You must defend **≥66.7%** of your range or villain can auto-profit by bluffing 100%.

**Example 2**: Villain bets 100% pot (pot-sized bet)

```text
MDF = 100 / (100 + 100) = 50%
```

You must defend **≥50%** of range.

**Example 3**: Villain bets 200% pot (overbet)

```text
MDF = 100 / (100 + 200) = 33.3%
```

You must defend **≥33.3%** of range.

**Key Insight**: Larger bets require LESS defense frequency. This is why overbets are powerful - they put maximum pressure on opponent's range.

#### Alpha (α) - Attacker's Required Fold Equity

#### Alpha = Bet / (Pot + Bet)

The % of time opponent must fold for a pure bluff (0% equity) to break even.

**Relationship**: α + MDF = 100%

| Bet Size | MDF (Defend) | Alpha (Fold Needed) |
|----------|--------------|---------------------|
| 33% pot | 75% | 25% |
| 50% pot | 67% | 33% |
| 75% pot | 57% | 43% |
| 100% pot | 50% | 50% |
| 150% pot | 40% | 60% |
| 200% pot | 33% | 67% |

### Section 2.3: Optimal Bluffing Frequency

When constructing a balanced betting range, use this ratio:

**Bluff:Value Ratio = α : (1 - α)**

For a pot-sized bet (α = 50%):

- Bluff:Value = 0.5 : 0.5 = **1:1**
- For every value bet, include 1 bluff

For a 50% pot bet (α = 33%):

- Bluff:Value = 0.33 : 0.67 = **1:2**
- For every 2 value bets, include 1 bluff

**Example Application**:

Flop: A♥K♣7♦, pot = 100bb

You bet 75bb (75% pot), α = 43%, MDF = 57%

Your value range: AA, KK, 77, AK (let's say 20 combos)
Optimal bluffs: 20 × (0.43/0.57) = **15 combos of bluffs**

Choose bluffs with:

- Blockers to opponent's calling hands
- Equity to improve (semi-bluffs preferred)
- Hands with little/no showdown value

### Section 2.4: Preflop Ranges by Position

#### 6-max Cash Game Opening Ranges (100bb)

**UTG (16-17%)**:

- Pairs: 22+
- Suited: A2s+, K9s+, Q9s+, J9s+, T8s+, 97s+, 87s, 76s, 65s
- Offsuit: AJo+, KQo

**MP/Lojack (20-22%)**:

- Add: K8s, Q8s, J8s, T7s, 96s+, 86s+, 75s+, 64s+, 54s

**Hijack (25-27%)**:

- Add: A9o, K7s, Q7s, J7s, T6s+, 95s+, 85s+, 74s+, 63s+, 53s+

**Cutoff (30-33%)**:

- Add: K6s+, Q6s+, J6s+, T5s+, 94s+, 84s+, 73s+, 62s+, 52s+, ATo, KJo, QJo

**Button (45-50%)**:

- Add: Essentially any suited connector, suited gapper, any Ace, K5s+, Q5s+, J5s+, most offsuit broadway, many suited kings/queens

**Small Blind (30-35% vs BB)**:

- Similar to Button but slightly tighter due to being OOP postflop

#### Tournament Adjustments (20-40bb stacks)

**Key Changes**:

- Tighter from early position (UTG 12-14%)
- More aggressive steal attempts from CO/BN (35-50%)
- 3-bet or fold strategy more common (less flatting)
- Shoving 10-15bb with wide ranges from SB/BN

**Push/Fold Charts (10-15bb)**:

When <15bb, many hands become push/fold (either shove or fold, rarely raise-call or raise-fold).

**Button vs BB (12bb effective)**:

Push range (~45%): 22+, A2+, K2s+, K7o+, Q4s+, Q9o+, J7s+, JTo, T7s+, 97s+, 87s, 76s, 65s, 54s

**SB vs BB (12bb effective)**:

Push range (~35%): 22+, A2+, K2s+, K9o+, Q7s+, QTo+, J8s+, JTo, T8s+, 98s, 87s, 76s

### Section 2.5: Preflop Bet Sizing

#### General Guidelines

**Early Position**: Use smaller sizes (2-2.5x BB)

- More players left to act = more likely to face 3-bet
- Smaller size reduces risk when you fold to 3-bet
- Generates enough fold equity

**Late Position**: Can use slightly larger sizes (2.2-2.5x BB)

- Fewer players to act through = safer
- Larger size builds pot with positional advantage
- Discourages light 3-bets

**Deeper Stacks** (100bb+): Use larger sizes (2.5-3x BB)

- SPR (Stack-to-Pot Ratio) considerations
- Build pot with strong hands
- More room for postflop play

**Shorter Stacks** (<40bb): Use smaller sizes (2-2.2x BB)

- Preserve stack for critical all-in decisions
- Minimize damage from 3-bets
- Still generates folds

#### Recommended Preflop Sizes

**Cash Game (100bb)**:

- UTG/MP: 2.2-2.5x BB
- CO: 2.2-2.5x BB
- BN: 2.2-2.5x BB
- SB: 3-3.5x BB (to compensate for OOP disadvantage)

**Tournament (20-40bb)**:

- Early: 2-2.2x BB
- Late: 2-2.2x BB
- SB: 2.5-3x BB

**Tournament (10-15bb)**:

- Push/fold strategy dominates
- When raising (instead of shoving): 2-2.2x BB then fold to 3-bet shove

### Section 2.6: Defending vs 3-bets

#### Pot Odds vs 3-bets

Example: You open 2.5bb from CO, BN 3-bets to 8bb

Pot: 8bb (3-bet) + 2.5bb (your raise) + 1.5bb (blinds) = 12bb
Cost to call: 5.5bb

#### Pot odds = 5.5 / (12 + 5.5) = 31.4%

You need 31.4% equity when calling the 3-bet.

#### Defending Strategy Framework

**Against 3-bet, you have 3 options**:

1. **4-bet** (for value or as bluff)
2. **Call** (if IP with playable hand)
3. **Fold** (if OOP with weak hand or low equity)

**4-bet Ranges** (for value):

- AA, KK always
- QQ, AK depending on opponent's 3-bet frequency
- Wider if opponent 3-bets light (>12%)

**4-bet Bluff Candidates**:

- Hands with blockers (ATo-A5o, KQo-KJo block AA/KK/AK)
- Low equity vs 3-bet range but too weak to call
- Suited wheel aces (A5s-A2s) - block AA, have playability if called

**Cold Calling 3-bets** (IP only):

Position matters! Calling 3-bets OOP is very difficult.

**CO vs BN 3-bet** (IP): Can call with:

- QQ-22 (small pairs for set value)
- AQ, AJ (sometimes ATs)
- KQ, KJs, QJs
- Suited connectors (T9s, 98s, 87s)

**MP vs CO 3-bet** (OOP): Much tighter calling range:

- Only calling JJ-99, AQs, AJs
- 4-betting or folding most other hands

#### MDF vs 3-bets

If you open 2.5bb and face 8bb 3-bet:

Cost to you: 5.5bb
Pot: 12bb

#### MDF = 12 / (12 + 5.5) = 68.6%

You should defend (call or 4-bet) **~69%** of your opening range to prevent auto-profit 3-bet bluffs.

If you opened 25% range from CO, defend **~17%** of all hands (69% of 25% = 17.25%).

### Section 2.7: Squeezing

**Squeeze** = 3-betting after someone raises and another player calls

**Why squeeze?**

- Fold equity from both the raiser AND caller
- Builds a big pot when you have a strong hand
- Balances range (mix of value and bluffs)

**Squeeze Sizing**:
Larger than standard 3-bet since you need to get two players to fold.

Standard 3-bet: 3x the original raise
Squeeze: **4-5x the original raise + 1x per caller**

Example:

- MP raises 2.5bb, CO calls 2.5bb
- You're in SB with AQs
- Squeeze size: (4 × 2.5bb) + 1bb = **11bb**

**Squeeze Value Range**:

- QQ+, AK (always)
- JJ, AQs (frequently)

**Squeeze Bluff Candidates**:

- A5s-A2s (wheel aces with blocker value)
- Suited connectors (for playability if called)
- Suited Ax with blocker

---

## DAY 2 Practice Exercises

**Exercise 1**: What's MDF when villain bets 75% pot?

- MDF = 100/(100+75) = 57.1%

**Exercise 2**: You open BTN 2.5bb (18% range), SB 3-bets to 9bb. What % of hands should you defend?

- Cost: 6.5bb, Pot: 12bb
- MDF = 12/18.5 = 64.9%
- Defend: 64.9% of 18% = 11.7% of all hands

**Exercise 3**: Construct balanced betting range for pot-sized bet

- α = 50%, so bluff:value = 1:1
- If you have 15 value combos, include 15 bluff combos

---

## DAY 3: POSTFLOP PLAY & ADVANCED CONCEPTS

### Section 3.1: Flop Textures and Range Advantage

#### Static vs Dynamic Boards

**Static (Dry) Boards**: Few draws, equity doesn't change much on turn/river

- Examples: K♦7♥2♣, A♣Q♦4♠, J♠6♦3♣
- Characteristics:
  - Limited draws
  - Equity remains stable across streets
  - Encourages smaller bets or checking
  - Good for pot control

**Dynamic (Wet) Boards**: Many draws, equity shifts dramatically

- Examples: Q♥J♥T♠, 9♦8♥7♣, K♠J♠5♠
- Characteristics:
  - Flush draws and straight draws present
  - Big equity shifts on turn/river
  - Encourages larger bets to deny equity
  - Difficult to control pot

#### Range Advantage vs Nut Advantage

**Range Advantage**: Player whose range contains more high-equity hands overall

**Nut Advantage**: Player whose range contains more nut hands (extremely strong holdings)

**Example**: CO raises, BB calls. Flop: A♥K♣Q♦

- **Range advantage**: CO (preflop raiser has more Ax, Kx, Qx)
- **Nut advantage**: CO (has more AK, AQ, KQ, AA, KK, QQ, JT)

**Implications**:

- Range advantage → Can c-bet frequently with entire range
- Nut advantage → Can use large bet sizes without fear
- Both together → Very aggressive strategy

**Example**: CO raises, BB calls. Flop: 8♥7♠5♠

- **Range advantage**: BB (has more connected cards, suited cards)
- **Nut advantage**: Split (both can have sets, straights)

**Implications**:

- CO should check back frequently despite being preflop aggressor
- BB can donk bet or check-raise effectively
- Smaller bet sizes preferred when betting

### Section 3.2: Continuation Betting (C-betting)

#### C-bet Frequency Formula

#### Minimum c-bet frequency = α = Bet / (Pot + Bet)

To prevent opponent from auto-profiting by always folding.

**But in practice**: Use RANGE advantage and NUT advantage to determine frequency, not just math.

#### C-betting Guidelines

**C-bet HIGH frequency when you have**:

1. Range advantage (more strong hands than villain)
2. Nut advantage (more nuts than villain)
3. Positional advantage (IP)
4. Static board texture (equity won't shift much)

**C-bet LOW frequency when**:

1. Villain has range advantage
2. Dynamic board (many draws)
3. Out of position
4. Multiway pot (more players = someone hit the flop)

#### C-bet Sizing

**Small C-bet** (25-33% pot):

- Polarized range (very strong or bluff)
- Static boards
- When you have nut advantage but not range advantage
- Forces opponent to defend wide range

**Medium C-bet** (50-66% pot):

- Most common sizing
- Balanced range (mix of value and draws)
- Standard range and nut advantage

**Large C-bet** (75-100% pot):

- Polarized range
- Dynamic boards (protect equity)
- When you have strong nut advantage
- When opponent's range is capped (limited strong hands)

**Overbet C-bet** (125-200%+ pot):

- Extreme polarization
- Villain's range is very capped
- Nut advantage is extreme
- Usually IP on specific board textures

### Section 3.3: Defending vs C-bets

#### Your Options

1. **Fold**: Worst hand, no equity, no playability
2. **Call**: Medium hands, draws, hands that improve
3. **Raise**: Strong hands, semi-bluffs, bluffs (with right frequency)

#### Check-Raising Strategy

**Why check-raise?**

- Take initiative away from IP player
- Build pot with strong hands
- Balance with bluffs
- Exploit over-c-betting villains

**Check-raise sizes**:

- **Small** (2-2.5x opponent's bet): More polarized, gets folds from weak hands
- **Large** (3-4x opponent's bet): Very polarized, all-in or fold decision for opponent

**Check-raise value range**:

- Sets, two-pairs (strong made hands)
- Strong top pairs (AK on Axx flop)
- Overpairs on certain textures

**Check-raise bluffs**:

- Flush draws (8-9 outs, can semi-bluff)
- Straight draws (OESD = 8 outs)
- Combo draws (12+ outs, very strong semi-bluff)
- Gutshots + backdoor equity

**Ratio**: Use same bluff:value ratios as c-betting based on your raise size.

If you check-raise to 3x c-bet:

- α for opponent = 3x / (Pot + 3x + c-bet)
- Calculate optimal bluff frequency from this

### Section 3.4: Turn Strategy

#### Turn Categories After Flop C-bet/Call

The turn is critical because:

- Pot is now larger (committed more)
- One fewer card to come (equity more defined)
- Stack-to-pot ratio (SPR) decreases

**Turn cards fall into categories**:

**1. Brick** (changes nothing):

- Example: Flop K♥9♦4♠, Turn 2♣
- Equity distributions stay similar
- Continue with similar strategy to flop

**2. Improves your range**:

- Example: Flop K♥9♦4♠, Turn K♠
- You have more Kx as PFR
- Can barrel again with high frequency

**3. Improves villain's range**:

- Example: Flop K♥9♦4♠, Turn 8♠ (completes flush draw)
- Check back more frequently
- Be cautious with marginal hands

**4. Scare card** (completes obvious draws):

- Example: Flop K♥9♥4♠, Turn J♥
- Even if it doesn't improve opponent, perceived threat is high
- Can bluff more (representing the draw)
- Can give up more (opponent might have hit)

#### Turn Betting Frequencies

After c-betting flop and getting called:

**IP Double Barrel Frequency** (turn bet after flop c-bet):

- Range advantage maintained: **60-70%**
- Neutral: **40-50%**
- Range disadvantage: **20-30%**

**Bet Sizing**:

- Polarized (nuts or bluffs): **75-100% pot**
- Merged (value + draws): **50-66% pot**
- Thin value + protection: **33-50% pot**

### Section 3.5: River Strategy

#### River Dynamics

The river is unique:

- **No more cards** = No draws, only made hands
- **Pot is largest** = Biggest decisions
- **All information revealed** = Entire betting story matters

#### River Betting Ranges

**Polarized Range**: Nuts or bluffs, nothing in between

- When: You've bet flop and turn aggressively
- Why: Medium hands prefer showdown value
- Sizing: Large (75-150%+ pot)
- Example hands: Sets, straights, flushes (value) + missed draws (bluffs)

**Merged/Linear Range**: Spectrum from strong to medium, few bluffs

- When: You've played passively (check/called)
- Why: You have many medium-strength hands
- Sizing: Small to medium (33-66% pot)
- Example hands: Top pair good kicker through second pair

#### River Bluff Frequency

Use same alpha formula:

For **pot-sized bet**: α = 50%, so Bluff:Value = **1:1**
For **2x pot overbet**: α = 67%, so Bluff:Value = **2:1** (need MORE bluffs!)

**Choosing River Bluffs**:

1. **Blockers** to villain's value hands (holding A blocks nut flush)
2. **Missed draws** that make sense with your betting story
3. **Hands with 0% equity** (maximize value of getting folds)
4. **Unblock villain's bluff-catchers** (don't hold the hands they'd fold)

**Example**:

Board: A♥K♠Q♣8♦4♥

You bet flop, turn, now deciding river bluffs for 1.5x pot bet:

Good bluffs:

- J♥T♥ (missed straight + flush draw, blocks JT straight)
- 7♥6♥ (missed flush, story makes sense)
- T♥9♥ (missed draws, represents hearts)

Bad bluffs:

- A♣5♣ (has showdown value, blocks villain's Ax calls)
- K♦J♦ (has showdown value as second pair)

### Section 3.6: Equity Buckets (Advanced Concept)

Modern GTO solvers group hands into **equity buckets** rather than specific combos.

**Bucket System Example**:

- **Bucket 1**: 90-100% equity (nuts)
- **Bucket 2**: 70-90% equity (very strong)
- **Bucket 3**: 50-70% equity (strong)
- **Bucket 4**: 30-50% equity (medium)
- **Bucket 5**: 10-30% equity (weak/draws)
- **Bucket 6**: 0-10% equity (air/weak draws)

**Why use buckets?**

- Simplifies strategy construction
- Focus on equity distribution, not specific hands
- Easier to balance ranges
- Helps visualize range vs range dynamics

**Application**:

When deciding postflop strategy, ask:

1. What % of my range is in each bucket?
2. What % of villain's range is in each bucket?
3. Do I have more nutted hands? (Bucket 1-2)
4. Do I have more total strong hands? (Bucket 1-3)

This guides:

- Bet frequency (more buckets 1-3 = bet more)
- Bet sizing (more bucket 1 = can use larger sizes)
- Balancing (need bucket 5-6 as bluffs to balance bucket 1-2 value)

### Section 3.7: Specific Postflop Situations

#### Single Raised Pot (SRP) - IP vs OOP

**Example**: You raise BN, BB calls. Flop K♥9♦4♠

**Your advantages**:

- Range advantage (more Kx, 9x, overpairs)
- Positional advantage (act last)
- Nut advantage (more KK, 99, 44, AK)

**Strategy**:

- C-bet ~70-80% range (very high frequency)
- Size: 33-50% pot (you're betting so much of range, use smaller size)
- When called, double barrel ~60% on most turn cards
- River: Polarize (bet big with nuts/bluffs, check medium hands)

#### Single Raised Pot - OOP vs IP

**Example**: MP raises, you call BB. Flop Q♣J♥T♠

**Villain's advantages**:

- Nut advantage (more KK, QQ, JJ, TT, AK)
- Positional advantage

**Your advantages**:

- This specific board helps your range (more suited connectors, more 98, more Kx)

**Strategy**:

- Check ~80-90% range (don't lead often)
- Donk bet occasionally with nutted hands (KK, sets) and bluffs
- Check-raise ~8-12% (strong hands + semi-bluffs)
- Check-call ~40-50% (medium hands, draws, bluff-catchers)
- Check-fold ~30-40% (weak hands, no equity)

#### 3-bet Pots

**Example**: CO raises 2.5bb, BN 3-bets 8bb, CO calls. Flop A♠7♦2♣

**BN (3-bettor) advantages**:

- Perceived range advantage (more AA, AK, AQ)
- Initiative (last aggressor)

**Strategy for BN**:

- C-bet ~60-70% range
- Size: 33-50% pot (smaller size, higher frequency)
- When called, slow down significantly (CO calling 3-bet then calling flop = strong range)
- River: Careful with thin value, polarize appropriately

**Strategy for CO**:

- Defend flop with proper MDF (~66% vs 50% pot c-bet)
- Mostly check-call (rarely check-raise in 3-bet pot due to SPR)
- Turn: Continue with strong pairs, overpairs, draws
- River: Become bluff-catcher (opponent has more nutted hands)

### Section 3.8: Stack-to-Pot Ratio (SPR)

#### SPR = Effective Stack / Pot

SPR determines commitment level and strategy.

**Low SPR** (1-3):

- Pot committed with strong hands
- Limited postflop play (often all-in by river)
- Play straightforward (less bluffing)
- Example: 3-bet pot, 100bb effective becomes ~3 SPR

**Medium SPR** (4-8):

- Most postflop skill applies
- Can fold strong hands, bluff effectively
- Multiple streets of action
- Example: Standard single raised pot

**High SPR** (10+):

- Requires nut hands to get stacks in
- Lots of implied odds for speculative hands
- Difficult to build big pots
- Example: Deep stacked cash games, small preflop raise

**Practical Application**:

You have AK, flop A♥8♦3♠, villain calls your c-bet.

**SPR = 2**: Pot = 50bb, Stack = 100bb

- Get it all-in on turn/river with top pair
- Villain's range is capped, you're ahead of most hands

**SPR = 15**: Pot = 20bb, Stack = 300bb

- Be cautious with just top pair
- Need reads/history to commit huge stack
- Consider pot control (check back some streets)

### Section 3.9: Multiway Pots

When 3+ players see the flop:

**Key Differences from Heads-Up**:

1. Someone hit the flop more often
2. Bluffs are less effective (only need one person to call)
3. Value betting should be tighter (need to beat multiple opponents)
4. Speculative hands gain value (implied odds from multiple villains)

**Multiway Strategy**:

- C-bet LESS frequently (~40-50% vs 70%+ HU)
- Value bet THINNER (only bet if you're ahead of all opponents on average)
- Bluff LESS (fold equity divided among opponents)
- Slowplay LESS (too many cards can hurt you)
- Bet SIZE larger (need to protect equity vs more draws)

**Example**: You raise BN with A♠K♠, SB and BB call. Flop K♥9♦4♠

In heads-up: C-bet 75% range, size 50% pot

Multiway: C-bet 50% range, size 66% pot

- Lower frequency (opponent ranges wider, more likely someone hit)
- Larger size (protect vs more draws, need more fold equity per opponent)

---

## DAY 3 Advanced Practice

### Practice Scenario 1: Flop Decision Tree

**Setup**: You open CO with A♥Q♥, BB calls. Flop K♠Q♦6♣ (pot: 9bb, stacks: 90bb)

**Question 1**: Should you c-bet? What size?
**Answer**: Yes, c-bet ~70% time. Size 33-50% pot (you have range advantage on K-high board).

**Question 2**: BB check-raises 3x your c-bet. What hands are in BB's value range? Bluff range?
**Answer**:

- Value: KQ, K6, 66, sometimes KJs, KTs
- Bluffs: Flush draws (QJ♠T♠, J♠T♠), gutshots (JTs, T9s), pair + gutshot (JT)

**Question 3**: Do you call with AQ, 4-bet, or fold?
**Answer**: Mostly call (2nd pair + good kicker has equity vs bluffs, showdown value vs value hands). Folding is too tight, 4-betting turns hand into bluff (worse than just calling).

### Practice Scenario 2: River Bluff Calculation

**Setup**:

- Pot: 100bb
- You've represented strong hand (bet flop + turn)
- River: 8♦ (board: A♣K♥Q♠J♦8♦)
- Your hand: 7♣6♣ (missed club draw)
- Planning to bet 150bb (1.5x pot)

**Question**: If you have 10 value combos (straights, sets), how many bluff combos should you include?

**Answer**:
α = 150 / (100 + 150) = 60%
Bluff:Value = α / (1-α) = 0.6 / 0.4 = 3:2 = 1.5:1

For 10 value combos: 10 × 1.5 = **15 bluff combos**

### Practice Scenario 3: Range Construction

**Setup**: You're in BB facing CO open raise (2.5bb). You decide to 3-bet.

**Question 1**: What size should your 3-bet be?
**Answer**: 9-10bb (about 3.5-4x the original raise)

**Question 2**: Construct a 3-bet value range.
**Answer**: QQ+, AKs, AKo (strongest ~4% hands)

**Question 3**: If you 3-bet 10% total, and 4% is value, how much is bluff? What hands?
**Answer**: 6% bluffs

- Candidates: A5s-A2s (wheel aces, blockers to AA/AK), KQs, KJs (blockers to KK/AK), some suited connectors (T9s, 98s for playability)

---

## Tournament-Specific Concepts

### Independent Chip Model (ICM)

**ICM** calculates the real money value of your chips in a tournament (not 1:1 with chip count).

**Key ICM Principles**:

1. **Chips lose value as you gain more** (diminishing returns)
2. **Preserving stack is critical near bubble**
3. **Big stack can apply pressure** (opponents risk more $EV by calling)

**ICM Pressure Spots**:

- **Bubble** (1 spot from money)
- **Final table bubble**
- **Pay jump** (e.g., 4th to 3rd pays significantly more)

**ICM Example**:

Final 4 players, payouts: 1st=$1000, 2nd=$600, 3rd=$400, 4th=$200

Chip counts:

- P1: 60,000 chips (ICM value: ~$640)
- P2: 40,000 chips (ICM value: ~$520)
- P3: 30,000 chips (ICM value: ~$450)
- P4: 10,000 chips (ICM value: ~$290)

Notice P1 has 6x chips of P4 but only ~2.2x ICM value. Doubling your chips doesn't double your $EV!

**ICM Strategy Adjustments**:

- **Big stack**: Apply pressure on medium stacks (they can't call light)
- **Medium stack**: Avoid big confrontations with other medium stacks
- **Short stack**: Push/fold aggressively (chips more valuable when short)
- **Bubble**: Tighten up vs big stacks, apply pressure on short stacks

### Push/Fold Strategy (10-15bb)

When stacks are 10-15bb, raising becomes risky because:

1. Pot odds for villain to call become favorable
2. You're pot committed after raising if facing a shove
3. Stack sizes don't allow for postflop play

**Solution**: Push/fold strategy (either shove all-in or fold preflop)

**Nash Equilibrium Push/Fold Charts** (SB vs BB, 10bb):

**SB Pushing Range** (~42%):
22+, A2+, K2s+, K7o+, Q5s+, Q9o+, J7s+, JTo, T7s+, T9o, 97s+, 87s, 76s, 65s

**BB Calling Range** (~30%):
77+, A8+, A5s+, KTs+, KJo+, QJs

**Why push wider than opponent calls?**

- Fold equity! SB gains chips from BB folds, making +EV shoves with weak hands

**Application**:

You're SB with 12bb, BN folds, you have K♦7♥

Check chart: K7o is in 42% pushing range → **PUSH**

BB has 15bb and wakes up with Q♠Q♦ → Snap calls (in 30% calling range)

Even though you're crushed, the times BB folds (70% of the time) make the K7o shove profitable!

### Blind vs Blind Dynamics

SB vs BB is the highest frequency battle in tournaments.

**SB Strategy** (deep stacks, 40bb+):

- Raise-first-in: 40-50% of hands
- Size: 2.5-3x BB (larger to compensate for OOP)
- Face 3-bet: Usually fold (OOP makes calling terrible, 4-bet when strong)

**BB Defense** (vs SB 3x raise):

- 3-bet: 8-12% (QQ+, AK, bluffs)
- Call: 40-50% (speculative hands, medium pairs)
- Fold: 38-50%

**Postflop in SB vs BB**:

- Most complex spot in poker (both OOP at different points)
- SB can barrel more (perceived range strength)
- BB can check-raise effectively (SB range is wide)
- Pots often go to showdown (both have medium hands)

---

## Mental Game & Bankroll Management

### Variance and Expected Downswings

**Variance** = Statistical spread of results around your true win rate.

Even winning players face **massive downswings**:

- 10 buy-in downswing: Common
- 20 buy-in downswing: Expected every few thousand tournaments
- 30+ buy-in downswing: Rare but possible

**Managing Variance**:

1. **Proper bankroll** (50-100 buy-ins for tournaments)
2. **Track results** (understand if you're running bad or playing bad)
3. **Review hands** (focus on decisions, not results)
4. **Take breaks** after bad beats
5. **Move down** if bankroll requires it (ego is expensive)

### Bankroll Requirements

**Cash Games**:

- Recreational: 20-30 buy-ins
- Professional: 50-100 buy-ins

**Tournaments**:

- Recreational: 50-100 buy-ins
- Professional: 100-200 buy-ins

**Why more for tournaments?**
Higher variance (only ~15% of field cashes, top-heavy payouts)

### Tilt Control

**Tilt** = Playing emotionally instead of logically

**Common tilt triggers**:

- Bad beats
- Coolers
- Missing draws
- Opponent gets lucky

**Anti-tilt strategies**:

1. **Take breaks** (walk away after tough hands)
2. **Breathing exercises** (calm nervous system)
3. **Session goals** (focus on playing well, not winning)
4. **Stop-loss** (quit if down X buy-ins in session)
5. **Hand review** (prove decision was correct, even if result was bad)

**Remember**:

- You can make perfect decision and lose (variance)
- You can make terrible decision and win (still -EV long-term)
- Focus on process, not results

---

## Quick Reference Charts

### Preflop Opening Ranges (6-max, 100bb)

| Position | Range % | Key Hands |
|----------|---------|-----------|
| UTG | 16% | 22+, A2s+, AJo+, KQo, K9s+, QTs+, JTs, T9s, 98s, 87s, 76s, 65s |
| MP | 22% | Add: A9o+, KJo+, K8s+, Q9s+, J9s+, T8s+, 97s+, 86s+, 75s+, 64s+ |
| CO | 30% | Add: ATo+, K7s+, Q8s+, J8s+, T7s+, 96s+, 85s+, 74s+, 63s+ |
| BN | 48% | Add: Most suited hands, any Ax, many offsuit broadways |
| SB | 35% | Slightly tighter than BN due to OOP postflop |

### MDF and Alpha Quick Reference

| Bet Size | MDF (Defend) | Alpha (Fold Needed) | Bluff:Value |
|----------|--------------|---------------------|-------------|
| 25% pot | 80% | 20% | 1:4 |
| 33% pot | 75% | 25% | 1:3 |
| 50% pot | 67% | 33% | 1:2 |
| 75% pot | 57% | 43% | 3:4 |
| 100% pot | 50% | 50% | 1:1 |
| 150% pot | 40% | 60% | 3:2 |
| 200% pot | 33% | 67% | 2:1 |

### Common Equity Matchups

| Matchup | Favorite | Equity |
|---------|----------|--------|
| AA vs KK | AA | 82% vs 18% |
| AA vs AKo | AA | 87% vs 13% |
| AA vs 22 | AA | 81% vs 19% |
| AKo vs QQ | QQ | 57% vs 43% |
| AKo vs AQo | AK | 70% vs 30% |
| JJ vs AK | JJ | 55% vs 45% |
| Overpair vs underpair | Over | 82% vs 18% |
| Pair vs 2 overcards | Pair | 55% vs 45% |
| Set vs overpair | Set | 91% vs 9% |
| Flush draw | Draw | 35% (to river) |
| OESD | Draw | 32% (to river) |

### SPR and Commitment Guide

| SPR | Strategy |
|-----|----------|
| 0-1 | Always commit with any pair+ |
| 1-3 | Commit with top pair+, sets, overpairs |
| 4-7 | Play multiple streets, can fold strong hands |
| 8-13 | Need very strong hands to commit |
| 13+ | Only commit with nuts or near-nuts |

---

## Common Mistakes to Avoid

### Beginner Mistakes

1. **Playing too many hands from early position**
   - Fix: Stick to opening ranges, fold marginal hands from EP

2. **Calling too much preflop OOP**
   - Fix: 3-bet or fold more, calling OOP is difficult

3. **C-betting 100% range regardless of board**
   - Fix: Check back on boards that favor opponent's range

4. **Chasing draws without pot odds**
   - Fix: Calculate pot odds before calling with draws

5. **Not folding to aggression**
   - Fix: Recognize when opponent's range is strong, fold medium hands

6. **Playing scared money** (too tight due to fear of losing)
   - Fix: Focus on +EV decisions, not protecting chips

7. **Going on tilt after bad beats**
   - Fix: Take breaks, focus on decision quality

### Intermediate Leaks

1. **Not adjusting to opponents**
   - Fix: Identify tight/loose, aggressive/passive opponents and exploit

2. **Betting without a plan**
   - Fix: Know what you're representing, have a story

3. **Ignoring ICM in tournaments**
   - Fix: Tighten up near bubble, avoid marginal spots with medium stack

4. **Misusing blockers**
   - Fix: Understand when blockers matter (river bluffs) vs when they don't (preflop all-ins)

5. **Auto-piloting common spots**
   - Fix: Stay focused, every hand is unique

6. **Poor river bluff selection**
   - Fix: Choose hands with blockers and 0% showdown value

7. **Transparent bet sizing tells**
   - Fix: Use consistent sizing, don't bet small with draws and large with value

---

## Study Plan After This Guide

### Week 1-2: Solidify Fundamentals

- Install equity calculator (Equilab or PokerStove)
- Run 100+ equity calculations until common matchups are memorized
- Practice pot odds calculations in real time
- Play micro-stakes cash games or cheap tournaments ($1-$5)
- Review every session - find 3 mistakes per session

### Week 3-4: Range Work

- Download free range viewer (Flopzilla free trial)
- Input opening ranges for each position
- Practice visualizing ranges on different flops
- Start constructing 3-bet ranges
- Identify leaks: Am I opening too wide? Too tight?

### Month 2: Postflop Mastery

- Study c-betting frequencies on different boards
- Practice check-raise frequencies
- Work on turn decision trees
- Analyze river spots (value or bluff?)
- Record and review postflop mistakes

### Month 3: GTO Study

- Experiment with free GTO solvers (GTO Wizard has free content)
- Compare your plays to GTO solutions
- Understand *why* solvers make certain plays
- Identify spots where you should deviate exploitatively

### Month 4+: Exploitative Play

- Take detailed notes on opponents
- Build HUD (Heads-Up Display) stats if playing online
- Exploit tendencies: 3-bet light vs tight players, value bet thin vs calling stations
- Balance exploitative play with GTO baseline
- Move up stakes gradually as bankroll allows

---

## Recommended Software & Tools

### Free Tools

1. **Equilab** - Equity calculator (essential)
2. **PokerStove** - Alternative equity calculator
3. **GTO Wizard** - Free GTO solver content
4. **ICMizer Free** - Basic push/fold trainer
5. **Hand2Note** - Free HUD for online poker

### Paid Tools (Intermediate/Advanced)

1. **Flopzilla** ($35) - Range analysis
2. **PioSOLVER** ($250+) - Full GTO solver
3. **ICMizer** ($50-100/year) - ICM trainer
4. **PokerTracker 4 / Hold'em Manager** ($60-100) - Database tracking
5. **GTO+ / Simple Postflop** ($100-200) - User-friendly solvers

---

## Final Thoughts

Poker is a game of **incomplete information** and **decision-making under uncertainty**. No single guide will make you an expert - that requires thousands of hours of study and play.

**The Path to Mastery**:

1. **Learn GTO fundamentals** (this guide)
2. **Play volume** (apply concepts in real games)
3. **Review your play** (find leaks constantly)
4. **Study opponents** (exploit their mistakes)
5. **Iterate** (adjust, learn, improve)

**Key Mindsets**:

- **Process over results**: Focus on making +EV decisions
- **Long-term thinking**: Variance is huge in poker; what matters is your edge over thousands of hands
- **Continuous learning**: The game evolves; stay curious
- **Bankroll discipline**: Don't play above your roll (ego is expensive)
- **Emotional control**: Tilt destroys edges faster than anything

**Remember**:

> "Poker is a hard way to make an easy living."

It requires discipline, study, emotional control, and humility. But it rewards those who put in the work with a skill that compounds over a lifetime.

Good luck at the tables!

---

## Glossary

**3-bet**: Re-raise after someone has already raised
**4-bet**: Re-raise after a 3-bet
**Alpha (α)**: Percentage of time opponent must fold for a bluff to break even
**Backdoor draw**: Draw requiring both turn AND river to complete
**Blockers**: Cards in your hand that reduce combinations of opponent hands
**C-bet**: Continuation bet (postflop bet by preflop aggressor)
**Combos**: Specific card combinations (e.g., A♠K♠ is one combo)
**Cooler**: Unavoidable confrontation between two strong hands
**Donk bet**: OOP player bets into preflop aggressor
**EV**: Expected value (average profit/loss over many iterations)
**Equity**: Share of pot based on win probability
**Equity realization**: Fraction of raw equity that materializes into EV
**Flop texture**: Characteristics of flop (wet/dry, static/dynamic)
**Fold equity**: Extra equity from possibility of opponent folding
**GTO**: Game Theory Optimal (unexploitable strategy)
**ICM**: Independent Chip Model (tournament chip value)
**Implied odds**: Expected value from future betting rounds
**MDF**: Minimum Defense Frequency (minimum calling % to prevent auto-profit bluffs)
**Nash Equilibrium**: Strategy where no player can improve EV by deviating unilaterally
**Nut advantage**: Player with more nutted hands in their range
**Outs**: Cards that improve your hand
**Polarized**: Range containing very strong hands and bluffs, no medium hands
**Pot odds**: Ratio of pot size to cost of call
**Range**: All possible hands a player could have
**Range advantage**: Player whose range contains more high-equity hands overall
**RFI**: Raise First In (open-raising when no one has entered pot)
**Semi-bluff**: Betting with a draw that has equity if called
**Showdown value**: Hand strength sufficient to win at showdown
**SPR**: Stack-to-Pot Ratio (remaining stack / pot size)
**Squeeze**: 3-betting after a raise and a call
**Static board**: Board with few draws (equity doesn't change much)
**Tilt**: Playing emotionally instead of logically
**Variance**: Statistical spread of results around true win rate
**VPIP**: Voluntarily Put money In Pot (entering pot by choice, not in blinds)

---

### End of Guide

Total study time: 24-30 hours
Mastery time: 1,000+ hours of play and review

Welcome to the game!
