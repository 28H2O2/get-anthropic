# Project instructions

Read README.md for commands, source behavior and deployment checks.

- Article records are authoritative; Markdown digests are derived output. Never overwrite a valid cached excerpt with a legacy error or older digest.
- `date` means a verified publication date. Keep sitemap lastmod separately and preserve incomplete date precision.
- A translation error must remain retryable and must not appear as article content.
- `summary_en` is an excerpt from the original source, independent of Chinese translation status. Preserve cached excerpts during canonical merges; do not back-translate Chinese excerpts into English.
- Run `python3 -m unittest discover -s tests -v` before building or publishing.
- `python3 build_data.py` validates all enabled source results and writes atomically; source failure must preserve published data.
- GitHub Actions writes data to main daily. Before publishing synchronize remote data, recheck HEAD/status and push only the intended changes. Do not rebase generated data over concurrent unknown changes.
- Credentials are environment-only. Do not print or commit secrets.
