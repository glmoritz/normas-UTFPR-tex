#!/usr/bin/env python3
"""Build the student/advisor HTML report from a findings JSON file.

Usage: build_report.py FINDINGS.json OUTPUT.html [--root PROJECT_DIR] [--allow-unlisted] [--fragment]

Layout: what is still open comes first, in a plain numbered list. What was resolved comes after.
With --root it checks the change log against the files: every "depois" must be in its file,
removed text must be gone, and every git-modified file must be listed.
"""
import argparse, html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TIERS = {"B": ("d1", "Bloqueia o depósito"), "C": ("d2", "Corrigir"), "A": ("d3", "Recomendação")}
OPEN = ("aluno", "orientador", "confirmar", "proposto")
WHO = {"aluno": "Aluno", "orientador": "Orientador", "confirmar": "Aluno confere", "proposto": "Aprovar correção"}
esc = html.escape


def source_link(ref, sources):
    entry = sources.get(ref["id"])
    if not entry:
        sys.exit(f"Unknown source id: {ref['id']}")
    detail = ref.get("detalhe", "")
    url = entry["url"]
    if entry.get("paginado") and ref.get("pagina"):
        url += f"#page={ref['pagina']}"
        detail = detail or f"p. {ref['pagina']}"
    text = esc(entry["label"]) + (f", {esc(detail)}" if detail else "")
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{text}</a>'


def links(refs, sources):
    return "<br>".join(source_link(r, sources) for r in refs)


def verify(changes, root, allow_unlisted):
    problems, listed = [], set()
    for c in changes:
        path = os.path.join(root, c["arquivo"])
        listed.add(os.path.normpath(c["arquivo"]))
        if not os.path.exists(path):
            problems.append(f"Missing file: {c['arquivo']}")
            continue
        with open(path, encoding="utf8", errors="replace") as f:
            content = f.read()
        if c.get("depois") and c["depois"] not in content:
            problems.append(f"{c['arquivo']}: 'depois' text not found: {c['depois'][:70]}")
        if not c.get("depois") and c.get("antes") and c["antes"] in content:
            problems.append(f"{c['arquivo']}: removed text is still there: {c['antes'][:70]}")
    out = subprocess.run(["git", "-C", root, "-c", "core.quotepath=off", "diff", "--name-only", "HEAD"],
                         capture_output=True, text=True)
    if out.returncode == 0 and not allow_unlisted:
        for name in out.stdout.splitlines():
            if os.path.normpath(name) not in listed:
                problems.append(f"Changed in git but not in the report: {name}")
    return problems


def is_process(f):
    return f["id"].startswith("PRO-")


def verdict(findings):
    """Computed from the findings, so wording cannot soften it. PRO- items do not count."""
    doc = [f for f in findings if not is_process(f) and f["status"] in OPEN]
    hard = [f for f in doc if f["tier"] == "B" and f["status"] != "confirmar"]
    if hard:
        return "rej", "Rejeitado", f"{len(hard)} item(ns) ainda impedem o depósito."
    if doc:
        return "res", "Falta só conferir", "Tudo o que dava para resolver já foi feito. Falta a conferência abaixo."
    return "apr", "Aprovado", "Nenhuma pendência nesta revisão."


def pending_block(findings, sources):
    items = [f for f in findings if f["status"] in OPEN]
    items.sort(key=lambda f: (is_process(f), {"B": 0, "C": 1, "A": 2}[f["tier"]]))
    if not items:
        return '<p class="lead">Nenhuma pendência.</p>'
    rows = []
    for n, f in enumerate(items, 1):
        ref = links(f["fontes"], sources)
        rows.append(
            f'<li class="pend"><div class="num">{n}</div><div class="pbody">'
            f'<div class="what">{esc(f["acao"])}</div>'
            f'<div class="why">{esc(f["problema"])}</div>'
            f'<div class="meta"><span class="chip {f["status"]}">{WHO[f["status"]]}</span> {esc(f["local"])}'
            f'{" · " + ref if ref else ""}</div></div></li>')
    return f'<ol class="pends">{"".join(rows)}</ol>'


def table(findings, sources, show_reason=True):
    rows, group = [], None
    for f in sorted(findings, key=lambda x: x.get("grupo", "")):
        if f.get("grupo") != group:
            group = f.get("grupo")
            rows.append(f'<tr class="group"><td colspan="4">{esc(group or "")}</td></tr>')
        dot = TIERS[f["tier"]][0]
        rows.append(
            f'<tr><td class="pg"><span class="dot {dot}"></span>{esc(f["local"])}<small>{esc(f["id"])}</small></td>'
            f'<td class="vi">{esc(f["problema"])}</td><td class="ac">{esc(f["acao"])}</td>'
            f'<td class="no">{links(f["fontes"], sources)}</td></tr>')
    return ('<div class="scroller"><table><thead><tr><th>Local</th><th>O que era</th><th>O que foi feito</th>'
            f'<th>Referência</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def change_table(changes, sources):
    rows = []
    for c in changes:
        rows.append(
            f'<tr><td class="pg">{esc(c["arquivo"])}</td>'
            f'<td class="ch a">{esc(c.get("antes", "")) or "(novo)"}</td>'
            f'<td class="ch d">{esc(c.get("depois", "")) or "(removido)"}</td>'
            f'<td class="vi">{esc(c["motivo"])}</td>'
            f'<td class="no">{links(c["fontes"], sources)}</td></tr>')
    return ('<div class="scroller"><table><thead><tr><th>Arquivo</th><th>Antes</th><th>Depois</th><th>Por quê</th>'
            f'<th>Referência</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def source_notes(used, sources):
    return "".join(
        f'<dt><a href="{esc(sources[k]["url"])}" target="_blank" rel="noopener">{esc(sources[k]["label"])}</a></dt>'
        f'<dd>Acesso: {esc(sources[k]["acesso"])}. Consulta nesta revisão: {esc(sources[k]["lido"])}.</dd>'
        for k in sorted(used))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("findings")
    ap.add_argument("output")
    ap.add_argument("--root")
    ap.add_argument("--allow-unlisted", action="store_true")
    ap.add_argument("--fragment", action="store_true", help="omit doctype/html/head/body, for Artifact publishing")
    a = ap.parse_args()
    with open(a.findings, encoding="utf8") as f:
        d = json.load(f)
    with open(os.path.join(HERE, "..", "references", "sources.json"), encoding="utf8") as f:
        sources = json.load(f)
    with open(os.path.join(HERE, "..", "assets", "report.css"), encoding="utf8") as f:
        css = f.read()
    findings, changes = d.get("findings", []), d.get("changes", [])
    missing = [f["id"] for f in findings if not f.get("porque", "").strip()]
    if missing:
        sys.exit("Report not built: findings without a reason (porque): " + ", ".join(missing))
    if a.root:
        problems = verify(changes, a.root, a.allow_unlisted)
        if problems:
            sys.exit("Report not built:\n  " + "\n  ".join(problems))
    v_class, v_label, v_text = verdict(findings)
    used = {r["id"] for x in findings + changes for r in x["fontes"]}
    n_open = sum(1 for f in findings if f["status"] in OPEN)
    done = [f for f in findings if f["status"] == "corrigido"]
    accepted = [f for f in findings if f["status"] == "aceito"]
    ok = "".join(f"<li>{esc(x)}</li>" for x in d.get("conforme", []))
    limits = "".join(f"<li>{esc(x)}</li>" for x in d.get("limites", []))
    title = esc(d.get("pagina", "Revisão de normas"))
    head = (f"<title>{title}</title><style>{css}</style>" if a.fragment else
            '<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f"<title>{title}</title><style>{css}</style></head>\n<body>")
    tail = "" if a.fragment else "</body></html>"
    accepted_block = (f'<h2 class="sec">Sem ação necessária ({len(accepted)})</h2>'
                      '<p class="lead">Diferem do texto da norma, mas seguem o modelo do PPGSE ou os trabalhos aceitos.</p>'
                      + table(accepted, sources)) if accepted else ""
    page = f"""{head}<div class="wrap">
<header>
  <div class="eyebrow">Revisão de normas UTFPR · {esc(d["data"])}</div>
  <h1>{esc(d["titulo"])}</h1>
  <p class="sub"><b>{esc(d["autor"])}</b> · Orientação: {esc(d["orientador"])}</p>
  <div class="verdict {v_class}"><b>{v_label}</b> {esc(v_text)}</div>
</header>
<h2 class="sec">Pendências ({n_open})</h2>
{pending_block(findings, sources)}
<h2 class="sec">Já resolvido ({len(done)})</h2>
<p class="lead">Nada a fazer aqui. Fica registrado o que estava errado e o que foi feito.</p>
{table(done, sources)}
{accepted_block}
<h2 class="sec">O que mudou nos arquivos ({len(changes)})</h2>
<p class="lead">Cada linha foi conferida nos arquivos do projeto.</p>
{change_table(changes, sources)}
{f'<h2 class="sec">Já estava conforme</h2><ul>{ok}</ul>' if ok else ''}
<section class="sources"><h2>Referências usadas</h2>
<p>As normas ABNT são consultadas pelo GEDWeb com a conta da UTFPR.</p>
<dl>{source_notes(used, sources)}</dl></section>
{f'<div class="note"><b>Limites desta revisão</b><ul>{limits}</ul></div>' if limits else ''}
<footer>{esc(d["resumo"])}</footer>
</div>{tail}
"""
    with open(a.output, "w", encoding="utf8") as f:
        f.write(page)
    print(f"Report written: {a.output} ({n_open} open, {len(done)} done, {len(accepted)} accepted, {len(changes)} changes)")


if __name__ == "__main__":
    main()
