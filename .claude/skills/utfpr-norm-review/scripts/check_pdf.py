#!/usr/bin/env python3
"""Measure a thesis PDF against UTFPR norm rules. Prints JSON. Needs poppler-utils.

Usage: check_pdf.py FILE.pdf [--first-text-page N] [--last-text-page N]

Every value here is a measurement or a heuristic hint for review, not a verdict.
"""
import argparse, collections, html, json, os, re, subprocess, sys


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


UP = r"[A-ZÀ-Ý]"
LOW = r"[a-zà-ÿ]"
SURNAME_UP = rf"{UP}{{3,}}(?:[ -]{UP}{{2,}})*"
SURNAME_MIX = rf"{UP}{LOW}+(?:[ -]{UP}?{LOW}+)*"
YEAR = r"(?:\d{4}[a-z]?|\[\d{2,4}-*\??\]|s\. ?d\.)"


def citations(text):
    text = re.sub(r"-\n\s*", "", text)
    flat = re.sub(r"\s+", " ", text)
    calls = re.findall(r"\(([^()]{3,120}?,\s*" + YEAR + r"(?:[^()]{0,60})?)\)", flat)
    upper, mixed = [], []
    for call in calls:
        for part in call.split(";"):
            part = part.strip()
            if re.match(rf"^{SURNAME_UP}(?: et al\.)?,", part):
                upper.append(call)
                break
            if re.match(rf"^{SURNAME_MIX}(?: et al\.)?,", part):
                mixed.append(call)
                break
    return {
        "upper_count": len(upper),
        "mixed_count": len(mixed),
        "upper_samples": [c for c, _ in collections.Counter(upper).most_common(6)],
        "mixed_samples": [c for c, _ in collections.Counter(mixed).most_common(6)],
        "note": "Short all-caps names may be acronyms, which stay uppercase (IEEE, IBGE).",
    }


def keywords(text):
    out = []
    for label in ("Palavras-chave", "Keywords"):
        m = re.search(rf"{label}\s*:\s*(.+?)(?:\n\s*\n|\f|$)", text, flags=re.S)
        if not m:
            out.append({"label": label, "found": False})
            continue
        value = re.sub(r"\s+", " ", m.group(1)).strip()
        items = [i.strip() for i in value.rstrip(".").split(";")]
        dotted = len(re.findall(r"\. +" + UP, value))
        out.append({
            "label": label, "found": True, "value": value[:220],
            "semicolons": value.count(";"), "ends_with_period": value.endswith("."),
            "looks_period_separated": dotted >= 2 and ";" not in value,
            "capitalized_items": sum(1 for i in items if i[:1].isupper()),
        })
    return out


def abstract_words(pdf, pages):
    out = {}
    for page in range(1, min(pages, 25) + 1):
        body = run("pdftotext", "-f", str(page), "-l", str(page), pdf, "-")
        for label, name in (("RESUMO", "resumo"), ("ABSTRACT", "abstract")):
            if re.match(rf"\s*{label}\s*\n", body) and name not in out:
                head = re.split(r"(?:Palavras-chave|Keywords)\s*:", body)[0]
                out[name] = {
                    "page": page,
                    "words": len(head.split()) - 1,
                    "paragraphs": len([p for p in re.split(r"\n\s*\n", head) if p.strip()]) - 1,
                }
    return out


def layout(pdf, first, last):
    xml = run("pdftohtml", "-xml", "-stdout", "-i", "-f", str(first), "-l", str(last), pdf)
    fonts = {i: (int(s), f.split("+")[-1]) for i, s, f in re.findall(
        r'<fontspec id="(\d+)" size="(-?\d+)" family="([^"]+)"', xml)}
    body, pageno, caption, left, right = (collections.Counter() for _ in range(5))
    sources = []
    source_align = collections.Counter()
    pages = re.findall(r'<page [^>]*height="(\d+)" width="(\d+)"[^>]*>(.*?)</page>', xml, flags=re.S)
    for h, w, content in pages:
        h, w = int(h), int(w)
        cm_x, cm_y = 21.0 / w, 29.7 / h
        for top, lft, wid, _, font, raw in re.findall(
                r'<text top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)" font="(\d+)">(.*?)</text>',
                content, flags=re.S):
            text = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
            top, lft, wid = int(top), int(lft), int(wid)
            size, family = fonts.get(font, (0, "?"))
            if top * cm_y < 3 and re.fullmatch(r"\d{1,3}", text):
                pageno[(family, round(top * cm_y, 1), round((w - lft - wid) * cm_x, 1))] += 1
            elif re.match(r"(Figura|Figure|Tabela|Table|Quadro|Gráfico) \d+", text) and ". ." not in text:
                caption[family] += 1
            elif re.match(r"(Fonte|Source)\s*:", text):
                sources.append(text[:70])
                mid = (w * 3 / 21 + w * 19 / 21) / 2
                source_align["centered" if abs(lft + wid / 2 - mid) < 7 * w / 595 else "left" if lft * cm_x < 3.3 else "other"] += 1
            else:
                body[family] += len(text)
                if len(text) > 70:
                    left[round(lft * cm_x, 1)] += 1
                    right[round((w - lft - wid) * cm_x, 1)] += 1
    return {
        "pages_scanned": [first, last],
        "body_fonts": body.most_common(4),
        "page_number": [{"font": k[0], "top_cm": k[1], "right_cm": k[2], "n": n}
                        for k, n in pageno.most_common(3)],
        "caption_fonts": caption.most_common(3),
        "captions_in_text": sum(caption.values()),
        "source_lines": len(sources),
        "source_alignment": dict(source_align),
        "source_forms": collections.Counter(
            re.sub(r"\d{4}", "AAAA", s)[:34] for s in sources).most_common(6),
        "left_margin_cm": left.most_common(3),
        "right_margin_cm": right.most_common(3),
    }


def pagination(pdf, pages, text):
    """Printed numbers against PDF pages. Rules PAG-01 to PAG-04."""
    sheets = text.split("\f")
    printed = []
    for sheet in sheets[:pages]:
        lines = [l for l in sheet.splitlines() if l.strip()]
        printed.append(int(lines[0]) if lines and re.fullmatch(r"\s*\d{1,4}\s*", lines[0]) else None)
    first = next((i + 1 for i, n in enumerate(printed) if n), None)
    if not first:
        return {"first_numbered_pdf_page": None, "problem": "No printed page numbers found."}
    offset = first - printed[first - 1]
    missing = [i + 1 for i, n in enumerate(printed) if i + 1 > first and n is None]
    breaks = [(i + 1, n) for i, n in enumerate(printed) if n and i + 1 - n != offset]
    toc, wrong = [], []
    for sheet in sheets[:first]:
        for line in sheet.splitlines():
            m = re.match(r"\s*(\d(?:\.\d+)*\s+\S.*?|REFER\S+|AP[ÊE]ND\S+.*?|ANEXO.*?)\s*[. ]{3,}\s*(\d+)\s*$", line)
            if m:
                toc.append((re.sub(r"\s+", " ", m.group(1)), int(m.group(2))))
    for title, number in toc:
        page = number + offset
        key = re.sub(r"^\d(\.\d+)*\s+", "", title)[:14].lower()
        if not 1 <= page <= pages or key not in re.sub(r"\s+", " ", sheets[page - 1]).lower():
            wrong.append([title[:50], number])
    stated = re.search(r"\b(\d{2,4})\s+f\.", " ".join(sheets[:8]))
    stated = int(stated.group(1)) if stated else None
    return {
        "stated_sheets_in_abstract_reference": stated,
        "stated_sheets_ok": None if stated is None else stated == pages - 1,
        "pdf_pages": pages,
        "first_numbered_pdf_page": first,
        "first_printed_number": printed[first - 1],
        "offset_pdf_minus_printed": offset,
        "offset_ok": offset == 1,
        "pages_without_number": missing[:30],
        "offset_breaks": breaks[:12],
        "last_page_numbered": printed[-1] is not None if printed else False,
        "toc_entries": len(toc),
        "toc_entries_not_on_stated_page": wrong[:12],
        "note": "Accepted works and the template have offset 1: cover not counted, rosto is sheet 1. "
                "A TOC mismatch can come from a long title broken across lines; open the page to confirm.",
    }


def filename_check(path):
    stem, _ = os.path.splitext(os.path.basename(path))
    return {
        "name": os.path.basename(path),
        "lowercase_alnum_only": bool(re.fullmatch(r"[a-z0-9]+(_produto)?", stem)),
        "note": "Confirm by hand: up to 4 significant title words, no articles or prepositions.",
    }


def corrupted_refs(text):
    idx = [m.start() for m in re.finditer(r"^\s*REFER[ÊE]NCIAS\s*$|^\s*REFERENCES\s*$", text, flags=re.M)]
    refs = text[idx[-1]:] if idx else ""
    return {
        "section_found": bool(refs),
        "double_punct": re.findall(r".{0,28}(?:\.\.|::|,,|,\.|\s;)\s.{0,12}", refs)[:8],
        "empty_available_at": len(re.findall(r"Dispon[ií]vel em:\s*\.", refs)),
        "lowercase_initials": re.findall(rf"{UP}{{3,}}, (?![vnp]\.)[a-z][.,;]", refs)[:8],
        "not_uppercase_author_lines": [
            l.strip()[:80] for l in refs.splitlines()
            if re.match(rf"^{UP}{LOW}+ .+\(({UP}{{2,}})\)\.", l.strip())][:8],
    }


def reference_entries(text):
    """Split the reference list and test each entry. NBR 6023:2018, Sections 6 to 9."""
    idx = [m.end() for m in re.finditer(r"^\s*REFER[ÊE]NCIAS\s*$|^\s*REFERENCES\s*$", text, flags=re.M)]
    if not idx:
        return {"entries": 0}
    refs = text[idx[-1]:]
    stop = re.search(r"^\s*(AP[ÊE]NDICE|ANEXO|APPENDIX|ANNEX)\b", refs, flags=re.M)
    refs = refs[:stop.start()] if stop else refs
    refs = re.sub(r"^\s*\d{1,3}\s*$", "", refs.replace("\f", "\n"), flags=re.M)
    raw = [re.sub(r"\s+", " ", e).strip() for e in re.split(r"\n\s*\n", refs)]
    entries, current = [], ""
    for chunk in raw:
        if not chunk:
            continue
        starts_new = re.match(rf"^[{UP[1:-1]}\[]", chunk) and re.match(rf"^[{UP[1:-1]}][^ ]*[ ,.]", chunk)
        if current and not starts_new:
            current += " " + chunk
        else:
            if current:
                entries.append(current)
            current = chunk
    if current:
        entries.append(current)
    lead = lambda e: e.split(",")[0].split(".")[0]
    not_upper = [e[:75] for e in entries if not re.match(rf"^{UP}{{2,}}", e)]
    url_no_access = [e[:75] for e in entries if re.search(r"https?://|www\.", re.sub(r"DOI: *https?://\S+( \S+)?", "", e)) and not re.search(r"Acesso em|Visited on|Accessed", e)]
    no_year = [e[:75] for e in entries if not re.search(r"\b(19|20)\d{2}\b|\[\d", e)]
    event_mixed = [e[:75] for e in entries if re.search(rf"\bIn: (?:\d|{UP}{LOW})", e)]
    full, initials = 0, 0
    for e in entries:
        m = re.match(rf"^{UP}[^,]*, (\S+)", e)
        if m:
            if re.fullmatch(rf"{UP}\.", m.group(1).rstrip(";,")):
                initials += 1
            else:
                full += 1
    keys = [re.sub(r"[^a-z0-9 ]", "", html.unescape(lead(e)).lower().translate(str.maketrans("áàâãäéêëíïóôõöúüç", "aaaaaeeeiioooouuc"))) for e in entries]
    misordered = [entries[i][:60] for i in range(1, len(keys)) if keys[i] < keys[i - 1]]
    return {
        "entries": len(entries),
        "not_starting_uppercase": {"n": len(not_upper), "samples": not_upper[:6]},
        "url_without_access_date": {"n": len(url_no_access), "samples": url_no_access[:6]},
        "no_year": {"n": len(no_year), "samples": no_year[:6]},
        "event_or_container_not_uppercase_after_In": {"n": len(event_mixed), "samples": event_mixed[:6]},
        "given_names": {"initials": initials, "full": full},
        "out_of_alphabetical_order": {"n": len(misordered), "samples": misordered[:6]},
        "note": "Splitting is heuristic. A book chapter after In: starts with an author, so check samples.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--first-text-page", type=int)
    ap.add_argument("--last-text-page", type=int)
    a = ap.parse_args()
    info = run("pdfinfo", a.pdf)
    meta = run("pdfinfo", "-meta", a.pdf)
    get = lambda k: (re.search(rf"^{k}:[ \t]*(.*)$", info, flags=re.M) or [None, ""])[1].strip()
    pages = int(get("Pages") or 0)
    text = run("pdftotext", "-layout", a.pdf, "-")
    page_data = pagination(a.pdf, pages, text)
    first = a.first_text_page or page_data["first_numbered_pdf_page"] or 1
    last = a.last_text_page or pages
    pdfa = re.search(r"pdfaid:part=['\"](\d)['\"][^>]*pdfaid:conformance=['\"](\w)['\"]", meta)
    pdfa = pdfa or re.search(r"<pdfaid:part>(\d)</pdfaid:part>.*?<pdfaid:conformance>(\w)<", meta, flags=re.S)
    fonts = sorted({re.sub(r"^[A-Z]{6}\+", "", l.split()[0]) for l in run("pdffonts", a.pdf).splitlines()[2:] if l.split()})
    json.dump({
        "file": filename_check(a.pdf),
        "size_mb": round(os.path.getsize(a.pdf) / 1048576, 2),
        "pages": pages,
        "first_text_page": first,
        "page_size": get("Page size"),
        "properties": {"title": get("Title"), "author": get("Author"), "keywords": get("Keywords")},
        "pdfa_declared": f"PDF/A-{pdfa.group(1)}{pdfa.group(2).lower()}" if pdfa else None,
        "pdfa_note": "This reads the file's claim only. Validate the final file with a real validator.",
        "font_families": fonts,
        "keywords": keywords(text),
        "abstracts": abstract_words(a.pdf, pages),
        "pagination": page_data,
        "citations": citations(text),
        "layout": layout(a.pdf, first, last),
        "references": corrupted_refs(text),
        "reference_entries": reference_entries(text),
        "mentions": {k: len(re.findall(k, text, flags=re.I)) for k in
                     ("LABIC", "CNPq", "CAPES", "Fundação Araucária", "Creative Commons", "Data de aprovação")},
    }, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
