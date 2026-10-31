# Local note-search experiment

Python 3.10+, standard library only. Reads notes without modifying them; no network
calls, installation, indexing, or configuration.

```sh
python3 search.py /path/to/notes "project idea"
```

Searches `.txt` files recursively for a literal, case-insensitive substring. Each
matching line is printed once as `relative/path.txt:line-number:original text`, in
path order, with line numbers starting at 1. Quote queries containing spaces.
Notes are read as UTF-8; undecodable bytes are replaced. Matches are within one
line, without ranking, fuzzy matching, or word-boundary rules.

Exit status: 0 for matches, 1 for no matches, 2 for invalid arguments or a reported
file-reading error. An empty query is rejected.

## Try it for 30 minutes

1. **0–5 minutes:** Pick a directory of your text notes and five real questions
   you would normally answer by hunting through them. Include a known phrase,
   a partial word, an ambiguous term, and something you think is absent.
2. **5–20 minutes:** Run a query for each question. Record the query, relevant
   hits, distracting hits, whether you found the needed note, and approximate time.
   Try one revised query when the first result is poor.
3. **20–30 minutes:** Compare with your normal way of finding notes. Keep the
   script if it saves time on enough of your actual questions; otherwise delete
   `search.py`. Note whether failures came from choosing words, too many hits,
   encoding, or needing other file formats before adding features.

## What was tried

Synthetic notes checked nested paths, multiple matches, mixed case, partial-word
matches, literal punctuation, preserved line text, and exclusion of non-`.txt`
files. Empty/no-match queries and a missing directory were checked too.
This establishes that the search mechanics work; usefulness on your own notes
still requires the short trial above. No real notes were supplied or searched.
