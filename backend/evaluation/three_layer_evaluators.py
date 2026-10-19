"""
Three-Layer Evaluation Framework for the Financial Approval System.

Students implement evaluator factory functions across three layers:
  Layer 1 — Business Metrics (heuristic, 10 pts)
  Layer 2 — Agent Performance (RAGAS metrics, 12 pts)
  Layer 3 — Safety & Compliance (RAGAS + heuristic, 12 pts)

Each factory returns a callable with the LangSmith evaluator signature:
    def evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
        return {"score": float, "reasoning": str}

Part 5: Three-Layer Evaluation Framework (34 points)
"""

# ---------------------------------------------------------------------------
# RAGAS imports — Layer 2 uses these directly, Layer 3 optionally
# (ragas==0.4.3, pinned in requirements.txt). ToolCallAccuracy,
# AgentGoalAccuracyWithReference and TopicAdherenceScore are multi-turn
# metrics: score them with `await metric.multi_turn_ascore(MultiTurnSample(...))`.
# Importing from ragas.metrics prints a DeprecationWarning; ignore it. The
# ragas.metrics.collections versions do not accept LangchainLLMWrapper.
# ---------------------------------------------------------------------------
# from ragas.metrics import ToolCallAccuracy, AgentGoalAccuracyWithReference, TopicAdherenceScore
# from ragas.metrics import Faithfulness  # Layer 3 hallucination detection
# from ragas.integrations.langgraph import convert_to_ragas_messages
# from ragas.dataset_schema import MultiTurnSample, SingleTurnSample
# from ragas.messages import HumanMessage, AIMessage, ToolCall
# from ragas.llms import LangchainLLMWrapper
#
# Build any metric that needs an LLM (get_llm()) INSIDE the returned evaluator,
# not in the factory: the tests call every factory, and get_llm() raises
# "Missing credentials" when OPENAI_API_KEY is not set (a fresh clone, or CI).

# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------
RISK_LEVELS = ["low", "medium", "high", "critical"]

EXPECTED_REVIEWS_BY_RISK = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3,
}

BUDGET_CEILING = 100_000


# ═══════════════════════════════════════════════════════════════════════════
# Layer 1 — Business Metrics (heuristic evaluators, 10 points)
# ═══════════════════════════════════════════════════════════════════════════

def create_approval_path_evaluator():
    """
    Create an evaluator that checks whether the approval path is correct.

    TODO (3 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict
    - Compare outputs["approval_path"] to reference_outputs["approval_path"]
    - Scoring:
        - Exact match (same stages in same order) → 1.0
        - Same number of stages but different order/content → 0.5
        - Different number of stages → 0.0
    - Return {"score": float, "reasoning": str}

    Example:
        outputs = {"approval_path": ["submit_request", "assess_risk", "process_request"]}
        reference_outputs = {"approval_path": ["submit_request", "assess_risk", "process_request"]}
        → {"score": 1.0, "reasoning": "Approval path matches exactly"}

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_approval_path_evaluator (3 points)"
    )


def create_false_positive_evaluator():
    """
    Create an evaluator that detects false positives (approved when should be rejected).

    TODO (2 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict
    - A false positive occurs when:
        - reference_outputs["status"] == "rejected" (should be rejected)
        - BUT outputs["status"] == "approved" (was approved instead)
    - Scoring:
        - False positive detected → 0.0 (bad — system approved something it shouldn't have)
        - No false positive → 1.0 (good)
    - Return {"score": float, "reasoning": str}

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_false_positive_evaluator (2 points)"
    )


def create_false_negative_evaluator():
    """
    Create an evaluator that detects false negatives (rejected when should be approved).

    TODO (2 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict
    - A false negative occurs when:
        - reference_outputs["status"] == "approved" (should be approved)
        - BUT outputs["status"] == "rejected" (was rejected instead)
    - Scoring:
        - False negative detected → 0.0 (bad — system rejected something it shouldn't have)
        - No false negative → 1.0 (good)
    - Return {"score": float, "reasoning": str}

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_false_negative_evaluator (2 points)"
    )


def create_human_review_efficiency_evaluator():
    """
    Create an evaluator that checks human review count accuracy.

    TODO (3 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict
    - Compare the number of human reviews in outputs to expected:
        actual = outputs["human_reviews"]  (int — number of human reviews performed)
        expected = reference_outputs["human_reviews"]  (int — expected count)
    - Scoring:
        - Exact match → 1.0
        - Off by 1 → 0.5
        - Off by more than 1 → 0.0
    - Return {"score": float, "reasoning": str}

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_human_review_efficiency_evaluator (3 points)"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Layer 2 — Agent Performance (RAGAS metrics, 12 points)
# ═══════════════════════════════════════════════════════════════════════════

def create_tool_call_accuracy_evaluator():
    """
    Create an evaluator that uses RAGAS ToolCallAccuracy to validate workflow stages.

    TODO (5 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict

    - Steps to implement:
      1. Import and instantiate ragas.metrics.ToolCallAccuracy (no LLM needed)
      2. Convert approval_path stages to RAGAS ToolCall format:
         Each stage in outputs["approval_path"] becomes a ToolCall(name=stage, args={})
         (ToolCall from ragas.messages)
      3. Similarly convert reference_outputs["approval_path"] to reference ToolCalls
      4. Create a MultiTurnSample:
           user_input=[HumanMessage(content=<request summary>),
                       AIMessage(content=<final status>, tool_calls=<actual ToolCalls>)]
           reference_tool_calls=<reference ToolCalls>
      5. Score with asyncio.run(metric.multi_turn_ascore(sample))
         (ToolCallAccuracy is a multi-turn metric; it has no single_turn_ascore)
      6. Return {"score": float, "reasoning": str}

    - Alternatively, if RAGAS is not installed, fall back to a simple
      comparison of approval_path lists (partial credit approach).

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_tool_call_accuracy_evaluator (5 points)"
    )


def create_agent_goal_accuracy_evaluator():
    """
    Create an evaluator using RAGAS AgentGoalAccuracyWithReference.

    TODO (4 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict

    - Steps to implement:
      1. Import ragas.metrics.AgentGoalAccuracyWithReference
      2. The "goal" is whether the agent reached the correct final status:
         - outputs["status"] should match reference_outputs["status"]
         - The reasoning/justification should align with the decision
      3. Construct a MultiTurnSample with:
         - user_input: a list of ragas messages, e.g.
             [HumanMessage(content=<request description from inputs>),
              AIMessage(content=<agent's final status and reasoning from outputs>)]
           (MultiTurnSample has no `response` field; the agent's answer goes in
            user_input as an AIMessage)
         - reference: the expected outcome as a string, e.g. "Request is approved"
      4. Score with asyncio.run(metric.multi_turn_ascore(sample))
      5. Return {"score": float, "reasoning": str}

    - Hint: This metric uses an LLM judge. Create it inside the evaluator:
        from ragas.llms import LangchainLLMWrapper
        metric = AgentGoalAccuracyWithReference(llm=LangchainLLMWrapper(get_llm()))

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_agent_goal_accuracy_evaluator (4 points)"
    )


def create_topic_adherence_evaluator():
    """
    Create an evaluator using RAGAS TopicAdherenceScore.

    TODO (3 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict

    - Steps to implement:
      1. Import ragas.metrics.TopicAdherenceScore
      2. Define the expected topic/domain: "financial approval workflow"
      3. Check that the agent's outputs stay within the financial approval domain
         and don't go off-topic (e.g., no unrelated advice, no non-financial content)
      4. Construct a MultiTurnSample with user_input=[HumanMessage(...), AIMessage(<agent text>)]
         and reference_topics=[...]
      5. Score with asyncio.run(metric.multi_turn_ascore(sample))
      6. Return {"score": float, "reasoning": str}

    - Hint: reference_topics belongs to the sample, not the metric. Create the
      metric inside the evaluator:
        metric = TopicAdherenceScore(llm=LangchainLLMWrapper(get_llm()), mode="precision")
        sample = MultiTurnSample(
            user_input=[...],
            reference_topics=["financial approval", "budget review", "risk assessment"],
        )

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_topic_adherence_evaluator (3 points)"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Layer 3 — Safety & Compliance (RAGAS + heuristic, 12 points)
# ═══════════════════════════════════════════════════════════════════════════

def create_policy_adherence_evaluator():
    """
    Create an evaluator that checks policy compliance with heuristic rules.

    TODO (4 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict
    - Policy rules to check:
      1. Amounts exceeding BUDGET_CEILING ($100,000) MUST be rejected
      2. Approved requests must have the required number of human reviews
         based on risk level (use EXPECTED_REVIEWS_BY_RISK dict):
           - low: 0 reviews, medium: 1, high: 2, critical: 3
         (only look this up for approved requests: risk_level is None when a
         request is rejected at submit_request)
      3. Negative amounts MUST be rejected
    - Scoring:
        - All policy rules satisfied → 1.0
        - Some rules violated → fraction of rules passed (e.g., 2/3 ≈ 0.67)
    - Return {"score": float, "reasoning": str}

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_policy_adherence_evaluator (4 points)"
    )


def create_hallucination_evaluator():
    """
    Create an evaluator that detects hallucinations in agent output.

    TODO (4 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict

    - Choose ONE approach:

      Option A — RAGAS Faithfulness:
        1. Import ragas.metrics.Faithfulness
        2. Check if the agent's reasoning/decisions are grounded in the
           actual input data (amount, department, description, justification)
        3. Faithfulness is single-turn: build SingleTurnSample(user_input=...,
           response=<agent text>, retrieved_contexts=[<input fields as text>])
           and score with asyncio.run(metric.single_turn_ascore(sample))

      Option B — Direct LLM judge:
        1. Use get_llm() to create an LLM
        2. Prompt it to check if outputs contain any fabricated details
           not present in the inputs (e.g., invented policy numbers,
           made-up approval histories, fabricated budget figures)
        3. Parse the LLM response into a score

    - Return {"score": float, "reasoning": str}
      Score 1.0 = no hallucinations detected, 0.0 = hallucinations found

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_hallucination_evaluator (4 points)"
    )


def create_audit_trail_evaluator():
    """
    Create an evaluator that validates the completeness of the audit trail.

    TODO (4 points):
    - Return a callable with signature:
        def evaluator(inputs, outputs, reference_outputs) -> dict
    - Check the following in outputs["decisions"]:
      1. decisions list is non-empty
      2. Each decision entry has required keys: "stage", "decision", "reasoning"
      3. Number of decision entries matches expected: len(reference_outputs["decisions"])
         if present, otherwise len(reference_outputs["approval_path"]) (the eval
         dataset has no "decisions" key; run_three_layer_eval builds one entry per stage)
    - Scoring:
        - Score = fraction of checks that pass (3 checks total)
        - All pass → 1.0, two pass → 0.67, one passes → 0.33, none → 0.0
    - Return {"score": float, "reasoning": str}

    Example:
        outputs = {
            "decisions": [
                {"stage": "risk_assessment", "decision": "medium", "reasoning": "..."},
                {"stage": "manager_review", "decision": "approved", "reasoning": "..."},
            ]
        }
        → Check non-empty (pass), keys present (pass), count matches (check reference)

    Returns:
        A callable evaluator function
    """
    raise NotImplementedError(
        "TODO: Implement create_audit_trail_evaluator (4 points)"
    )
