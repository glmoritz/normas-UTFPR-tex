---
name: utfpr-norm-review
description: Review a UTFPR thesis, dissertation or TCC against UTFPR and ABNT norms, fix what is safe, and write a report for the student and advisor listing what went wrong, what changed, and the reference behind each item. Use whenever the user wants to check, conferir, revisar or normalizar an academic work for UTFPR, mentions ABNT or NBR formatting of a thesis, deposit or entrega at the biblioteca, PDF/A, folha de rosto, folha de aprovação, or citations and references in a dissertation, even if they do not name the norms.
---

# UTFPR norm review

Check an academic work against the rules UTFPR actually applies, make the safe fixes, and tell
the student and advisor what happened. Each item ends in one of two ways: it is corrected, or the
work is rejected on it, and either way the report says why. The report matters as much as the fixes. Students learn
from it, and the advisor must validate conformity before deposit (IN 31/2023, art. 4º).

Two things make a review trustworthy, so protect them throughout:
- **Every claim has a reference** that can be opened and checked.
- **Every change is reported.** A student should never find an edit the report does not list.
- **Every finding says why.** A rejection without a reason teaches nothing, and the student
  cannot argue with it or learn from it.

## Files

- `references/rules.md`: rule catalog with tiers, sources, and who can fix each item
- `references/sources.json`: source registry used for report links
- `references/precedents.md`: documents the library accepted; these set how strict to be
- `references/latex-templates.md`: settings to check per template
- `references/lessons.md`: what past reviews taught; read before starting
- `references/local.md` (optional, private): one advisor's settings; see `local.example.md`
- `scripts/check_pdf.py`, `scripts/check_tex.py`: measurements
- `scripts/build_report.py`: builds and verifies the report
- `scripts/make_pdfa.sh`: converts to PDF/A-2b and validates with veraPDF

## Workflow

### 1. Prepare

Read `rules.md`, `precedents.md` and `lessons.md`, plus `references/local.md` if it exists: it holds
one advisor's own settings. Then establish:
- the source project and the PDF under review; compile a copy if the PDF is older than the source
- work type (TCC, dissertation, thesis) and program
- whether this is the version for defense or the final one for deposit

Dissertations and theses use IN 31, the Mestrado e Doutorado procedure, and at PPGSE the page
"Procedimentos para defesa" with its checklist. TCCs use the delivery
page and the manual; their approval sheet is not system-issued. Article-format work needs the
ART rules: read Res. PPGSE 10/2024 and IN 01/2017 first, since they disagree on the article count.

If the work is at an early stage, or the project is far from the template, recommend restarting
from the PPGSE template in `latex-templates.md`. Most formatting errors go away there, so one
report line saying so is worth more than dozens of small findings.

Ask for what only people have: the system's defense data, the approval sheet PDF, the license
choice, funding, and any company or personal data used. List the gaps instead of guessing.

### 2. Measure

```bash
python3 -I <skill>/scripts/check_tex.py <project>
python3 -I <skill>/scripts/check_pdf.py <file.pdf>
```

Treat the output as measurements. Open the pages behind any surprising number, because text
extraction can miss things and heuristics misfire. All-caps names, for example, may be acronyms.

Check the template settings against `latex-templates.md` first. One option can explain dozens
of findings, and the fix belongs at the cause.

Pagination gets special care, because the library often returns works for it. Read the
`pagination` block of `check_pdf.py`, and repeat it after any change that adds pages, such as
inserting the approval sheet. A clean result on a draft does not carry over to the final file.

### 3. Review what scripts cannot see

Read the rules in `rules.md` and inspect the rendered pages for the rest: cover and rosto against
the manual's models, figure placement and legibility, table style, reference content, and the
acknowledgments. Render pages to images when layout matters.

### 4. Assign tiers

`rules.md` gives each rule a default tier. Adjust from evidence, in this order of authority:

1. UTFPR regulations and library procedures (IN 31, COUNI 78, program rules)
2. What accepted documents and the PPGSE template actually do
3. Current ABNT editions
4. UTFPR manual, for what the others leave open

- **Bloqueia o depósito:** on the library's verification list, or required by the norm and
  followed by accepted documents.
- **Corrigir:** required by a current rule; accepted documents follow it or do not test it.
- **Recomendação:** in a norm or the manual, but an accepted document passed without it, or
  it is only a recommendation.

The advisor's position is to follow what is used, so a tolerated deviation drops to
Recomendação. It stays in the report, because the precedents are few. Raise a tier only with
evidence from accepted work or the library, never from one document alone.

### 5. Decide each item: correct it or reject

Resolve as much as you can, so the student is left mainly with verification. Look data up rather
than handing it back: Crossref for events, official sources for legislation, opening each link
to set a real access date.

- If it can be fixed safely, fix it, and say what changed and why.
- If not, it stays open, with the reason and what would clear it.

Fixing does not need permission for each item, but it does need the safety test below.


Apply a fix when all of these hold:
- the rule marks it `auto`, or the correct result follows entirely from the document and the rule
- it changes presentation, not scholarship or meaning
- the result can be verified by compiling

Leave these to people, however easy they look:
- bibliographic data, sources of figures, dates, names, grant numbers: never invent or infer
- whether third-party material was used, and whose it is
- the license, the degree name, and anything that must match the Sistema Acadêmico
- rewording of the student's argument

A figure's source can be filled in only when the project shows it is the author's own, such as
a plot built by a script in the repo. When unsure, leave the finding open for the student.

Edit the working tree only. Do not commit or push unless asked, since many projects sync to
Overleaf, and do not overwrite the student's PDF: compile in a copy, then confirm it builds.
Record each change as you make it.

Keep norm PDFs and any file holding access tokens out of the project.

### 6. Write the report

Write the findings JSON, then build:

```bash
python3 -I <skill>/scripts/build_report.py findings.json correcoes_<slug>_<data>.html --root <project>
```

Write the report in Portuguese, addressed to the student, in plain language. The build fails if
a finding has no reason, if a claimed change is not in its file, or if a changed file is
unlisted. Fix the log or the edit; do not bypass the check to get a report out.

The report opens with what is still open, as a numbered list where each item says what to do.
Everything resolved comes after it. A reader must see in seconds what is left.

The script computes the verdict from the findings, so it cannot be softened by wording:
- **Rejeitado:** at least one open blocker that is not just a confirmation
- **Falta só conferir:** only confirmations and lesser items remain
- **Aprovado:** nothing open

`PRO-` items are reminders and do not count. Tolerated deviations use status `aceito`: they appear
under "Sem ação necessária", not as pending. For open items, write `acao` as an instruction.

When the user wants to verify before anything changes, set `"modo": "proposta"`, apply the fixes
to a compiled copy instead, point `--root` at that copy, and mark those findings `proposto`. They
still count as open in the verdict. Give the user the patch alongside the report.

Writing good entries:
- Cite the sheet (`fl.`, the PDF page) so the student can find it.
- Show an example from the work, not just a rule name.
- Say why in `porque` in plain words: what the rule protects, or what the library will do.
- Group repeats into one finding with a count and the locations.
- Link at least one source per finding. Use `MAN` with `pagina` so the link opens at that page.
  Problems outside the norms, such as typos or data that contradicts the text, go in their own
  `OBS` group with no source, because the reason is the document itself.
- Fill `limites` honestly: rules resting on the manual instead of the norm, the Sistema
  Acadêmico data not seen, or a PDF that was not the final one.

When others will read the report, publish it with the Artifact tool and give the link.

### 7. Close the loop

Warn about any deadline first. Then tell the user the status in a few lines and point to the report: blockers open, what changed,
and what is needed from whom.

Then improve the skill. Add what this review taught to `lessons.md`, correct `rules.md` if a rule
was wrong, and add confirmed deposits to `precedents.md`. When the advisor or the library reports
an outcome, record it, because real results are the best evidence this skill has.

## Source limits

ABNT text sits behind the GEDWeb login, and the Chrome extension cannot read its viewer. Rules
from NBR 6024 and 6027 currently rest on the manual; `sources.json` records this, and the report
must state it. NBR 14724 was read without the corrected version of 01.04.2025. Paraphrase
ABNT content and do not store its text in this skill.
