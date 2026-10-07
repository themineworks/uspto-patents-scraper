# USPTO Patents Scraper: Open Data Portal

Query the official USPTO Open Data Portal for US patent applications and grants: invention title, status, filing/grant dates, patent number, full inventor and applicant lists, CPC classifications, and examiner name. Covers applications, not only granted patents. Requires your own free USPTO API key.

**Run it on Apify:** [apify.com/themineworks/uspto-patents](https://apify.com/themineworks/uspto-patents)
**Docs, FAQ and pricing:** [themineworks.com/actors/uspto-patents](https://themineworks.com/actors/uspto-patents/)

**Price:** From $0.048 per records on Apify's higher plans ($0.08 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Covers applications as well as granted patents
* Full inventor and applicant lists, not just the first name
* CPC classifications and examiner name per record
* Filter by keyword, applicant, inventor, type, or date range
* Bring your own free USPTO Open Data Portal API key

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/uspto-patents").call(run_input={
    "keyword": "machine learning",
    "applicantName": "International Business Machines Corporation",
    "inventorName": "Musk, Elon",
    "applicationType": "Utility"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/uspto-patents').call({
    "keyword": "machine learning",
    "applicantName": "International Business Machines Corporation",
    "inventorName": "Musk, Elon",
    "applicationType": "Utility"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~uspto-patents/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "machine learning", "applicantName": "International Business Machines Corporation", "inventorName": "Musk, Elon", "applicationType": "Utility"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 uspto_patents_scraper.py --token YOUR_APIFY_TOKEN --keyword "machine learning" --applicant-name "International Business Machines Corporation" --inventor-name "Musk, Elon" --application-type "Utility"
node uspto_patents_scraper.mjs --token YOUR_APIFY_TOKEN --keyword "machine learning" --applicant-name "International Business Machines Corporation" --inventor-name "Musk, Elon" --application-type "Utility"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `keyword` | string |  | Match applications whose invention title contains this phrase (for example lithium battery) |
| `applicantName` | string | `""` | Applicant/company name as filed on the application (for example International Business Machines Corporation) |
| `inventorName` | string | `""` | Inventor name to filter by, formatted as it appears on the patent, for example "Musk, Elon" |
| `applicationType` | string | `""` | for example Utility, Design, Plant, Reissue |
| `dateFrom` | string | `""` | Only applications granted on or after this date, for example 2020-01-01 |
| `dateTo` | string | `""` | Only applications granted on or before this date, for example 2023-12-31 |
| `maxResults` | integer | `25` | Maximum number of application records to return |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `application_number` | string | USPTO application number |
| `invention_title` | string | Application/patent title |
| `application_type` | string | for example Utility, Design, Plant, Reissue |
| `status` | string | Current application status description |
| `filing_date` | string | Filing date (YYYY-MM-DD) |
| `grant_date` | string | Grant date (YYYY-MM-DD), absent if not yet granted |
| `patent_number` | string | Granted patent number, absent if not yet granted |
| `first_inventor` | string | First named inventor |
| `first_applicant` | string | First named applicant |
| `inventors` | array | List of inventor names |
| `applicants` | array | List of applicant/assignee-of-record names |
| `cpc_classifications` | array | CPC classification codes |
| `docket_number` | string | Applicant's own docket number, if on file |
| `examiner_name` | string | Assigned USPTO examiner |
| `url` | string | Google Patents URL if granted, else USPTO Patent Center URL |
| `scraped_at` | string | Timestamp when the record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/uspto-patents
```

## FAQ

### Is the old PatentsView-based version still available?

No. Retargeted 2026-08-01. search.patentsview.org no longer resolves at all; this version targets the live replacement, USPTO's Open Data Portal.

### Do I need my own API key?

Yes. As of June 18, 2026, requesting one requires a full USPTO.gov account with mandatory multi-factor authentication. It is sent only as the X-API-KEY header and never written to the dataset.

### Does it only return granted patents?

No. ODP covers applications too. One that hasn't granted yet still returns a full record, just with grant_date and patent_number unset.

### What must I supply as a search filter?

At least one of keyword, applicantName, inventorName, or applicationType.

### What does it cost?

Pay per record delivered. Failed and empty results are never charged.

### Is the examiner named in the record?

Yes. Each record carries the examiner name alongside CPC classifications, the full inventor and applicant lists, and filing and grant dates.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [India Gov Data](https://themineworks.com/actors/india-data-gov-scraper/): Trade, prices, and thousands of datasets from data.gov.in
* [CourtListener Scraper](https://themineworks.com/actors/courtlistener-court-records/): US court opinions, dockets, and case law as structured JSON
* [Socrata Open Data](https://themineworks.com/actors/socrata-open-data/): Any government data portal: CDC, HHS, NYC, Texas, and hundreds more

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
