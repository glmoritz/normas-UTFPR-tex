# Lessons

Append what each review teaches: wrong rules, new precedents, false positives, what the library
actually returned. Keep entries short and dated, with no student names. When a lesson changes a
rule, update `rules.md` too, and keep the entry so the reason stays visible.

## Reports

- Open items come first, as a numbered list saying what to do. Resolved items come after.
- Resolve what you can, so the student is left mainly with verification.
- Do not add deadlines to a report unless asked.

## Sources

- The GEDWeb viewer refuses the Chrome extension with "A origem da aplicação não pertence ao
  token", even when the person sees the norm. Do not retry or get around it. Ask for excerpts.
- The manual is stricter than NBR 6023 on given names. Prefer the norm's own wording.
- NBR 6023 sets case in the reference list; NBR 10520 sets it in citations.
- utfpr.edu.br pages can fail through a fetch agent while curl with a browser user agent works.
  Files behind "Carregando arquivo..." download by adding `/@@download/file` to the URL.
- Overleaf projects can contain a stale compiled PDF. Review the file the student sent, then
  confirm the source matches it.

## Evidence

- Measure alignment of captions and sources against accepted works. A review once ranked the norm's text above the centered source that every accepted work used; the advisor caught it.
- Check what a dataset citation really describes against the scripts: resolution, year and identifiers can show it is the wrong one.

- Do not raise a tier from one accepted document. A draft did, and a later PPGSE work passed with
  uppercase citations and et al. for three authors.
- Compare figures with any related paper by the student. Only a person can decide how to credit them.
- Script counts miss what pages show: caption position, closed tables, a figure contradicting the text.
- Check `fl.` numbers against the PDF before publishing a report.
- An approval sheet shows title, author, degree, area and date, but not the advisors' roles.

## Files

- Check `git status` before each pass. The advisor may have edited files.
- Ghostscript can claim PDF/A and still fail veraPDF without a real OutputIntent, and it drops links
  unless hyperref has the `pdfa` option. `scripts/make_pdfa.sh` holds the working recipe.
- A date of access is honest only if the link was opened. Crossref gives event city, pages and DOI.
