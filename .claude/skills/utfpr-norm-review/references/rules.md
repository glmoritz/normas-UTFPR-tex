# Rule catalog

Rules are paraphrased, never copied from ABNT text. Source IDs are keys of `sources.json`.

**Tier:** B = blocks deposit, C = correct, A = advice. See SKILL.md for how tiers are assigned.
**Fix:** `auto` = apply if mechanical and safe; `aluno` = student must supply content;
`orientador` = advisor decides; `manual` = must be inspected by eye.

Tiers already reflect the accepted precedents and the PPGSE template. Where the manual disagrees
with a current ABNT edition, the ABNT edition is the reference for advice, unless practice differs.

## Delivery and file (IN 31 is the rule of record)

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| ARQ-01 | B | Final file is PDF/A. Accepted files are PDF/A-2b and PDF/A-1b, both converted after compiling | IN31 art. 2º, I; ENT; ACEITO; ACEITO2 | auto, final version only |
| ARQ-02 | B | File name: up to 4 significant title words, lowercase, no spaces, accents, cedilla, dots, special chars, articles, prepositions, conjunctions. Products add `_produto` | IN31 art. 3º; ENT | auto, final copy only |
| ARQ-03 | B | Size at most 50 MB; above 9 MB some browsers struggle (warn) | ENT | aluno |
| ARQ-04 | A | Properties hold title, author, keywords. Accepted file left them blank; still fill them | IN31 art. 2º | auto |

## Program process (PPGSE)

The program's page "Procedimentos para defesa" and its checklist cover what happens around the
document. These items do not change the document and do not affect its verdict. List them in
the report under their own group as reminders, for the student to confirm.

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| PRO-02 | B | Delivered within the deadline in the ata, at most 90 days after the defense. Missing it means "Reprovado". Calculate the date from the approval sheet and warn first if it is near or past | PPGSE; COUNI78; CHECK item 10 | aluno |
| PRO-03 | B | Corrections requested by the committee are done, with the advisor's approval | CHECK item 9; IN31 art. 4º | aluno |
| PRO-04 | B | Lattes URL with the Lattes ID and full ORCID URL registered in the Portal do Aluno; the repository needs both | CHECK item 1.9 | aluno |
| PRO-05 | C | Lattes lists the program as "Sistemas de Energia", CAPES code 40006018038P2 | PPGSEDEF | aluno |
| PRO-06 | C | Publication or submission requirement met, as the program's rules set | CHECK item 1.4; PPGSE | aluno |
| PRO-07 | A | Word users follow the library's norms and its .docx templates; LaTeX users start from the program's model | PPGSEDEF; MODELO | aluno |

## Article-format dissertation

Applies only to a work presented as a collection of articles. Check each item.

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| ART-01 | B | Has all required pre- and post-textual elements, plus introductory sections on the problem, objectives and method that tie the articles together | IN0117 art. 1º | aluno |
| ART-02 | B | Articles already published, with the candidate as first author and the advisor as co-author | IN0117 art. 2º; PPGSE10 | aluno |
| ART-03 | B | Journal meets the quality bar in the year of publication (Qualis or equivalent) and the PPGSE relevance criteria | IN0117 art. 2º, II; PPGSE10 | orientador |
| ART-04 | B | Number of articles. **The rules conflict:** IN 01/2017 asks for at least 2 for a master's, Res. PPGSE 10/2024 for at least 1. Flag it for the advisor; do not decide | IN0117 art. 2º, III; PPGSE10 | orientador |
| ART-05 | B | Proof that each article may be deposited in the repository: open license, journal policy screen, or signed document | IN0117 art. 3º, 4º | aluno |
| ART-06 | B | Copyright was not transferred in a way that blocks the repository; the authorized version is the one included | IN0117 art. 3º | aluno |

## Identification

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| ID-01 | B | Author, advisor, co-advisor, committee, title and defense date match "Marcação/Resultado de Defesa" in the Sistema Acadêmico exactly | IN31 art. 1º, V; PROC | aluno |
| ID-02 | B | Folha de rosto carries title in the text language plus translation (English, or Portuguese if the text is in another language) | PROC; MAN p. 15 | aluno |
| ID-03 | B | Creative Commons license in the rosto footer: icon, version as active link, summary. License is set by the program | IN31 art. 1º, III; PROC; MAN p. 15-16 | orientador |
| ID-04 | B | Approval sheet is issued by the Sistema Acadêmico, no signatures or initials, and is inside the final file. A placeholder is rejected. This overrides the signatures in NBR 14724 §4.2.1.3 | IN31 art. 5º; PROC; MAN p. 17; CHECK item 11, 15.1 | aluno |
| ID-05 | B | Title identical on cover, rosto and approval sheet | MAN p. 13; PROC | auto |
| ID-06 | C | Cover: institution, author, title, subtitle after colon, city of the campus, deposit year. Title uppercase and bold is UTFPR practice | NBR14724 §4.1.1; MAN p. 13-14 | auto |
| ID-07 | C | Natureza states work type, goal, institution, concentration area, right-aligned block from mid-page, single-spaced. At PPGSE the degree reads "Mestre em Engenharia Elétrica" (template, P2 and its system sheet) | NBR14724 §4.2.1.1.1, §5.2; MAN p. 15-16; MODELO; ACEITO2 | auto |
| ID-08 | C | Advisor and co-advisor names in full, as in Lattes | MAN p. 15 | aluno |
| ID-09 | A | Ficha catalográfica. NBR asks for it; neither accepted file has one and the manual does not list it as mandatory | NBR14724 §4.2.1.1.2; ACEITO; ACEITO2 | orientador |

Do not copy the accepted file's cover year (2024 with a 2025 defense). It looks like a slip.

## Acknowledgments and authorizations

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| ACK-01 | B | Funded work names agency and grant number in the last paragraph of Agradecimentos | IN31 art. 6º; PROC; MAN p. 20 | aluno |
| ACK-02 | B | Work using LABIC infrastructure must thank it with the exact name. PT: "Laboratório Multiusuário de Inteligência Computacional - LABIC, câmpus Curitiba". EN: "Computational Intelligence Laboratory - LABIC, Curitiba, Brazil". Users also send LABIC the full reference | LABIC art. 19 | auto if use is confirmed |
| ACK-03 | C | Agradecimentos names no company or institution absent from the text | MAN p. 20 | aluno |
| ACK-04 | B | Company or institution data needs the signed Termo de Autorização | IN31 art. 9º; PROC | aluno |
| ACK-05 | B | Images, voices or digital data of people need the signed Termo de Uso | IN31 art. 10; PROC | aluno |
| ACK-06 | B | Human or animal research needs CEP/CEUA approval, with process number in the methodology | IN31 art. 7º | aluno |

Local policy: if `references/local.md` exists, apply what it says, such as an advisor's grant number.

## Structure and abstract

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| EST-01 | B | Required elements present: cover, rosto, approval, resumo, abstract, sumário, introduction, development, conclusion, references | NBR14724 §4; MAN p. 12 | aluno |
| EST-02 | C | Pre-textual order follows the scheme. Pre-textual elements stay out of the sumário; post-textual ones appear in it | NBR14724 §4.2.1; NBR6027 p. 34 | auto |
| EST-04 | C | An epígrafe is a citation: its author goes in the reference list | MAN p. 20 | aluno |
| EST-05 | C | Apêndice and anexo each open with an indicator page holding only `APÊNDICE A – Título` (or `ANEXO A – ...`), centered; the document starts on the next page. Apêndice is the author's own material, anexo is someone else's | NBR14724 §4.2.3; MAN p. 23-24 | auto |
| EST-06 | C | Every section has text of its own: no heading followed directly by a subheading (e.g. `1.2 OBJETIVOS` then `1.2.1`) | NBR6024 (via MAN p. 27) | aluno |
| EST-07 | A | Section numbers in arabic digits, one space before the title, left-aligned, at most five levels (three recommended); text starts on the next line | NBR6024 (via MAN p. 27) | auto |
| LST-01 | C | Lista de siglas in alphabetical order, each followed by its meaning | NBR14724 §4.2.1.11; MAN p. 21 | auto |
| LST-02 | A | Separate lists by illustration type (figuras, quadros, gráficos) when a type has more than three items | MAN p. 21 | auto |
| EST-03 | A | The norm says sections, not "capítulos". Both accepted files use the word | NBR14724 §4.2.2; ACEITO; ACEITO2 | auto, if asked |
| RES-01 | C | One paragraph, informative, 150 to 500 words, third person advised | NBR6028 §4.1.2-4.1.4, §4.1.8; MAN p. 29 | aluno |
| RES-02 | A | Keywords right below the abstract, separated by `;`, ending with `.` The current template does this. P1 did; P2 used periods and passed | NBR6028 §4.1.7; MAN p. 29; MODELO; ACEITO2 | auto |
| RES-03 | A | Keywords start lowercase except proper names. Accepted file capitalized them | NBR6028 §4.1.7; ACEITO | auto |
| RES-04 | A | Avoid uncommon abbreviations, symbols, formulas. Manual is stricter (none); accepted file uses IoT | NBR6028 §3.3; MAN p. 29; ACEITO | aluno |
| RES-05 | C | Abstract matches the resumo in content | NBR14724 §4.2.1.8 | aluno |
| RES-06 | B | No reference of the work (`AUTOR. Título. 2026. 80 f. Dissertação ...`) above the resumo or the abstract, and no citations in them. The manual only "suggests" it and P2 passed with it, but the library returned a PPGSE dissertation for it in Nov 2026. `normas-utf-tex` prints it from the class, including the current `ppgse-cc` branch | MAN p. 29; NBR6028; DEVOL1 | auto |
| RES-07 | A | Keywords taken from a controlled vocabulary, such as the Biblioteca Nacional authority catalog (termo tópico), with the matching English term in Keywords | MAN p. 32 | aluno |

## Layout

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| FMT-01 | C | A4; left and top 3 cm, right and bottom 2 cm | NBR14724 §5.1; MAN p. 8 | auto |
| FMT-02 | C | 12 pt text; smaller and uniform (10 pt at UTFPR) for long quotes, footnotes, page numbers, captions, sources | NBR14724 §5.1; MAN p. 9 | auto |
| FMT-03 | C | 1,5 line spacing; single for long quotes, footnotes, references, captions, sources, natureza | NBR14724 §5.2; MAN p. 8 | auto |
| FMT-05 | A | One typeface throughout; Arial or Times recommended. Black text | MAN p. 9; NBR14724 §5.1 | auto |
| FMT-06 | C | Section number and title share the same emphasis, in the sumário and the text. Primary sections start a new page | NBR14724 §5.2.2, §5.4; MAN p. 26-27 | auto |
| FMT-07 | C | Unnumbered titles centered, bold, uppercase | NBR14724 §5.2.3; MAN p. 25 | auto |
| FMT-08 | C | Acronym: full name first, acronym in parentheses, on first mention | NBR14724 §5.6 | auto |
| FMT-09 | A | Alíneas `a)` rather than bullets. Both accepted files used bullets | NBR6024 p. 27; ACEITO; ACEITO2 | auto |
| FMT-10 | A | Display equations numbered in parentheses at right when referenced | NBR14724 §5.7 | manual |
| FMT-12 | A | No extra space before or after paragraphs | MAN p. 8 | auto |
| FMT-11 | C | Footnotes inside margins, 5 cm rule, smaller type | NBR14724 §5.2.1 | auto |

## Pagination

The library often sends works back for page counts (advisor's report), so check this every time,
and again after the approval sheet goes in, because it shifts every later page.

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| PAG-01 | B | Cover not counted; rosto is sheet 1. Every printed number equals the PDF page minus 1. Both accepted files and the template do this | MAN p. 28; NBR14724 §5.3; ACEITO; ACEITO2; MODELO; ORIENT | auto |
| PAG-02 | B | No hard-coded counter (`\\setcounter{page}{N}`) in the source; it breaks the count whenever a page is added | MAN p. 28; ORIENT | auto |
| PAG-03 | B | Numbers appear from the first textual page to the last page, with no gaps, including appendices, annexes and pages from `\\includepdf` | NBR14724 §5.3; ORIENT | auto |
| PAG-04 | B | Sumário numbers match the printed pages, recompiled until stable | NBR6027 p. 34; ORIENT | auto |
| PAG-05 | C | Page number at top right, 2 cm from the edges, in smaller type | NBR14724 §5.3; MAN p. 9, p. 28 | auto |

## Figures and tables

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| FIG-01 | B | Every illustration and table has a source line right after it. Accepted file does | NBR14724 §5.8, §5.9; MAN p. 36; ACEITO | auto only for the author's own generated work |
| FIG-02 | B | Caption above the illustration: type, number, dash, title; source right after it. Both accepted files and the template do this | NBR14724 §5.8; MODELO; ACEITO; ACEITO2 | auto |
| FIG-03 | C | Own work states it, in one consistent form. The template and P2 use "Fonte: Autoria própria." Manual also asks for the year, and P2 passed without it | NBR14724 §5.8; MAN p. 36; MODELO; ACEITO2 | auto |
| FIG-04 | C | Source line centered right below the illustration. Short captions centered too; long ones fill the width. Both accepted files, the template and the manual do this, so it overrides a strict reading of §5.8 | MAN p. 36; ACEITO; ACEITO2; MODELO; NBR14724 §5.8 | auto |
| FIG-05 | C | Cited in the text and placed near the citation | NBR14724 §5.8, §5.9 | manual |
| FIG-06 | C | Authors named in sources are in the reference list | MAN p. 36 | aluno |
| FIG-07 | C | Tables follow IBGE: open sides, source line. Quadros are closed and qualitative | NBR14724 §5.9; MAN p. 39-40 | manual |
| FIG-08 | A | Screenshots and small text stay legible at print size | NBR14724 §5.8 | aluno |
| FIG-09 | A | Bold title and source suggested at UTFPR | MAN p. 36 | auto |

| FIG-10 | A | Keep captions as titles. Long descriptions fill the list of figures; `\\caption[short]{long}` keeps the list brief | NBR14724 §4.2.1.9, §5.8 | aluno |
| ANX-01 | C | An annex states where it came from, in the annex itself (note or list) | NBR14724 §4.2.3.1 | auto when the source is known |
| ANX-02 | C | Third-party material: the author holds the rights to reproduce it and it is compatible with the license | IN31 art. 11; MAN p. 16 | aluno |

## Citations

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| CIT-01 | A | NBR 10520:2023 uses upper and lower case: `(Silva, 2019)`. Library practice is split: P1 mixed case, P2 (PPGSE, 2026) uppercase with the current template, even though the program's page says the model meets NBR 10520/2023. Follow the template; only require one form throughout | NBR10520 §6.1.1.1; MODELO; ACEITO; ACEITO2 | auto, if asked |
| CIT-02 | A | Norm allows *et al.* from 4 authors, used uniformly. P1 followed this; P2 and the template use it from 3 (`abnt-etal-cite=2`) and passed | NBR10520 §6.1.2; MAN p. 45; ACEITO; ACEITO2 | auto, if asked |
| CIT-03 | C | One call system throughout; author-date at UTFPR. Numeric is barred if there are notes | NBR10520 §6, §6.2.2; MAN p. 43 | auto |
| CIT-04 | B | Every citation is in the reference list, and the list holds only cited works | NBR10520 §5.1; MAN p. 43 | aluno |
| CIT-05 | C | Direct quote has page or locator. Over 3 lines: indented (4 cm advised), smaller, single-spaced, no quotes | NBR10520 §6.1.3, §7.1, §7.1.1; MAN p. 42 | manual |
| CIT-06 | C | Translated quote says "tradução nossa"; added emphasis says "grifo nosso" | NBR10520 §7.1.5, §7.1.6 | aluno |
| CIT-07 | C | apud: reference list holds only the consulted source. Avoid when possible | NBR10520 §7.3; MAN p. 41 | aluno |
| CIT-08 | C | Same author and year get letters; several authors separated by `;`, alphabetical advised | NBR10520 §6.1.6, §6.1.8 | auto |

## References

From NBR 6023:2018, read directly. Citations in the text are a different matter: see CIT-01,
because NBR 6023 governs the reference list only. Do not confuse the two when explaining case.

| ID | Tier | Rule | Sources | Fix |
|---|---|---|---|---|
| REF-01 | C | Centered bold heading; single-spaced, left-aligned, separated by one blank single-spaced line; alphabetical in author-date works, one list | NBR6023 §6.3, §6.7, §9.1; NBR14724 §5.2; MAN p. 46 | auto |
| REF-02 | C | Person: last surname in capitals, then given names, abbreviated or not, as in the document; `;` between authors | NBR6023 §8.1.1 | auto |
| REF-03 | C | Institutional author in capitals, in full or abbreviated as it is known. The text says "forma conhecida"; capitals come from every example, and both accepted files do it | NBR6023 §8.1.2; ACEITO; ACEITO2 | auto |
| REF-04 | A | Given names uniform across the list. The norm allows either form; the manual asks for initials; P1 mixed them | NBR6023 §8.1.1; MAN p. 46-47; ACEITO | auto |
| REF-05 | C | Up to 3 authors: list all. From 4: listing all is advised, *et al.* allowed | NBR6023 §8.1.1.1, §8.1.1.2 | auto |
| REF-06 | C | One emphasis (bold, italic or underline) for titles, in every entry. For articles it falls on the journal title | NBR6023 §6.7, §7.7.5; MAN p. 46 | auto |
| REF-07 | C | One punctuation style; the same complementary elements for all entries of a type | NBR6023 §6.4, §6.8 | auto |
| REF-08 | C | Online document: `Disponível em:` and `Acesso em:`, as the last elements. Access date has day, month and year in every example | NBR6023 §6.6, §8.13 | aluno |
| REF-09 | C | Article: authors, title, journal, place, volume, number, pages, date; add DOI if it has one | NBR6023 §7.7.5, §7.7.6 | aluno |
| REF-10 | A | Conference paper: `In:`, event name in capitals, number, year, city, `Anais [...]`, then place, publisher, date, pages. All three works use mixed-case event names, P2 less so | NBR6023 §7.8.4.1, §8.1.3; ACEITO; ACEITO2 | auto when data is present |
| REF-11 | C | Thesis: author, title, deposit year, type, degree and course in parentheses, institution, place, defense date | NBR6023 §7.1.2 | aluno |
| REF-12 | C | Unknown place or publisher: `[S. l.]`, `[s. n.]`, `[S. l.: s. n.]`. No year found: give one in brackets, like `[2021?]` | NBR6023 §8.4.4, §8.5.5, §8.5.6, §8.6.1.3 | aluno |
| REF-13 | C | Unknown author: enter by title, first word in capitals. "Anônimo" and "Autor desconhecido" are not allowed | NBR6023 §8.1.4, §8.2.1 | auto |
| REF-14 | C | Months abbreviated per Anexo A, in the publication's language; page ranges as `p. 31-40` | NBR6023 §8.6.2, §8.7.2.4 | auto |
| REF-15 | C | Software and databases: author, title, version, place, date, medium | NBR6023 §7.20 | aluno |
| REF-16 | C | Laws and regulations: jurisdiction in capitals, type, number, date, ementa, publication data | NBR6023 §7.11.1, §7.11.5 | aluno |
| REF-18 | A | `In:` and *et al.* in italics in the reference list. The manual asks it; check what the template's .bst does before changing | MAN p. 49 | auto, if asked |
| REF-17 | C | No corrupted entries: duplicate punctuation, lost letters, empty `Disponível em` | NBR6023 §6.4, §6.5 | auto when the fix is unambiguous |

Data comes from the document itself; anything from elsewhere goes in brackets (§4). So do not fill
gaps from memory or by guessing: if a field is missing, leave it for the student.
