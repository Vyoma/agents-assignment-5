"""
LLM-based evaluation dataset generator for the Financial Approval System.

Students implement functions to:
1. Generate diverse test cases using an LLM
2. Generate edge/adversarial cases
3. Upload datasets to LangSmith
4. Validate generated datasets

Part 5: Dataset Generation (16 points)
"""

import json

# ---------------------------------------------------------------------------
# Constants (GIVEN — do not modify)
# ---------------------------------------------------------------------------

VALID_DEPARTMENTS = ["engineering", "marketing", "operations", "research", "hr"]

BUDGET_CEILING = 100_000

DEPARTMENT_BUDGETS = {
    "engineering": 50000,
    "marketing": 30000,
    "operations": 40000,
    "research": 60000,
    "hr": 5000,
}

DATASET_SCHEMA = {
    "input": {
        "request_id": "str — unique identifier (e.g., 'GEN-001')",
        "title": "str — short description of the purchase",
        "description": "str — detailed description",
        "amount": "float — dollar amount (can be negative for edge cases)",
        "department": "str — one of VALID_DEPARTMENTS",
        "requester": "str — person making the request",
        "justification": "str — business justification",
        "priority": "str — one of: low, normal, high, urgent",
    },
    "expected": {
        "risk_level": "str — one of: low, medium, high, critical",
        "status": "str — one of: approved, rejected",
        "approval_path": "list[str] — ordered list of workflow stages",
        "human_reviews": "int — number of human review interrupts expected",
    },
}

GENERATION_PROMPT = """You are a test case generator for a Financial Approval System.

Generate {num_cases} diverse test cases for evaluating the system. Each test case
should be a JSON object with "input" and "expected" fields.

Business Rules:
- Amounts <= $10,000: low risk, auto-approved (0 human reviews)
  Path: submit_request → assess_risk → validate_budget → process_request
- Amounts $10,001-$50,000: medium risk, needs manager review (1 human review)
  Path: submit_request → assess_risk → manager_review → validate_budget → process_request
- Amounts $50,001-$100,000: high risk, needs manager + finance review (2 human reviews)
  Path: submit_request → assess_risk → manager_review → finance_review → process_request
- Amounts > $100,000: rejected (exceeds budget ceiling)
  Path: submit_request → handle_rejection
- Negative amounts: rejected (invalid)
  Path: submit_request → handle_rejection
- Priority "urgent" + amount > $50,000: critical risk, needs 3 reviews
  Path: submit_request → assess_risk → manager_review → finance_review → final_signoff → process_request
- Department budgets: engineering $50,000, marketing $30,000, operations $40,000,
  research $60,000, hr $5,000. validate_budget escalates when the amount is over budget:
  - Low risk over budget: manager review (1 human review)
    Path: submit_request → assess_risk → validate_budget → manager_review → process_request
  - Medium risk over budget: finance review after the budget check (2 human reviews)
    Path: submit_request → assess_risk → manager_review → validate_budget → finance_review → process_request

Valid departments: {departments}
Valid priorities: low, normal, high, urgent

Generate realistic financial requests covering different departments, amounts,
and risk levels. Include a mix of approved and rejected cases.

Return ONLY a JSON array of test case objects. No markdown, no explanation.
"""

EDGE_CASE_PROMPT = """You are a test case generator for a Financial Approval System.
Generate {num_cases} EDGE CASES and ADVERSARIAL scenarios.

Focus on boundary conditions and tricky scenarios:
1. Amounts exactly at thresholds ($10,000, $50,000, $100,000)
2. Negative amounts or zero amounts
3. Very large amounts (> $1,000,000)
4. Unusual descriptions that might confuse the system
5. Requests that test policy boundaries

Business Rules:
- Amounts <= $10,000: low risk, auto-approved
- Amounts $10,001-$50,000: medium risk, manager review
- Amounts $50,001-$100,000: high risk, manager + finance review
- Amounts > $100,000: REJECTED (exceeds ceiling)
- Negative amounts: REJECTED
- Priority "urgent" + amount > $50,000: critical risk, 3 reviews
- Over the department budget (engineering $50,000, marketing $30,000, operations $40,000,
  research $60,000, hr $5,000): low risk adds a manager review (1 review), medium risk
  adds a finance review after the budget check (2 reviews)

Valid departments: {departments}

Return ONLY a JSON array of test case objects. No markdown, no explanation.
"""


# ═══════════════════════════════════════════════════════════════════════════
# Student TODO — Dataset Generation Functions (16 points)
# ═══════════════════════════════════════════════════════════════════════════

def generate_eval_dataset(num_cases=10, llm=None):
    """
    Generate diverse evaluation test cases using an LLM.

    TODO (4 points):
    - If llm is None, create one using: from backend.config import get_llm
    - Format GENERATION_PROMPT with num_cases and VALID_DEPARTMENTS
    - Invoke the LLM with the formatted prompt
    - Parse the JSON response into a list of dicts
    - Each dict must match DATASET_SCHEMA structure
    - Return the list of generated test cases

    Args:
        num_cases: Number of test cases to generate (default 10)
        llm: Optional LangChain LLM instance (if None, use get_llm())

    Returns:
        list[dict]: Generated test cases matching DATASET_SCHEMA

    Example:
        dataset = generate_eval_dataset(num_cases=5)
        # Returns: [{"input": {...}, "expected": {...}}, ...]
    """
    raise NotImplementedError(
        "TODO: Implement generate_eval_dataset (4 points)"
    )


def generate_edge_cases(num_cases=5, llm=None):
    """
    Generate boundary and adversarial test cases using an LLM.

    TODO (4 points):
    - If llm is None, create one using: from backend.config import get_llm
    - Format EDGE_CASE_PROMPT with num_cases and VALID_DEPARTMENTS
    - Invoke the LLM with the formatted prompt
    - Parse the JSON response into a list of dicts
    - Focus on boundary conditions (exact thresholds, negatives, etc.)
    - Return the list of generated edge cases

    Args:
        num_cases: Number of edge cases to generate (default 5)
        llm: Optional LangChain LLM instance (if None, use get_llm())

    Returns:
        list[dict]: Generated edge cases matching DATASET_SCHEMA
    """
    raise NotImplementedError(
        "TODO: Implement generate_edge_cases (4 points)"
    )


def upload_to_langsmith(dataset, dataset_name="financial-approval-eval"):
    """
    Upload a dataset to LangSmith for evaluation runs.

    TODO (4 points):
    - Import langsmith and create a Client: client = langsmith.Client()
    - Create a new dataset: ls_dataset = client.create_dataset(dataset_name=dataset_name)
      (use a new name; the `dataset` argument is your list of test cases)
    - For each test case in the dataset, create an example:
        client.create_example(
            inputs=case["input"],
            outputs=case["expected"],
            dataset_id=ls_dataset.id,
        )
    - Return the dataset ID as a string

    Args:
        dataset: list[dict] — test cases with "input" and "expected" keys
        dataset_name: str — name for the LangSmith dataset

    Returns:
        str: The LangSmith dataset ID

    Raises:
        ValueError: If dataset is empty
    """
    raise NotImplementedError(
        "TODO: Implement upload_to_langsmith (4 points)"
    )


def validate_generated_dataset(dataset):
    """
    Validate that a generated dataset conforms to the expected schema.

    TODO (4 points):
    - Check the following and collect error messages for failures:
      1. dataset is a non-empty list
      2. Each entry has "input" and "expected" top-level keys
      3. Each input has required fields: request_id, title, description,
         amount, department, requester, justification, priority
      4. Each expected has required fields: risk_level, status,
         approval_path, human_reviews
      5. amount is a number (int or float)
      6. department is in VALID_DEPARTMENTS
      7. risk_level is one of: low, medium, high, critical
      8. status is one of: approved, rejected
      9. approval_path is a list
      10. human_reviews is an int >= 0
    - Return a tuple: (is_valid: bool, errors: list[str])
      - is_valid is True if no errors found
      - errors is a list of descriptive error strings

    Args:
        dataset: list[dict] — the dataset to validate

    Returns:
        tuple[bool, list[str]]: (is_valid, error_messages)

    Example:
        valid, errors = validate_generated_dataset([{"input": {}, "expected": {}}])
        # valid = False, errors = ["Case 1: input missing 'request_id'", ...]
    """
    raise NotImplementedError(
        "TODO: Implement validate_generated_dataset (4 points)"
    )
