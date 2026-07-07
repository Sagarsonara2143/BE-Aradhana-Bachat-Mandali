from rest_framework.views import exception_handler


def standard_exception_handler(exc, context):
    """Normalise DRF errors into a frontend-friendly envelope.

    The EnvelopeJSONRenderer performs the final wrapping; here we ensure the
    error body carries a helpful top-level message.
    """
    response = exception_handler(exc, context)
    if response is None:
        return None

    detail = response.data
    message = "Validation error"
    if isinstance(detail, dict) and "detail" in detail:
        message = str(detail["detail"])
    elif isinstance(detail, list) and detail:
        message = str(detail[0])

    response.data = {"success": False, "error": detail, "message": message}
    return response
