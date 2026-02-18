# /solve — Start a New Problem

## Arguments
$ARGUMENTS: <slug-or-url-or-description> [lang]

- First argument: One of three formats:
  1. **LeetCode slug** (e.g. `two-sum`) — looks up in `problems.json`, fetches from LeetCode
  2. **LeetCode URL** (e.g. `https://leetcode.com/problems/valid-parentheses/`) — works for ANY problem
  3. **Inline description** — user pastes a problem description directly
- Second argument (optional): Language — `cpp`, `python`, or `java`. Defaults to `cpp`.

## Instructions

1. **Determine input mode:**
   - If argument looks like a URL (`https://`), extract the slug from it.
   - If argument looks like a slug (lowercase-with-dashes), use it directly.
   - If neither, treat as an inline problem description — skip fetching, use the description as-is.

2. **Look up metadata** from `problems.json` (if slug matches a problem in any track). Get topic, difficulty, LC number.

3. **Fetch the problem description** from `https://leetcode.com/problems/<slug>/` using web fetch. If blocked, try `https://algo.monster/liteproblems/<number>` as fallback. Skip this step for inline descriptions.

4. **Scaffold the problem:**
   ```bash
   grind new <slug> <lang>
   ```

5. **CRITICAL — Edit the solution file** to match the actual problem:
   - Read the scaffolded solution file from `problems/<slug_underscored>/solution.<ext>`
   - Replace the `TODO` placeholder in the `Solution` class with the **exact method signature** from LeetCode (function name, parameter types, return type). Leave the body as a TODO comment or `pass`/`return default`.
   - Replace the `TODO` test cases in `main` with **one working example** from the problem, calling the Solution method with the example input and printing the result.
   - Do NOT write any solution logic — only the signature and test harness.

6. **Write a README.md** in the problem folder (`problems/<slug_underscored>/README.md`) containing:
   - Problem title and difficulty
   - Problem description (cleaned up from the web fetch)
   - Example inputs/outputs
   - Constraints

7. **Check `memory.md`** — has the user attempted this problem before? If so, mention it.

8. **Present the problem** per `coach_persona.md`:
   - Show the problem statement, constraints, and one example clearly
   - Optionally ask: "Any questions about the problem?"
   - **Say nothing else.** No leading questions, no hints about approach or technique. Wait for the user to speak first.

## Example
```
/solve two-sum cpp
/solve https://leetcode.com/problems/binary-watch/ python
/solve <user pastes problem description>
```

Expected result in `solution.cpp`:
```cpp
#include "../../utils/cpp/lc_utils.h"

// Problem: binary-watch
// URL: https://leetcode.com/problems/binary-watch/

class Solution {
public:
    vector<string> readBinaryWatch(int turnedOn) {
        // TODO: Implement solution
        return {};
    }
};

int main() {
    ios::sync_with_stdio(0); cin.tie(0);

    Solution sol;
    cout << sol.readBinaryWatch(1) << endl;

    return 0;
}
```
