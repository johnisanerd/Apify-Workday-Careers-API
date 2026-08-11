# Workday Jobs API: Scrape Any Workday Careers Site from Python or MCP

This repo shows two ways to use the [Workday Careers API](https://apify.com/johnvc/workday-careers-api?fpr=9n7kx3) on Apify: a Python quick start managed with `uv`, and MCP install guides for five AI clients (Claude Cowork Desktop, Claude Code, Claude on the web, Cursor, and ChatGPT).

Give the API any Workday careers URL, like `https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite`, and it returns every live job posting as structured JSON: titles, locations, exact ISO posted dates, full descriptions, extracted pay ranges, employment type, remote status, requisition IDs, and direct apply URLs. Thousands of Fortune 500 employers run hiring on the Workday ATS, and this is the practical Workday API for their public job data: no login, no proxies, pay per result.

## Video walkthrough

[![Apify MCP setup walkthrough](https://img.youtube.com/vi/jREWahDGhJM/0.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

Searching for a Workday API for job postings usually leads to Workday's enterprise SOAP and REST APIs, which need tenant credentials and never expose public listings. This Actor takes the other path: you give it the careers-site URL any candidate can open, and it reads the same public data feed the page itself uses. The main input is `startUrls` (one or more Workday careers URLs, both `myworkdayjobs.com` and `myworkdaysite.com` forms work); the main outputs are `title`, `locationsText`, `postedDate`, `salaryMin`/`salaryMax`, `descriptionText`, and `applyUrl`, one row per job. A concrete example from a published task: run it on NVIDIA's careers site and you get every one of its thousands of live openings, with US pay-transparency ranges parsed into numeric fields, ready for a job board, hiring-trend dashboard, or scheduled monitor.

## Python quick start

1. Get your free Apify API key: https://apify.com?fpr=9n7kx3
2. Clone this repo, then:

```bash
cp .env.example .env   # paste your APIFY_API_TOKEN inside
uv sync
uv run python workday-careers-api-example.py
```

The default run pulls 10 jobs from Workday's own careers site so your first call costs a fraction of a cent. Task-aligned recipes:

```bash
uv run python workday-careers-api-example.py --example nvidia_jobs
uv run python workday-careers-api-example.py --example remote_jobs
uv run python workday-careers-api-example.py --example salary_ranges
```

## Input parameters

| Parameter | Type | Description |
|---|---|---|
| `startUrls` | array (required) | One or more Workday careers URLs. Locale segments and both URL families are handled automatically. |
| `searchText` | string | Keyword query, same behavior as the search box on the careers page. |
| `maxJobsPerSite` | integer | Cap per site; `0` means every job. |
| `includeDetails` | boolean | `true` (default) fetches full details per job; `false` is a fast list-only mode, one request per 20 jobs. |
| `descriptionFormat` | enum | `both`, `html`, or `text`. |
| `postedAfter` | string | ISO date filter, requires `includeDetails`. |
| `detailConcurrency` | integer | Parallel detail requests, 1 to 10 (default 5). |

## Output fields

One row per job: `title`, `company`, `tenant`, `siteId`, `sourceUrl`, `url`, `applyUrl`, `jobReqId`, `jobPostingId`, `workdayInternalId`, `locationsText`, `primaryLocation`, `additionalLocations`, `country`, `countryCode`, `postedOn`, `postedDate`, `endDate`, `timeLeftToApply`, `timeType`, `remoteType`, `canApply`, `descriptionHtml`, `descriptionText`, `salaryText`, `salaryMin`, `salaryMax`, `salaryCurrency`, `scrapedAt`, `totalJobsOnSite`. A `SITE_SUMMARY` key-value record adds per-site totals and facet counts.

## Recipes: ready-to-run Store tasks

Each recipe is a one-click landing page on Apify Store; clone it and swap in your target URL:

- [Export All NVIDIA Jobs with Salaries and Locations](https://apify.com/johnvc/workday-careers-api/examples/nvidia-jobs?fpr=9n7kx3)
- [Monitor New Workday Job Postings for Any Company](https://apify.com/johnvc/workday-careers-api/examples/monitor-workday-job-postings?fpr=9n7kx3)
- [Find Remote Jobs on Any Workday Careers Site](https://apify.com/johnvc/workday-careers-api/examples/find-remote-workday-jobs?fpr=9n7kx3)
- [Extract Jobs with Salary Ranges from Workday Sites](https://apify.com/johnvc/workday-careers-api/examples/workday-jobs-with-salaries?fpr=9n7kx3)
- [Export Workday Job Listings to JSON, CSV or Excel](https://apify.com/johnvc/workday-careers-api/examples/export-workday-job-listings?fpr=9n7kx3)

Tip: put any of these on an Apify Schedule (for example daily) and diff on `jobReqId` to catch new Workday job postings the day they appear.

## FAQ: people also ask

**Does Workday have a REST API for job postings?**
Workday's official APIs cover internal HR integrations and need tenant credentials. For public job listings, this Actor is the practical Workday jobs API: paste the careers URL, get JSON.

**Is Workday an ATS?**
Yes, Workday Recruiting is one of the most widely used enterprise applicant tracking systems, and every customer publishes jobs on a public Workday careers site this API can read.

**Which companies can I scrape jobs from?**
Any employer whose careers page lives on `myworkdayjobs.com` or `myworkdaysite.com`: NVIDIA, Adobe, Intel, Disney, PayPal, Capital One, Target, Salesforce, and thousands more.

**What is the best MCP server for Workday job data?**
The hosted Apify MCP server with this Actor attached; the five install sections below wire it into Claude, Cursor, or ChatGPT in a few minutes.

**What is myworkdaysite.com?**
The second official domain Workday hosts customer career sites on (for example Mondelez). This API handles both URL families.

---

The Actor's MCP server URL, used in all five install sections below:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api
```

The `actors` and `docs` tools let the assistant discover and read Apify docs, while preloading just this one Actor keeps the tool list small. Auth is either OAuth in the browser when offered, or your Apify API token (the same `APIFY_API_TOKEN` secret used by the Python example). Get a token at https://console.apify.com/settings/integrations and a free Apify account at https://apify.com?fpr=9n7kx3 .

## Use from n8n

Available as an n8n community node, **[n8n-nodes-workday-jobs-api](https://www.npmjs.com/package/n8n-nodes-workday-jobs-api)**. In n8n: Settings, Community Nodes, install `n8n-nodes-workday-jobs-api`, then use it in any workflow (it also works as an AI Agent tool).

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Workday Careers API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Workday Careers API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Workday Careers API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/workday-careers-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api`, using OAuth when prompted.
5. Ask Claude to run the Workday Careers API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Workday Careers API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/workday-careers-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[View the Workday Careers API on Apify Store](https://apify.com/johnvc/workday-careers-api?fpr=9n7kx3)

Last Updated: 2026.08.11
