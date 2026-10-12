# Monitor sitemap changes without treating every URL as new

A sitemap export answers which URLs a site lists now. A content-refresh or SEO workflow also needs to know what changed since the last successful scan. I built [Sitemap Extractor & Website URL Change Monitor](https://apify.com/vdb997/sitemap-growth-watch) for that second step. This is my paid tool; the setup below uses one public source.

## 1. Export a small inventory

Open the tool, choose Input, and paste:

```json
{
  "sitemapUrls": ["https://docs.apify.com/sitemap_base.xml"],
  "maxUrlsPerRoot": 1000,
  "maxSitemapsPerRoot": 10,
  "outputMode": "all"
}
```

The URL is the XML sitemap itself. A home page is not a valid substitute. Set Maximum cost per run to $0.20005 for one root check plus its start fee at fixed 512 MB memory.

Our development check returned 710 URL records and one check summary. That inventory size can change. The summary reported complete coverage; inspect the current summary instead of assuming the entire source fit within the configured limits.

## 2. Establish a watch

Run the same input with a Watch ID and changes mode:

```json
{
  "sitemapUrls": ["https://docs.apify.com/sitemap_base.xml"],
  "maxUrlsPerRoot": 1000,
  "maxSitemapsPerRoot": 10,
  "watchId": "documentation-url-watch",
  "outputMode": "changes",
  "trackRemovals": true
}
```

The first successful changes-mode run saves a baseline and returns a summary. Reuse that exact Watch ID on subsequent runs. In our repeat check, 710 URLs were unchanged and no URL change records were emitted. A one-row dataset can therefore be a successful quiet check.

Later datasets can contain newly observed URLs, changed declared `lastmod` values, or removed inventory entries. Changing a filter does not make already observed URLs new again.

## 3. Connect an automation

After manual checks work, create an Apify schedule. For n8n or Make, run the Actor with this input, retrieve its dataset and process `recordType: "url"` records. Store or inspect `check_summary` records separately, particularly `coverageComplete`, `coverageLimits` and `removalsCompared`. Handle `source_error` as a failed source check instead of an empty inventory.

Only fetch or refresh the pages represented by useful URL deltas in your downstream workflow. This tool does not crawl their contents. Avoid overlapping runs with the same Watch ID.

## What removals and dates mean

Two consecutive complete scans are required before comparing removals. A limited scan preserves unseen history and disables removal comparison; the next complete scan restores the baseline. A request or parsing failure preserves the previous snapshot.

`removed` means absent from the scanned sitemap inventory. It does not establish that the page was deleted or returns 404. `lastmod` is the site's declared value, not a verified content modification. Some sites change all dates on every deployment, which can generate many alerts.

The tool supports XML, gzip and same-origin HTTPS sitemap indexes. It respects robots.txt and has limits of 10,000 unique URLs, 20 files and two minutes per root. Cross-origin children and unsupported formats fail the check; capped successful checks explicitly report incomplete coverage.

## Price

$0.20 per successful root check, plus $0.00005 per execution start. Usage is included. One root checked daily for 30 days costs $6.0015 in event charges; empty, unchanged and successful capped checks count too. Source failures do not generate the root event, while the start fee still applies. Check the [Store pricing tab](https://apify.com/vdb997/sitemap-growth-watch) for the active terms.

[Try one sitemap](https://apify.com/vdb997/sitemap-growth-watch) or [browse the other public-data monitors](https://apify.com/vdb997).
