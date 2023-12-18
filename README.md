# JPMorgan Chase & Co: S&P 500 Index Replication

### Goal: Our goal is to create an portfolio that replicates the performance of the S&P 500 using Natural Language Constraints and Optimization techniques.

### S&P 500
- The S&P500 is a stock market index tracking the performance of 500 large companies listed on exchanges in the United States
- One of the most followed indices. 
- Often used as a reference benchmark.

### We would like to create a portfolio to replicate the  the S&P 500 performance  with:
1. Less companies -> Cost reduction
2. Arbitrary constraints -> User preferences

### Desired Output:

<img width="668" alt="Screenshot 2023-11-20 at 12 52 52 PM" src="https://github.com/arianab68/JPMC-Index-Replication/assets/70418227/dce20e82-8753-4650-ada3-4c57f1f834e9">

### Natural Language Processing 

The goal of the NLP portion is to extract 3 constraints out of a sentence:
1. Number Constraint (3)
2. Mathematical Constraint (<=, >=, >, <, =)
3. Sector Constraint (Technology, Energy, etc.)

Example Inputs:
“I want to invest in at least 3 tech companies”  <- 3 (number); >= (mathematical); tech (sector)

### Optimization

### Purpose: Understanding our clients needs by taking their numerical and sector constraints from our NLP side, and using them to return the most optimal portfolio (most similarity to S&P500 and best returns)
### Example: 

1. Portfolio 1 - (Apple, Tesla, Microsoft) → 70% similar to S&P500 | 50% return
2. Portfolio 2 - (Google, Palantir, Meta) → 60% similar to S&P500 | 30% return

### General Steps For Optimization:
1. Compute log returns of daily stock price
2. Create a correlation matrix of the log returns of each stock
3. Feed correlation matrix into K-Means algorithm to give us the best stocks 
4. Creating a portfolio of stocks given market cap weighting 

### Demo

https://github.com/arianab68/JPMC-Index-Replication/assets/70418227/6b1a8b8a-aab9-41a5-b79e-f0e96b9ac9de






