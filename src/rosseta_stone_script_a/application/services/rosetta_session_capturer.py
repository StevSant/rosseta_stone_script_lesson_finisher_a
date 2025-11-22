import re
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

from rosseta_stone_script_a.shared.mixins.loggin_mixin import LoggingMixin


class RosettaSessionCapturer(LoggingMixin):
    """Service to capture Rosetta Stone session data from network traffic."""

    def __init__(self):
        self.captured_data = {
            "authorization": None,
            "school_id": None,
            "user_id": None,
            "lang_code": None,
            "session_token": None,
        }

    async def handle_request(self, request: Any) -> None:
        """Callback to handle network requests and extract data."""
        try:
            url = request.url
            headers = request.headers

            # 1. Capture header "authorization" from GraphQL
            if "authorization" in headers:
                auth_value = headers["authorization"]
                # Ensure we capture the long JWT-like token (starts with eyJ), not the UUID Bearer token
                if auth_value.startswith("eyJ") and not self.captured_data[
                    "authorization"
                ]:
                    self.captured_data["authorization"] = auth_value

            # 2. Capture data from /recommended_course
            if "/recommended_course" in url:
                # Extract school_id and user_id
                match = re.search(
                    r"/ee/ce/([^/]+)/users/([^/]+)/recommended_course", url
                )
                if match:
                    self.captured_data["school_id"] = match.group(1)
                    self.captured_data["user_id"] = match.group(2)

                # Extract lang_code
                parsed = urlparse(url)
                qs = parse_qs(parsed.query)
                if "product_identifier" in qs:
                    self.captured_data["lang_code"] = qs["product_identifier"][0]

                # Extract session token
                if "x-rosettastone-session-token" in headers:
                    self.captured_data["session_token"] = headers[
                        "x-rosettastone-session-token"
                    ]
        except Exception as e:
            self.logger.error(f"Error in request interceptor: {e}")

    def get_captured_data(self) -> Dict[str, Optional[str]]:
        """Return the captured session data."""
        return self.captured_data
