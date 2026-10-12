# Monitor Steam review edits, recommendation flips and developer replies

A game's latest reviews are useful for product feedback, but repeatedly exporting them can fill a feedback database with duplicates. Reviews also change: a player can edit the text or reverse a recommendation, and a developer can reply. I built [Steam Review Scraper - Edits, Flips & Replies](https://apify.com/vdb997/steam-review-change-watch) to compare these fields across runs. This is my paid tool.

## 1. Export a review sample

Open the tool and paste this input:

```json
{
  "appIds": ["413150"],
  "language": "all",
  "maxReviewsPerGame": 100,
  "outputMode": "all"
}
```

413150 is Stardew Valley's public Steam app ID. You can replace it with a supported game's ID or Steam app URL. Set Maximum cost per run to $0.05005 for one game-language check and its start fee at fixed 512 MB memory.

Our development run exported 100 review records and one summary. Records include review text, recommendation, review-context fields and developer-response information where available. The summary separates source query totals from the sample's positive share; the sample is not a random survey of all players.

## 2. Establish a feedback watch

```json
{
  "appIds": ["413150"],
  "language": "all",
  "maxReviewsPerGame": 100,
  "watchId": "game-feedback-watch",
  "outputMode": "changes"
}
```

The first successful changes-mode check establishes a silent baseline. Reuse the same Watch ID on later runs. In our repeat test, the actor scanned 100 reviews, found no matching changes and emitted only the summary. That is a completed quiet check, not a missing dataset.

Newly observed reviews, meaningful text edits, recommendation flips, developer replies and tracked context changes can produce records. Votes or increasing current playtime alone do not cause a review to be treated as edited.

## 3. Filter and integrate

For a complaints workflow, use `recommendationFilter: "negative"`. Output filters are applied after comparison: an initially positive review remains in history, so it can be recognized if it later turns negative. Raise `maxReviewsPerGame` up to 500 if your game's activity requires a wider window.

Once manual checks work, schedule the Actor. In n8n or Make, retrieve the dataset and route `recordType: "review"` records into a feedback database. Store the check summary separately and handle source errors. Avoid overlapping runs with the same Watch ID.

Use review text to investigate themes and individual feedback; this tool does not provide an automatic sentiment model or a revenue forecast.

## Coverage limitations

The Actor uses Valve's current [IUserReviewsService/GetAppReviews API](https://partner.steamgames.com/doc/webapi/IUserReviewsService) and reads the recently updated review window. Anonymous responses may be cached for up to ten minutes. The 500-review cap means busy games can have activity outside the observed window. Missing review IDs are not treated as deleted reviews.

There is no Steam login or separate Valve API key to configure. App metadata lookup must succeed, and failed requested review pages fail the entire check rather than committing partial history.

## Price

$0.05 per successful game-language check, plus $0.00005 per execution start. Platform usage is included. One game checked daily for 30 days costs $1.5015 in event charges. Empty and unchanged successful feeds count too; source failures do not generate the check event, while the start fee still applies. Check the [Store page](https://apify.com/vdb997/steam-review-change-watch) for active pricing.

[Try one game](https://apify.com/vdb997/steam-review-change-watch) or [browse the other public-data monitors](https://apify.com/vdb997).
