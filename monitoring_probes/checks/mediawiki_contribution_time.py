import logging
from datetime import datetime

import aiohttp
from prometheus_client import Gauge

from monitoring_probes.checks import METRIC_PREFIX

logger = logging.getLogger(__name__)

last_user_contribution_time = Gauge(
    f"{METRIC_PREFIX}_last_user_contribution_time",
    "Timestamp of the last contribution",
    ["domain", "username"],
)


async def get_last_user_contribution_time(
    username: str, domain: str = "en.wikipedia.org"
) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{domain}/w/api.php",
            params={
                "action": "query",
                "list": "usercontribs",
                "ucuser": username,
                "uclimit": 1,
                "format": "json",
            },
            headers={"User-Agent": "ClueBot NG Monitoring"},
        ) as r:
            if r.status != 200:
                logger.error(
                    f"Wikipedia API returned non 200 for usercontribs query: {r.status}: {await r.text()}"
                )
                return

            data = await r.json()
            if user_contributions := data.get("query", {}).get("usercontribs", []):
                timestamp = int(
                    datetime.fromisoformat(
                        user_contributions[0]["timestamp"]
                    ).timestamp()
                )
                last_user_contribution_time.labels(
                    domain=domain, username=username
                ).set(timestamp)
