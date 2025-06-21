import asyncio

# Monitor all on-chain USD-paired tokens with farming rewards
async def monitor_onchain_apy(threshold_apy):
    while True:
        pairs = await get_all_usd_pairs_onchain()
        for pair in pairs:
            apy = await get_pair_apy(pair)
            # Only proceed if APY exceeds threshold and CEX has a perpetual for the token
            if apy > threshold_apy and has_cex_perp(pair.token):
                await execute_lp_farming_strategy(pair, apy)
        await asyncio.sleep(30)  # Refresh every 30 seconds

# Check if the token has a perpetual contract on the CEX
def has_cex_perp(token_symbol):
    return token_symbol in get_cex_perp_symbols()

# Execute delta-neutral LP farming: long spot + farm + short perp
async def execute_lp_farming_strategy(pair, apy):
    price = await get_token_price(pair.token)
    size = calc_entry_size(pair, apy, price)
    
    # Buy spot token and provide liquidity with USD
    await buy_token_onchain(pair.token, size)
    await add_liquidity_to_pool(pair.token, size, size * price)
    await stake_lp_for_farming(pair.pool)

    # Hedge the position by shorting the token on CEX
    await short_token_on_cex(pair.token, size)

    log_entry(pair.token, size, apy)

# Periodically rebalance position to keep USD-neutral exposure
async def rebalance_position(interval=60):
    while True:
        for token in get_current_lp_tokens():
            lp_value = await get_lp_market_value(token)
            short_value = await get_cex_short_value(token)

            diff = lp_value - short_value
            # If the value difference exceeds threshold, rebalance the hedge
            if abs(diff) > rebalance_threshold:
                if diff > 0:
                    # LP value > short value → increase short
                    await short_token_on_cex(token, diff / get_token_price(token))
                else:
                    # LP value < short value → reduce short
                    await reduce_cex_short(token, -diff / get_token_price(token))
        await asyncio.sleep(interval)

# Main entry point: run monitoring and rebalancing concurrently
async def main():
    await asyncio.gather(
        monitor_onchain_apy(threshold_apy=0.20),  # e.g., only act on APY > 20%
        rebalance_position(interval=60)           # rebalance every 60 seconds
    )

# Start the async event loop
asyncio.run(main())
