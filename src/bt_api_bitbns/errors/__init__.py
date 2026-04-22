from __future__ import annotations

from typing import Any

from bt_api_base.error import ErrorCategory, ErrorTranslator, UnifiedError, UnifiedErrorCode


class BitbnsErrorTranslator(ErrorTranslator):
    @classmethod
    def translate(cls, raw_error: dict[str, Any], venue: str) -> UnifiedError | None:
        code = raw_error.get("code", raw_error.get("errorCode"))
        message = str(raw_error.get("message", raw_error.get("error", "")))
        lower = message.lower()

        if code in (0, "0"):
            return None
        if code == 401 or "auth" in lower:
            error_code = UnifiedErrorCode.INVALID_API_KEY
            category = ErrorCategory.AUTH
        elif code == 429 or "rate" in lower or "limit" in lower:
            error_code = UnifiedErrorCode.RATE_LIMIT_EXCEEDED
            category = ErrorCategory.RATE_LIMIT
        elif "balance" in lower or "insufficient" in lower:
            error_code = UnifiedErrorCode.INSUFFICIENT_BALANCE
            category = ErrorCategory.BUSINESS
        elif "not found" in lower or code == 404:
            error_code = UnifiedErrorCode.ORDER_NOT_FOUND
            category = ErrorCategory.BUSINESS
        elif "invalid" in lower or code == 400:
            error_code = UnifiedErrorCode.INVALID_PARAMETER
            category = ErrorCategory.VALIDATION
        else:
            return super().translate(raw_error, venue)

        return UnifiedError(
            code=error_code,
            category=category,
            venue=venue,
            message=message or error_code.name,
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )
