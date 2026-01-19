# Performance Tests Documentation

## Overview
Performance tests verify that our API responses meet strict time requirements, ensuring the application doesn't degrade as features are added.

## Test Categories

### 1. Account Creation and Deletion Test
**File:** `test_create_and_delete_100_accounts()`

**What it tests:**
- Creates and immediately deletes 100 accounts sequentially
- Each request must complete within **0.5 seconds**
- Validates proper HTTP status codes (201 for creation, 200 for deletion)

**Key Metrics:**
- 100 iterations
- Max response time per request: 0.5s
- Tests individual operation performance

**Why this pattern:**
- Simulates real-world user behavior (create account, then cancel)
- Tests if operations remain fast when performed one after another

### 2. Incoming Transfers Performance Test
**File:** `test_create_account_and_100_incoming_transfers()`

**What it tests:**
- Creates one account
- Executes 100 incoming transfers on that account
- Each transfer request must complete within **0.5 seconds**
- Validates final balance correctness

**Key Metrics:**
- Initial balance: 50.0 (promo bonus)
- 100 transfers × 10.0 = 1000.0
- Expected final balance: 1050.0
- Tests data correctness under load

**Why this pattern:**
- Simulates account activity with many transactions
- Verifies system stability with growing transaction history
- Tests if the history list management affects performance

### 3. Bulk Account Creation Test (1000 accounts)
**File:** `test_create_1000_accounts_then_delete()`

**What it tests:**
- **Phase 1:** Creates 1000 accounts (max 0.5s per request)
- **Phase 2:** Deletes all 1000 accounts (max 0.5s per request)
- All operations must meet the 0.5s response time requirement

**Key Metrics:**
- 2000 total requests (1000 creates + 1000 deletes)
- Registry grows from 0 to 1000 accounts then shrinks
- Tests algorithmic complexity

**Why this pattern is different from test 1:**
- **Test 1 (create-delete pairs):** Tests if individual operations stay fast
- **Test 3 (bulk then delete):** Tests if performance degrades as data structures grow
- Key insight: Does searching/finding an account in a list of 1000 take significantly longer than in a list of 10?

## Performance Insights

### What can impact application speed?

1. **Data Structure Complexity**
   - Lists vs. dictionaries for lookups
   - O(n) searches become noticeable at scale

2. **Database Operations** (hypothetically)
   - Query optimization
   - Index usage
   - Connection pooling

3. **API Framework Overhead**
   - Flask request/response handling
   - JSON serialization/deserialization

4. **Business Logic**
   - Account validation rules
   - Transfer calculations
   - History tracking

5. **System Resources**
   - Memory usage
   - CPU cache efficiency
   - Garbage collection

### Why single-threaded testing might miss real problems

1. **Race Conditions:** Real systems have concurrent requests that our sequential tests don't test
2. **Resource Contention:** Multiple threads competing for locks
3. **Memory Pressure:** Accumulated allocations causing GC pauses
4. **Cache Behavior:** Real-world patterns differ from sequential access
5. **Network Latency:** Simulated locally but would add variance in production

### Advanced Tools

For more comprehensive performance testing:
- **Locust:** Python-based load testing (supports thousands of concurrent users)
- **k6:** JavaScript-based performance testing with sophisticated reporting
- **Apache JMeter:** Enterprise-grade load testing tool
- **Grafana:** For monitoring and visualization

## Running the Tests

### Local Execution
```bash
# Terminal 1: Start Flask
export FLASK_APP=src/api.py
flask run

# Terminal 2: Run performance tests
python -m pytest tests/perf/ -v
```

### GitHub Actions
The performance tests run automatically on every push and pull request via the `performance-tests.yml` workflow.

## Expected Performance

All tests should pass with response times well under the 0.5s threshold on modern hardware. If tests fail:

1. **Check system load** - High CPU/memory usage could slow responses
2. **Review database operations** - If added in future
3. **Profile the code** - Use `cProfile` to find bottlenecks
4. **Check for memory leaks** - Growing memory usage over time
