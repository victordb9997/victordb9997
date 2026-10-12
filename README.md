# Public data monitors on Apify

I build public-data tools that export current records and compare later runs, so an automation can process changes instead of repeating the same data.

## Start with a use case

- **SEO and content teams:** [extract sitemap URLs and monitor inventory changes](https://apify.com/vdb997/sitemap-growth-watch). XML, gzip and nested indexes; coverage reports explain whether removals can be compared. [Try the walkthrough](apify-guides/sitemap-monitoring.md).
- **Game studios:** [scrape Steam reviews and monitor edits, recommendation flips and developer replies](https://apify.com/vdb997/steam-review-change-watch). [Try the walkthrough](apify-guides/steam-review-monitoring.md).
- **Recruiting teams:** [monitor Greenhouse, Lever and Ashby jobs](https://apify.com/vdb997/ats-job-watch), including newly observed, edited and removed postings.

## Tools and prices

| Tool | What a successful check covers | USD/check |
| --- | --- | ---: |
| [ATS Job Scraper](https://apify.com/vdb997/ats-job-watch) | One Greenhouse, Lever or Ashby company board; up to 5,000 jobs | 0.025 |
| [Shopify Price & Restock Monitor](https://apify.com/vdb997/shopify-price-restock-watch) | One product and returned variants | 0.01 |
| [Google News Scraper](https://apify.com/vdb997/google-news-keyword-watch) | One query; up to 100 feed articles | 0.025 |
| [App Store Review Scraper](https://apify.com/vdb997/app-store-review-watch) | One iOS app and country; up to 500 recent reviews | 0.025 |
| [WordPress Post Scraper](https://apify.com/vdb997/wordpress-content-watch) | One public WordPress site; up to 500 posts | 0.05 |
| [Steam Review Scraper](https://apify.com/vdb997/steam-review-change-watch) | One game and language; up to 500 recently updated reviews | 0.05 |
| [Sitemap Extractor](https://apify.com/vdb997/sitemap-growth-watch) | One root; up to 10,000 unique URLs and 20 sitemap files | 0.20 |

Each execution adds a $0.00005 start event at fixed 512 MB memory. Platform usage is included. Successful empty, unchanged and supported capped checks still count; source failures do not generate a check event. Read each Store page for current pricing and scope. Running these tools requires your own Apify account.

## How to try a monitor

1. Open a tool, copy its quick-start input and query one source in `all` mode.
2. Inspect records and the check summary, then export JSON, CSV or Excel.
3. Give the watch a stable ID and switch to `changes` mode. Its first successful run establishes the baseline.
4. Reuse that ID for later runs. Schedule checks after the manual example works and cap the run budget.

For n8n or Make, run the Actor through the Apify integration and process its dataset. Route data records separately from check summaries and source errors. Keep runs with the same Watch ID from overlapping.

## Verified development examples

These are development checks, not customer case studies:

- **Steam:** exported 100 Stardew Valley reviews. A repeat scanned the same 100 reviews and emitted only a summary, with zero matching change records.
- **Sitemap:** exported 710 URLs from the Apify documentation base sitemap with complete coverage. A repeat emitted only a summary, with 710 unchanged URLs and zero new, changed or removed URLs.

Change output depends on source activity and coverage. Steam observes a capped window; sitemap `lastmod` values are site declarations and missing inventory entries do not establish page deletion.

[Browse all tools on Apify](https://apify.com/vdb997). I maintain these tools; the links lead to my paid listings. Questions and source-specific issues can be reported through each tool's public Issues tab.
