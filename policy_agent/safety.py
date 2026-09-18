"""Input and output safety rules for the policy assistant."""

import re


class SafetyGuard:
    """Reject prompt-injection and sensitive-data requests before model use."""

    _prompt_injection = re.compile(
        r"\b(ignore|disregard|override|bypass)\b.{0,80}\b(instruction|system|prompt|rule)s?\b"
        r"|\b(reveal|show|print|repeat)\b.{0,50}\b(system prompt|developer message|hidden instruction)s?\b"
        r"|\b(jailbreak|prompt injection)\b",
        re.IGNORECASE,
    )
    _sensitive_data = re.compile(
        r"\b(full|complete|entire)\s+(id|identification|social security|account)\s+number\b"
        r"|\b(pin|password|passcode|one[- ]time password|otp)\b"
        r"|\b(send|share|tell|give|provide)\b.{0,40}\b(secret|credential|security code)\b",
        re.IGNORECASE,
    )
    _live_account_data = re.compile(
        r"\b(current|live|actual|real[- ]time)\b.{0,30}\b(balance|transactions?|account status)\b"
        r"|\b(balance|transactions?|account status)\b.{0,30}\b(current|live|actual|real[- ]time)\b",
        re.IGNORECASE,
    )

    @classmethod
    def refusal_for(cls, question: str) -> str | None:
        if cls._prompt_injection.search(question):
            return "I can only answer questions using the provided policy documents. Source: none."
        if cls._sensitive_data.search(question):
            return "I cannot request, handle, or retain passwords, PINs, OTPs, or full identification numbers. Source: none."
        if cls._live_account_data.search(question):
            return "That information is not covered by the provided policy documents. Source: none."
        return None


def refusal_for(question: str) -> str | None:
    """Compatibility function for callers that used the original script."""

    return SafetyGuard.refusal_for(question)