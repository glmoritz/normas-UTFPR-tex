# LaTeX settings by template

Check the settings first. One wrong option can explain dozens of findings, and fixing the
cause is safer than editing each occurrence. `scripts/check_tex.py` reports these values.

**Students should start from the PPGSE template**, the `ppgse-cc` branch of
https://github.com/gbrante/normas-UTFPR-tex. It is maintained, and it produced accepted precedent P2.
`utfpr-thesis` (P1) is a second accepted reference. Compare settings against both.

| Topic | Accepted reference | What to look for elsewhere |
|---|---|---|
| Citation case | Template: uppercase. `utfpr-thesis`: `\renewcommand*{\mkbibnamefamily}[1]{#1}` | Mixed forms inside one document |
| et al. | Template: `abnt-etal-cite=2`. `utfpr-thesis`: from 4 authors | Inconsistent use |
| Call system | `style=abnt`, author-date | Numeric styles |
| Source lines | `\SourceOrNote{...}` under each float | Floats with no source command |
| PDF/A | Converted after compiling | Unconverted final PDF |
| License | Set on the rosto | Commented-out license command |
| Approval sheet | `\includepdf[pages=1]{...FolhaAprovacao.pdf}` | Generated or commented-out sheet |

## normas-utf-tex, PPGSE branch `ppgse-cc` (recommended start)

Same class family as older copies, updated to May 2026. Compared with an older copy it adds:
- `\programaSigla`, `\instituicaoSigla`, and one `\licenca...` option per CC license
- `\includepdf{folhaaprovacao.pdf}` active, with a placeholder sheet
- natureza wording matching the library model, with the degree as "Mestre em Engenharia Elétrica"
- keywords separated by `;`
- `\MakeUppercase` in `abnt-alf.bst`, which handles accented names properly
- automatic ordering of acronyms

Moving an existing project is not drop-in. Replacing only `normas-utf-tex.cls`, `abnt.cls` and
`abnt-alf.bst` stops on undefined `\ABNTsubsubsubsectionfont` and `\ABNTsubsubsubsectionfontsize`.
Its `.eps` license icons appear as file paths under pdflatex: use `latex` plus conversion as in
its `.bat` files, or convert the icons to PDF. Test any migration in a copy.

`\extraPages` adds to the page count before the Introduction. Leave it at 0 unless the count
is measurably wrong, and fix the cause first.

## normas-utf-tex, older copies (with abntcite and abnt-alf.bst)

| Setting | Problem | Fix |
|---|---|---|
| `\setcounter{page}{N}` before the lists | Breaks the page count (PAG-01, PAG-02) | Delete it and compile |
| `\includepdf` for annexes | Pages have no number (PAG-03) | Add `pagecommand={\thispagestyle{plainheader}}` |
| `abnt-etal-cite=2` | Same as the template and P2, so advice only. `3` follows the norm | Change only if asked |
| `\fonte{...}` | May never be used, and it is `flushleft` in older copies | Add it to each float. Use `center` in `\fonte` and `\@makecaption`, as in the current template. After a `tabular`, add `\vspace{8pt}` first, or the source collides with the bottom rule |
| `\capa`, `\folhaderosto` | Older copies lack bold and have only one license | Port the whole block from the template, keeping `.pdf` icons under pdflatex |
| License block | Two minipages at 0.25 and 0.75 stack if a line break separates them | Add `%` right after the first `\end{minipage}` |
| Advisors on the rosto | Accepted work writes "Prof. Dr." | `\orientador{Prof. Dr. Nome}` |
| `\includepdf` for the sheet | Often commented out | Uncomment once the student has the PDF |
| `pdfx` | Too slow on Overleaf | Leave it off. Add `pdfa` to the hyperref options, then run `scripts/make_pdfa.sh`, which also validates with veraPDF |
| License other than NC-ND | Older class has only `\licencaCCBYNCND` | Copy the block from the template and use icons converted to PDF with `epstopdf` |
| `resumo` and `abstract` environments | Print the work's reference (`\UTFPRcitadata ... \pageref{LastPage} f. ...`) above the text. The library returns this (RES-06). The current `ppgse-cc` branch still has it | Delete that line in both environments of the class |
| `\palavraschave`, `\keywords` | Older copies separate with periods; advice only, since P2 passed that way | Use `;` and end with `.` |

## utfpr.cls (DACOM, linked from the library page)

- `utfpr.cls` v2.0 (2021) on abnTeX2, with `abntex2-alf.bst`
- Compiles only with TeX Live 2021 on Overleaf, per its readme
- Has native PDF/A options since its version 2.4
- Example text mixes editions (NBR 10520:2023 and NBR 14724:2011). Do not treat it as a norm source.
- Its maintainers state they are not ABNT specialists.

## utfpr-thesis (Lima, unofficial)

- Built on `memoir` with biblatex-abnt. Current options sit commented in `\usepackage[...]{utfpr-thesis}`.
- Defaults: Arial, author-date, `Version=Final`.
- Already applies NBR 10520:2023 name case and *et al.* formatting.
- If no compiled result is available, build with `latexmk -norc -pdf -no-shell-escape`.
