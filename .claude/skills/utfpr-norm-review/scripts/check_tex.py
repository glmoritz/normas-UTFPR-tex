#!/usr/bin/env python3
"""Read a thesis LaTeX project and report norm-related settings. Prints JSON.

Usage: check_tex.py PROJECT_DIR

Reads files only; it never compiles or edits. Values are hints for review.
"""
import glob, json, os, re, sys


def read(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf8")
    except UnicodeDecodeError:  # the PPGSE template keeps .tex and .bib in ISO-8859-1
        return raw.decode("latin-1")


def strip_comments(tex):
    return re.sub(r"(?<!\\)%.*", "", tex)


def main_file(root):
    hits = [f for f in glob.glob(os.path.join(root, "*.tex"))
            if re.search(r"^\s*\\documentclass", read(f), flags=re.M)]
    hits.sort(key=lambda f: (os.path.basename(f) != "main.tex", f))
    return hits[0] if hits else None


def included(root, main):
    seen, order, queue = set(), [], [main]
    while queue:
        path = queue.pop(0)
        if path in seen or not os.path.exists(path):
            continue
        seen.add(path)
        order.append(path)
        for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", strip_comments(read(path))):
            name = name if name.endswith(".tex") else name + ".tex"
            queue.append(os.path.normpath(os.path.join(root, name)))
    return order


def detect_template(main_tex):
    cls = re.search(r"\\documentclass(?:\[[^\]]*\])?\{([^}]+)\}", main_tex)
    pkg = "utfpr-thesis" if "{utfpr-thesis}" in main_tex else None
    return pkg or (cls.group(1) if cls else None)


def bib_authors(root):
    entries = {}
    for path in glob.glob(os.path.join(root, "**", "*.bib"), recursive=True):
        base = os.path.basename(path)
        if base.startswith(("abnt-", "abntex", "iso-")):
            continue
        for key, author in re.findall(
                r"@\w+\s*\{\s*([^,\s]+)\s*,(?:(?!\n@).)*?\bauthor\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n",
                read(path), flags=re.S | re.I):
            entries[key] = len(re.split(r"\s+and\s+", author))
    return entries


def main():
    root = sys.argv[1]
    main = main_file(root)
    if not main:
        sys.exit("No main .tex file with \\documentclass found.")
    raw_main = read(main)
    live_main = strip_comments(raw_main)
    files = included(root, main)
    body = "\n".join(strip_comments(read(f)) for f in files)

    figures = len(re.findall(r"\\begin\{figure\*?\}", body))
    tables = len(re.findall(r"\\begin\{(?:table\*?|quadro|longtable)\}", body))
    source_cmds = re.findall(r"\\(?:fonte|SourceOrNote\*?|source|fonte[A-Z]\w*)\{", body)
    source_text = re.findall(r"Fonte\s*:|Source\s*:", body)
    cited = set()
    for group in re.findall(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}", body):
        cited.update(k.strip() for k in group.split(","))
    authors = bib_authors(root)
    in_commented = lambda pattern: bool(re.search(r"^\s*%.*" + pattern, raw_main, flags=re.M))
    in_live = lambda pattern: bool(re.search(pattern, live_main))
    prose = re.sub(r"\\(?:label|ref|input|include)\{[^}]*\}", "", body)

    json.dump({
        "main_file": main,
        "template": detect_template(raw_main),
        "files_read": [os.path.relpath(f, root) for f in files],
        "citation_setup": {
            "abntcite_options": (re.search(r"\\usepackage\[([^\]]*)\]\{abntcite\}", live_main) or [None, None])[1],
            "etal_cite": (re.search(r"abnt-etal-cite=(\d+)", live_main) or [None, None])[1],
            "biblatex": "biblatex" in live_main,
            "name_case_override": in_live(r"\\renewcommand\*?\{\\mkbibnamefamily\}"),
        },
        "pagination_setup": {
            "hard_coded_page_counter": re.findall(r"\\setcounter\{page\}\{\d+\}", body),
            "includepdf_without_pagecommand": sum(1 for m in re.findall(r"\\includepdf(\[[^\]]*\])?", body) if "pagecommand" not in m and "pages=-" in m),
            "uses_template_extra_pages": bool(re.search(r"\\extraPages", body)),
        },
        "floats": {
            "figures": figures, "tables": tables,
            "source_commands": len(source_cmds), "literal_source_text": len(source_text),
        },
        "bibliography": {
            "entries_with_authors": len(authors),
            "three_author_entries": sorted(k for k, n in authors.items() if n == 3),
            "cited_keys": len(cited),
            "cited_not_in_bib_with_authors": sorted(k for k in cited if k not in authors)[:40],
            "in_bib_not_cited": sorted(k for k in authors if k not in cited)[:40],
            "note": "Entries with no author field appear as cited-but-absent; confirm against the .bib.",
        },
        "pretextual": {
            "agradecimentos_active": in_live(r"\\begin\{agradecimentos\}|\\begin\{Acknowledgments\}") or bool(re.search(r"acknowledgments", live_main)),
            "approval_pdf_active": in_live(r"\\includepdf.*(?:provac|ata)|ApprovalPagePDF"),
            "approval_pdf_commented": in_commented(r"\\includepdf"),
            "license_active": in_live(r"\\licenca|License\{|CC-BY|\\ccby"),
            "license_commented": in_commented(r"\\licenca"),
            "pdfx_active": in_live(r"\\usepackage\[[^\]]*\]\{pdfx\}"),
            "keywords_pt": (re.search(r"\\palavraschave\{([^}]*)\}", live_main) or [None, None])[1],
            "keywords_en": (re.search(r"\\keywords\{([^}]*)\}", live_main) or [None, None])[1],
            "degree_text": (re.search(r"\\comentario\{([^\n]*)\}", live_main) or [None, None])[1],
            "program": (re.search(r"\\programa\{([^}]*)\}", live_main) or [None, None])[1],
            "year": (re.search(r"\\data\{([^}]*)\}", live_main) or [None, None])[1],
        },
        "wording": {
            "capitulo_uses": len(re.findall(r"\bcap[ií]tulos?\b|\bchapters?\b", prose, flags=re.I)),
            "itemize": body.count("\\begin{itemize}"),
            "enumerate": body.count("\\begin{enumerate}"),
            "labic": len(re.findall("LABIC", body)),
            "cnpq": len(re.findall("CNPq", body)),
        },
    }, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
