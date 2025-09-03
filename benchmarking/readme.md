## Performance of AI Models on Project Euler Problems

| Difficulty | Claude Opus 4.1                                       | ChatGPT 5 Pro                                                        | Gemini 2.5 Pro                                                        |
|------------|-------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|
| **5%**     | ❌ Failed to compile on both tries (3 min + 15s)       | ✅ Succeeded on first try, compiled instantly (8 mins)                | ⚠️ Succeeded on second try, ran in ~2 mins (<2 mins)                    |
| **10%**    | ✅ Succeeded on first try, compiled instantly (4 mins) | ✅ Succeeded on first try, compiled instantly (4 mins)                | ✅ Succeeded on first try, compiled instantly (~2 mins)                |
| **20%**    | ❌ Wrong answers on both attempts (9 + 1 mins)         | ✅ Succeeded on first try, compiled instantly (12 mins)               | ✅ Succeeded on first try, compiled instantly (~3 mins)                |
| **30%**    | ❌ Wrong answers on both attempts (5 min + 30 s)       | ✅ Succeeded on first try, ran for ~10s (13 mins)                     | ✅ Succeeded on first try, ran for ~10s (~3 mins)                      |
| **40%**    | ❌ Eliminated                                          | ✅ Succeeded on first try, compiled instantly (12 mins)               | ❌ Failed both attempts, produced fabricated output (time not reported) |
| **50%**    | ❌ Eliminated                                          | ✅ Succeeded on first try, compiled instantly (time not reported)     | ❌ Wrong answers on both attempts (time not reported)                  |
| **60%**    | ❌ Eliminated                                          | ✅ Succeeded on first try, compiled instantly  (14 mins)              | ❌ Eliminated                                                          |
| **70%**    | ❌ Eliminated                                          | ⚠️ Memory error first, then compiled instantly (25 + 11 mins)        | ❌ Eliminated                                                          |
| **80%**    | ❌ Eliminated                                          | ✅ Succeeded on first try, ran briefly (25 mins)                      | ❌ Eliminated                                                          |
| **90%**    | ❌ Eliminated                                          | ❌ Partial solution for both attempts (20 + 16 mins)                  | ❌ Eliminated                                                          |
| **100%**   | ❌ Eliminated                                          | ⚠️ First attempt wrong, second attempt correct (~15–20 mins per try) | ❌ Eliminated                                                          |

---

### Legend
- ✅ **Succeeded** = Correct solution and code ran successfully  
- ❌ **Eliminated** = Both attempts failed
- ⚠️ **Partial/Mixed** = First attempt failed
- **Thinking time (in parantheses)** = How long the model spent “working” before producing the solution  
