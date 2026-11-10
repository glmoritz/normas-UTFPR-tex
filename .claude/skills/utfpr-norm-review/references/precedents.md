# Accepted precedents

Documents that really passed library verification. They show how the rules are applied.
Follow what is used: practice outranks strict norm text
when choosing a tier, but never hides a rule: a tolerated deviation stays as advice.

Two documents are still thin evidence. Add each newly confirmed deposit here and re-rank.
P2 weighs more for PPGSE work: same program, recent, and built on the recommended template.

## How to add a precedent

1. Find the record: `https://repositorio.utfpr.edu.br/jspui/simple-search?query=<words>`.
2. Download the deposited PDF. A repo's own compiled PDF may be stale, as it was for this one.
3. Run `scripts/check_pdf.py` on it and record the differences below.
4. If the LaTeX source is available, add its settings to `latex-templates.md`.

## P1: dissertação CPGEI (2025)

- Record: https://repositorio.utfpr.edu.br/jspui/handle/1/36171, file `aoasubsetsampling.pdf`
- CPGEI, master's, defended 27/02/2025. 44 pages. Text in English.
- Built on the unofficial template `utfpr-thesis` v1.8.
- Advisor confirmed it passed library verification.

Followed:
- PDF/A-2b, made with PDF24 and Ghostscript after compiling
- Three-word file name
- 23 mixed-case citations, 0 uppercase; `(He; Long; Zhang, 2021b)` written out
- Source line under figures: `Source: own authorship (2024)`, `Source: (MathWorks, 2024)`
- System-issued approval sheet inserted as page 4, no signatures
- CC BY 4.0 note at the rosto foot; Portuguese title translation
- Keywords separated by `;`, ending in `.`
- Margins 3 cm left, 2 cm right; 12 pt body; 10 pt page numbers at top right
- Sans typeface (Latin Modern Sans)

Tolerated, so treat as advice:
- "Chapter" used in the text
- Bullets for objectives instead of alíneas
- Capitalized keywords
- No ficha catalográfica
- Full given names in some references
- Abbreviations (IoT) in the abstract
- Blank title, author and keywords in document properties

Not a precedent:
- Cover year 2024 with a February 2025 defense
- Agradecimentos without funding: it may simply have had none

## P2: dissertação PPGSE (2026)

- Record: https://repositorio.utfpr.edu.br/jspui/handle/1/40437, file `impactosveiculossistemasdistribuicao.pdf`
- An advisor confirmed it passed library verification.
- PPGSE, master's, defended 13/03/2026. 144 pages. Text in Portuguese.
- Built on the `ppgse-cc` template.

Followed:
- PDF/A-1b, converted with iLovePDF after compiling; descriptive file name
- Rosto: English title, "Mestre em Engenharia Elétrica", CC BY-NC-SA footer
- System-issued approval sheet as page 3, no signatures
- Pagination: printed number is PDF page minus 1, numbered to the last page, including annexes
- Source line under figures and tables: 102 lines for 109 detected captions (the count includes list-of-figures noise)
- Margins 3 cm left, 2 cm right; 12 pt serif body; 10 pt page numbers at top right
- Properties filled in

Tolerated, so treat as advice:
- 104 uppercase citations, 0 mixed case
- *et al.* for three authors (5 references)
- Keywords separated by periods, in title case
- The work's reference above the resumo and abstract (`143 f.`). No longer tolerated: the library
  returned a PPGSE dissertation for it in Nov 2026. See RES-06
- "Fonte: Autoria própria." with no year; 2 variants in capitalization
- 36 bullets, "capítulo" in the text
- No ficha catalográfica
