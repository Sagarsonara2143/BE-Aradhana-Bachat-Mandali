from rest_framework.renderers import JSONRenderer


class EnvelopeJSONRenderer(JSONRenderer):
    """Wrap all responses in a consistent { success, data/error, message } shape."""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")
        status_code = getattr(response, "status_code", 200)

        # Already enveloped (e.g. re-rendered) — pass through.
        if isinstance(data, dict) and "success" in data and (
            "data" in data or "error" in data
        ):
            payload = data
        elif status_code >= 400:
            message = "Request failed"
            if isinstance(data, dict):
                message = str(data.get("detail", message))
            payload = {"success": False, "error": data, "message": message}
        else:
            payload = {"success": True, "data": data, "message": "Success"}

        return super().render(payload, accepted_media_type, renderer_context)
