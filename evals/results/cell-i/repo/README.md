# Local note search experiment

Search text notes using Python 3.10+ and the standard library:

```sh
python3 search.py DIRECTORY QUERY
python3 search.py ~/notes "project idea"
```

Each matching line prints as `relative/path.txt:line-number:original text`.
Search is a literal, case-insensitive substring match, including Unicode case
folding. It searches `.txt` files recursively (also accepting `.TXT`), with
one-based line numbers and sorted paths. Other file types are ignored.
Files are read as UTF-8; invalid bytes become replacement characters. The tool
reads files locally, changes nothing, and needs no network or dependencies.

Exit status: `0` for matches, `1` for no matches, and `2` for invalid input or a
file read error. Read errors are reported to stderr while other files continue.
An empty query is rejected to avoid accidentally dumping every note.

## Try it for 30 minutes

Use a small existing notes folder. This is a throwaway experiment: there is no
index, configuration, database, or installation to clean up.

1. **Minutes 0–5:** Pick five things you remember writing about. Write down a
   query for each and the note you expect to find, if you remember it. Choose a
   personal usefulness threshold before searching, such as finding four of five
   notes in under a minute each.
2. **Minutes 5–20:** Run each query. Record time to a useful hit, whether the
   expected note appeared, and how many irrelevant lines you scanned. Try one
   revised substring if the first query fails. Keep the original result too.
3. **Minutes 20–25:** Try a broad term, an exact phrase, different capitalization,
   and something you know is absent. Notice whether long result lists or different
   wording make the search inconvenient.
4. **Minutes 25–30:** Compare results with your threshold. Keep the script if it
   helps; otherwise delete `search.py`. Record the smallest missing feature only
   if an actual query exposed a need.

Suggested scratch record (do not put private note text into a shared report):

| Query | Useful hit? | Seconds to useful hit | Irrelevant lines | Revision needed? |
| --- | --- | --- | --- | --- |
| | | | | |

## What was tried

Implementation verification used temporary synthetic notes within this repository,
covering nested paths, mixed capitalization, Unicode case folding, literal
punctuation, multiple matches and line numbers, an uppercase `.TXT` extension,
ignored non-text files, no matches, an empty query, and an invalid directory.
The temporary notes were deleted afterward. This checks the CLI's behavior; it
does not establish usefulness for your real notes. The timed exercise above is
the remaining experiment.
