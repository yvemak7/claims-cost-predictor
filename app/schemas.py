"""
WEEK 7 STARTER (part 1 of 2) — the request and response contract.

Pydantic is doing two jobs here. It stops malformed requests before they reach
the model, and it generates the OpenAPI docs that tell a caller what this
service expects. Both of those are the contract, so get the constraints right.

Fill in every section marked TODO.

Check your work:
    pytest tests/test_api.py -v
"""

from typing import Literal
from pydantic import BaseModel, Field


class MemberFeatures(BaseModel):
    """
    TODO 1 — declare the request body.

    One field per feature your model was trained on. Requirements:

      - age_bucket, sex, region should only accept the values that exist in the
        training data. Anything else is a caller bug and should be rejected with
        a 422, not silently scored. Hint: typing.Literal.
      - the count and amount fields are non-negative integers. A member cannot
        have -3 claims. Hint: Field(ge=0).
      - has_specialty_drug is a bool.
      - the field names must match the column names the model was trained on,
        because main.py turns this object straight into a one-row DataFrame.

    The columns your model expects (run this if you are unsure which ones you
    settled on in Week 4):

        python -c "import joblib; \
          print(list(joblib.load('model.joblib')['preprocessor'].feature_names_in_))"

    Then think about which of these constraints you *cannot* express here, and
    what happens at predict time if a caller violates one — e.g. nothing stops
    them sending medical_claims=5 with total_claims=1.
    """

    # TODO: replace this line with your fields.
    age_bucket: Literal[
        "18-29", "30-39", "40-49",
        "50-59", "60-64"
    ]
    sex: Literal["F", "M"]
    region: Literal["Northeast", "Southeast", "Midwest", "Southwest", "West"]
    total_claims: int = Field(ge=0)
    medical_claims: int = Field(ge=0)
    pharmacy_claims: int = Field(ge=0)
    inpatient_claims: int = Field(ge=0)
    has_specialty_drug: bool
    specialty_drug_fills: int = Field(ge=0)
    unique_diagnosis_codes: int = Field(ge=0)


class PredictionResponse(BaseModel):
    """
    TODO 2 — declare the response body.

    Three fields:
        is_high_cost       bool   the decision
        probability        float  constrained to [0.0, 1.0]
        threshold_dollars  int    which threshold this prediction is relative to

    That third field looks redundant until you deploy a second model trained at
    a different threshold and a caller has a number with no idea what it means.
    """

    # TODO: replace this line with your fields.
    is_high_cost: bool
    probability: float = Field(ge=0.0, le=1.0)
    threshold_dollars: int
