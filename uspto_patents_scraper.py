#!/usr/bin/env python3
"""US patent applications & grants via the official Open Data Portal. Python, Node.js and cURL clients for the USPTO Patents Scraper on Apify, pay per result.

Command-line client for the themineworks/uspto-patents actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/uspto-patents/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/uspto-patents"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--keyword", help="Match applications whose invention title contains this phrase (for example lithium…")
    ap.add_argument("--applicant-name", help="Applicant/company name as filed on the application (for example International Business…")
    ap.add_argument("--inventor-name", help="Inventor name to filter by, formatted as it appears on the patent, for example 'Musk…")
    ap.add_argument("--application-type", help="for example Utility, Design, Plant, Reissue")
    ap.add_argument("--date-from", help="Only applications granted on or after this date, for example 2020-01-01")
    ap.add_argument("--date-to", help="Only applications granted on or before this date, for example 2023-12-31")
    ap.add_argument("--max-results", type=int, help="Maximum number of application records to return")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.keyword is not None: run_input["keyword"] = a.keyword
    if a.applicant_name is not None: run_input["applicantName"] = a.applicant_name
    if a.inventor_name is not None: run_input["inventorName"] = a.inventor_name
    if a.application_type is not None: run_input["applicationType"] = a.application_type
    if a.date_from is not None: run_input["dateFrom"] = a.date_from
    if a.date_to is not None: run_input["dateTo"] = a.date_to
    if a.max_results is not None: run_input["maxResults"] = a.max_results

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
