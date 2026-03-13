"""
Marketing platform integration stubs.
Replace stub implementations with real API calls for your stack.

Supported platforms (configure via .env):
  - HubSpot (CRM, email, landing pages)
  - Mailchimp / Klaviyo (email)
  - Buffer / Hootsuite (social scheduling)
  - Google Analytics 4 (web analytics)
  - Semrush / Ahrefs (SEO data)
  - Meta Ads / Google Ads (paid)
"""

import os
from typing import Any


# ──────────────────────────────────────────────
# HubSpot
# ──────────────────────────────────────────────

def create_hubspot_email_campaign(
    name: str,
    subject: str,
    body_html: str,
    contact_list_id: str,
) -> dict[str, Any]:
    """Create a draft email campaign in HubSpot."""
    api_key = os.getenv("HUBSPOT_API_KEY")
    if not api_key:
        return {"status": "stub", "message": "Set HUBSPOT_API_KEY in .env to activate"}

    # Real implementation:
    # import hubspot
    # client = hubspot.Client.create(access_token=api_key)
    # return client.marketing.emails.create(...)
    return {"status": "stub", "platform": "hubspot", "campaign": name}


def get_hubspot_contact_count(list_id: str) -> dict[str, Any]:
    """Get contact count for a HubSpot list."""
    api_key = os.getenv("HUBSPOT_API_KEY")
    if not api_key:
        return {"status": "stub", "count": 0, "message": "Set HUBSPOT_API_KEY in .env"}
    return {"status": "stub", "list_id": list_id, "count": 0}


# ──────────────────────────────────────────────
# Email Platforms (Mailchimp / Klaviyo)
# ──────────────────────────────────────────────

def schedule_email(
    platform: str,  # "mailchimp" | "klaviyo"
    subject: str,
    body: str,
    audience_id: str,
    send_time: str,  # ISO 8601
) -> dict[str, Any]:
    """Schedule an email campaign."""
    key = os.getenv(f"{platform.upper()}_API_KEY")
    if not key:
        return {"status": "stub", "message": f"Set {platform.upper()}_API_KEY in .env"}
    return {"status": "stub", "platform": platform, "subject": subject, "scheduled": send_time}


# ──────────────────────────────────────────────
# Social Scheduling (Buffer)
# ──────────────────────────────────────────────

def schedule_social_post(
    platform: str,  # "linkedin" | "twitter" | "instagram" | "facebook"
    content: str,
    scheduled_time: str,
    profile_id: str | None = None,
) -> dict[str, Any]:
    """Schedule a social post via Buffer."""
    api_key = os.getenv("BUFFER_API_KEY")
    if not api_key:
        return {"status": "stub", "message": "Set BUFFER_API_KEY in .env to schedule posts"}
    return {
        "status": "stub",
        "platform": platform,
        "content_preview": content[:80] + "...",
        "scheduled": scheduled_time,
    }


# ──────────────────────────────────────────────
# SEO Data (Semrush)
# ──────────────────────────────────────────────

def get_keyword_data(keyword: str, country: str = "us") -> dict[str, Any]:
    """Fetch keyword volume and difficulty from Semrush."""
    api_key = os.getenv("SEMRUSH_API_KEY")
    if not api_key:
        return {
            "status": "stub",
            "keyword": keyword,
            "message": "Set SEMRUSH_API_KEY in .env for real data",
            "mock_data": {
                "volume": "1,000 - 10,000/mo",
                "difficulty": "medium (45/100)",
                "cpc": "$2.50",
            },
        }
    return {"status": "stub", "keyword": keyword}


# ──────────────────────────────────────────────
# Analytics (Google Analytics 4)
# ──────────────────────────────────────────────

def get_ga4_report(
    property_id: str,
    metrics: list[str],
    date_range: tuple[str, str],
) -> dict[str, Any]:
    """Fetch a GA4 report."""
    credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials:
        return {
            "status": "stub",
            "message": "Set GOOGLE_APPLICATION_CREDENTIALS in .env",
            "mock_data": {
                "sessions": 12_450,
                "bounce_rate": "42%",
                "avg_session_duration": "2m 34s",
                "conversions": 187,
            },
        }
    return {"status": "stub", "property_id": property_id}
