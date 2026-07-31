"""
Workday Careers API: A Quick Start Example
See more at: https://apify.com/johnvc/workday-careers-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/workday-careers-api/input-schema?fpr=9n7kx3

This script shows how to call the Workday Careers API on Apify from Python and
read its structured JSON output: every job on any Workday careers site, with
titles, locations, ISO posted dates, pay ranges, and apply URLs. The default
run exercises several input parameters while staying cheap. Optional --example
recipes mirror published Store tasks (see the README Recipes section).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python workday-careers-api-example.py
  uv run python workday-careers-api-example.py --example nvidia_jobs
  uv run python workday-careers-api-example.py --example remote_jobs
  uv run python workday-careers-api-example.py --example salary_ranges
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/workday-careers-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short summary of dataset rows.

    Args:
        items: Rows returned from the Actor's default dataset.
    """
    print(f"Returned {len(items)} job(s).\n")
    for item in items:
        salary = item.get("salaryText") or "no published range"
        print(f"- {item.get('title')} | {item.get('locationsText')} | "
              f"posted {item.get('postedDate') or item.get('postedOn')} | {salary}")
        print(f"  {item.get('url')}")


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start against Workday's own careers site."""
    # Inputs are kept small (one site, 10 jobs) to keep this first run
    # inexpensive. Set maxJobsPerSite to 0 to fetch every job on the site.
    run_input: dict[str, Any] = {
        "startUrls": [{"url": "https://workday.wd5.myworkdayjobs.com/Workday"}],
        "maxJobsPerSite": 10,
        "includeDetails": True,
        "descriptionFormat": "text",
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_nvidia_jobs(client: ApifyClient) -> None:
    """Mirrors the Store task "Export All NVIDIA Jobs with Salaries and Locations".

    https://apify.com/johnvc/workday-careers-api/examples/nvidia-jobs?fpr=9n7kx3

    The published task exports the full site; this helper clamps the count so
    the demo run stays cheap.
    """
    run_input: dict[str, Any] = {
        "startUrls": [{"url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"}],
        "maxJobsPerSite": 25,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_remote_jobs(client: ApifyClient) -> None:
    """Mirrors the Store task "Find Remote Jobs on Any Workday Careers Site".

    https://apify.com/johnvc/workday-careers-api/examples/find-remote-workday-jobs?fpr=9n7kx3
    """
    run_input: dict[str, Any] = {
        "startUrls": [{"url": "https://workday.wd5.myworkdayjobs.com/Workday"}],
        "searchText": "remote",
        "maxJobsPerSite": 25,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_salary_ranges(client: ApifyClient) -> None:
    """Mirrors the Store task "Extract Jobs with Salary Ranges from Workday Sites".

    https://apify.com/johnvc/workday-careers-api/examples/workday-jobs-with-salaries?fpr=9n7kx3

    Filters client-side to rows where the Actor extracted a pay range.
    """
    run_input: dict[str, Any] = {
        "startUrls": [{"url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"}],
        "maxJobsPerSite": 25,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    with_salary = [i for i in items if i.get("salaryMin")]
    print(f"{len(with_salary)} of {len(items)} jobs carry a published pay range.")
    _print_items(with_salary)


EXAMPLES = {
    "default": run_default,
    "nvidia_jobs": run_nvidia_jobs,
    "remote_jobs": run_remote_jobs,
    "salary_ranges": run_salary_ranges,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Workday Careers API examples")
    parser.add_argument("--example", choices=sorted(EXAMPLES), default="default")
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token or token == "your_apify_api_token_here":
        raise SystemExit(
            "Set APIFY_API_TOKEN in .env first. "
            "Get a free key at https://apify.com?fpr=9n7kx3"
        )
    client = ApifyClient(token)
    EXAMPLES[args.example](client)


if __name__ == "__main__":
    main()
