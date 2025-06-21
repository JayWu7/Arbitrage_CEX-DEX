# Delta-Neutral Arbitrage Bots on CEX & DEX

This repository implements two real-time, delta-neutral arbitrage strategies that operate across centralized (CEX) and decentralized (DEX) exchanges.

## 📈 Strategy Overview

### 1. **CEX-DEX Spot Price Arbitrage**

**Objective:**  
Capture price discrepancies between a CEX and a DEX spot market (e.g., Binance and Raydium), executing simultaneous trades on both sides to lock in profit.

**Key Concepts:**
- Monitor spot prices on both CEX and DEX (via WebSocket and gRPC).
- Detect price spread opportunities exceeding fees and slippage.
- Execute buy on the cheaper side and sell on the more expensive side *simultaneously*.
- If both trades succeed → profit realized.
- If one leg fails → hedge or revert the other leg to minimize risk.
- Maintain balanced inventory between CEX and on-chain accounts with periodic rebalancing.

### 2. **Farming APY Arbitrage with Delta-Neutral Hedging**

**Objective:**  
Exploit high-yield DeFi farming opportunities while neutralizing USD-denominated exposure using perpetual futures on CEX.

**Key Concepts:**
- Monitor Onchain USD-based token pairs with active farming programs (e.g., USDC/SOL LP).
- Ensure the token has a perpetual market on a CEX (e.g., SOL-PERP).
- When APY exceeds a predefined threshold:
  - Buy token spot and pair with USD to provide on-chain liquidity.
  - Stake LP tokens into a farming contract to earn yield.
  - Simultaneously short the same token on the CEX to neutralize price exposure.
- Periodically rebalance to ensure LP value ≈ short position, maintaining a **delta-neutral position**.

---

