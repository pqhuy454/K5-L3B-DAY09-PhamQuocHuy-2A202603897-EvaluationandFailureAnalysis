"""Regression test for the M1 trace case (C-002@11 FM-03 ticket_trust)."""

from __future__ import annotations

import pytest

from lab9.trace_case import investigate


@pytest.mark.student
def test_c002_ticket_trust_regression():
    fixed = investigate("fixed", "C-002", 11)["trial"]
    assert fixed["lab8_pass"], fixed["lab8_reason"]
    assert [e for e in fixed["events"] if e.get("kind") == "model_override"] == []

    reg = investigate("seeded_regression", "C-002", 11)["trial"]
    assert not reg["lab8_pass"]
    overrides = [e for e in reg["events"] if e.get("kind") == "model_override"]
    assert len(overrides) == 1
