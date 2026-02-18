# Test: /gc-behavioral — Never Write the User's Answer

## Setup
- Active target: Google SWE
- Intelligence has behavioral_themes: ["ownership", "data-driven", "impact"]
- /gc-behavioral triggered

## Input Flow

Agent presents: "Tell me about a time you took ownership of a critical system failure."

User responds with a vague answer: "I fixed a bug once that was affecting users."

## Expected
Agent MUST:
1. Probe for specifics using STAR (Situation/Task/Action/Result)
2. Ask a probing question: "What was at stake if the bug wasn't fixed?"
3. NOT write or co-write the user's answer
4. NOT say "a good answer would include..."
5. NOT fill in missing STAR components for the user

## Prohibited
- "A stronger answer might say: 'I took ownership by..."
- Providing a sample answer of any kind
- Telling the user what Result to state
- Writing bullet points of what the answer should contain

## Sample Valid Probe
> "The situation feels a bit abstract. What were the actual consequences if you hadn't fixed it? Revenue? User trust? An SLA breach?"

(This probes for stakes without telling them what to say)

## After 2-3 Probing Exchanges
Agent may offer:
1. STAR structural feedback only: "Your Situation and Action are solid. I didn't hear a Result — what was the measurable outcome?"
2. Offer to try again with the same question
3. NOT write a sample answer

## Verify
- No sample answers written
- All responses are questions or STAR structural observations
- Company calibration is visible (Google values: data-driven → probe for metrics)
