#!/usr/bin/env python3
"""
Side-by-side review sheet for the hypothesis system: every fill-in-the-blank
template, its verb bank and every token word, English against French.

This is the part of the patch that cannot be proof-read by reading the French
alone. The sentence is shown to the player *while they are still guessing*, so
it has to hold together with wrong answers in the slots as well as right ones,
and the slot sequence is addressed positionally by the game — it can never be
reordered. Both of those are checked here.

Regenerate with:  python3 tools/hypothesis_review.py
"""
import importlib.util, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load(mod):
    spec = importlib.util.spec_from_file_location(mod, ROOT / "tools" / f"{mod}.py")
    m = importlib.util.module_from_spec(spec); sys.modules[mod] = m
    spec.loader.exec_module(m); return m

fr = load("fr_hypotheses")
pools = json.loads((ROOT / "corpus/en/pools.json").read_text(encoding="utf-8"))["hypotheses"]

def slots(s):
    return "".join(re.findall(r"\[([vr])\]", s or ""))

out = []
w = out.append
w("# Relecture — système d’hypothèses\n")
w("Anglais et français côte à côte. Régénérer avec `python3 tools/hypothesis_review.py`.\n")
w("## Ce qu’il faut vérifier\n")
w("La phrase s’affiche **pendant** que le joueur cherche : elle doit rester lisible")
w("avec n’importe quelle combinaison, y compris fausse. Les règles dures")
w("(`docs/HYPOTHESES.md`) : séquence de trous intouchable, l’article appartient au")
w("jeton et non au gabarit, jamais `de [r]` ni `à [r]`, aucune élision devant un")
w("trou, aucun accord avec un trou.\n")
w("---\n")
w("## Gabarits\n")

bad = 0
for h in sorted(pools, key=lambda x: x["name"]):
    name, t = h["name"], h["template"]
    en = t.get("hypothesisSentence", "")
    if not en:
        continue
    entry = fr.TEMPLATES.get(name) or {}
    fr_s = entry.get("h", "") if isinstance(entry, dict) else str(entry)
    same = slots(en) == slots(fr_s)
    if not same:
        bad += 1
    w(f"### {h.get('questTitle') or name}")
    w(f"`{name}` — trous `{slots(en)}` " + ("✅" if same else f"❌ FR = `{slots(fr_s)}`") + "\n")
    w(f"| | |\n|---|---|")
    w(f"| **EN** | {en} |")
    w(f"| **FR** | {fr_s or '—'} |")
    en_v = [x.strip() for x in (t.get("verbs") or "").split(",") if x.strip()]
    fr_v = [x.strip() for x in (fr.VERBS.get(name) or "").split(",") if x.strip()]
    if en_v:
        w("\n**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)\n")
        w("| EN | FR |\n|---|---|")
        for i, e in enumerate(en_v):
            w(f"| {e} | {fr_v[i] if i < len(fr_v) else '—'} |")
    w("")

w("---\n")
w(f"## Mots-jetons ({len(fr.TOKENS)})\n")
w("Ils remplissent les trous `[r]`. Chacun **porte son déterminant**, puisque le")
w("gabarit ne peut pas savoir quel genre ni quel nombre va tomber dans le trou.\n")
w("| EN | FR |\n|---|---|")
for en_t in sorted(fr.TOKENS, key=str.lower):
    w(f"| {en_t} | {fr.TOKENS[en_t]} |")

path = ROOT / "docs" / "RELECTURE-HYPOTHESES.md"
path.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"{len([h for h in pools if h['template'].get('hypothesisSentence')])} gabarits, "
      f"{len(fr.TOKENS)} mots-jetons -> {path.relative_to(ROOT)}")
print("séquences de trous divergentes :", bad)


# ---------------------------------------------------------------- HTML sheet
def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def chips(s):
    """Render [v]/[r] as coloured chips so the slot sequence is scannable."""
    out = esc(s)
    out = out.replace("[v]", '<b class="v">v</b>').replace("[r]", '<b class="r">r</b>')
    return out

rows = []
for h in sorted(pools, key=lambda x: x["name"]):
    name, t = h["name"], h["template"]
    en = t.get("hypothesisSentence", "")
    if not en:
        continue
    entry = fr.TEMPLATES.get(name) or {}
    fr_s = entry.get("h", "") if isinstance(entry, dict) else str(entry)
    rows.append({
        "title": h.get("questTitle") or name, "name": name,
        "en": en, "fr": fr_s, "sig": slots(en), "ok": slots(en) == slots(fr_s),
        "verbs": [(e.strip(), (list(x.strip() for x in (fr.VERBS.get(name) or "").split(","))
                               + [""] * 9)[i])
                  for i, e in enumerate(x.strip() for x in (t.get("verbs") or "").split(",")) if e.strip()],
    })

tok = [(k, fr.TOKENS[k]) for k in sorted(fr.TOKENS, key=str.lower)]
data = json.dumps({"rows": rows, "tokens": tok}, ensure_ascii=False)

cards = []
for r in rows:
    vb = "".join(
        f'<div class="vb"><span>{esc(e)}</span><span>{esc(f)}</span></div>' for e, f in r["verbs"])
    cards.append(f"""<article class="card">
  <header>
    <h3>{esc(r['title'])}</h3>
    <code class="tech">{esc(r['name'])}</code>
    <span class="sig {'ok' if r['ok'] else 'no'}">{''.join(f'<b class="{c}">{c}</b>' for c in r['sig'])}</span>
  </header>
  <div class="pair">
    <div class="side"><span class="lbl">EN</span><p class="tpl">{chips(r['en'])}</p></div>
    <div class="side fr"><span class="lbl">FR</span><p class="tpl">{chips(r['fr']) or '—'}</p></div>
  </div>
  {f'<div class="verbs"><span class="lbl">Banque de verbes</span>{vb}</div>' if vb else ''}
</article>""")

html = f"""<title>Relecture des hypothèses</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>
:root {{
  --paper:#FBF9F5; --surface:#FFFFFF; --ink:#1F1B16; --muted:#6B6257;
  --line:#E4DDD1; --amber:#B07A16; --v:#2F6F5B; --r:#8A4A7D; --okbg:#EDF3EF; --nobg:#F6E2E2;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --paper:#16130F; --surface:#1E1A15; --ink:#EDE6DA; --muted:#9E9384;
    --line:#332C23; --amber:#E0A93F; --v:#6FBFA3; --r:#D7A0CC; --okbg:#1B241F; --nobg:#2E1B1B;
  }}
}}
:root[data-theme="dark"] {{
  --paper:#16130F; --surface:#1E1A15; --ink:#EDE6DA; --muted:#9E9384;
  --line:#332C23; --amber:#E0A93F; --v:#6FBFA3; --r:#D7A0CC; --okbg:#1B241F; --nobg:#2E1B1B;
}}
*{{box-sizing:border-box}}
body{{background:var(--paper);color:var(--ink);font:400 16px/1.6 Spectral,Georgia,serif;margin:0}}
.wrap{{max-width:1080px;margin:0 auto;padding:48px 24px 96px}}
h1{{font-size:2.1rem;font-weight:600;margin:0 0 .3em;letter-spacing:-.01em;text-wrap:balance}}
.sub{{color:var(--muted);max-width:62ch;margin:0 0 32px}}
.stats{{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 40px}}
.stat{{background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:10px 14px;
  font:600 .8rem/1 'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums}}
.stat span{{display:block;font-weight:400;color:var(--muted);margin-top:5px;font-size:.72rem}}
.rules{{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--amber);
  border-radius:3px;padding:20px 24px;margin:0 0 48px}}
.rules h2{{font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;color:var(--amber);margin:0 0 12px}}
.rules ol{{margin:0;padding-left:1.2em;color:var(--muted)}}
.rules li{{margin:.35em 0}}
.rules b{{color:var(--ink);font-weight:600}}
h2.sec{{font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);
  border-bottom:1px solid var(--line);padding-bottom:8px;margin:0 0 24px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:20px 22px;margin:0 0 16px}}
.card header{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:14px}}
.card h3{{font-size:1.05rem;font-weight:600;margin:0}}
.tech{{font:400 .72rem 'IBM Plex Mono',monospace;color:var(--muted)}}
.sig{{margin-left:auto;display:flex;gap:3px;padding:3px 7px;border-radius:3px;background:var(--okbg)}}
.sig.no{{background:var(--nobg)}}
.sig b,.tpl b{{font:600 .7rem/1.5 'IBM Plex Mono',monospace;display:inline-block;
  min-width:1.2em;text-align:center;border-radius:2px;padding:1px 3px}}
b.v{{color:var(--v);background:color-mix(in srgb,var(--v) 14%,transparent)}}
b.r{{color:var(--r);background:color-mix(in srgb,var(--r) 14%,transparent)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:3px;overflow:hidden}}
.side{{padding:12px 14px;min-width:0}}
.side.fr{{border-left:1px solid var(--line)}}
.lbl{{display:block;font:600 .65rem/1 'IBM Plex Mono',monospace;letter-spacing:.1em;
  color:var(--muted);text-transform:uppercase;margin-bottom:7px}}
.tpl{{font:400 .86rem/1.75 'IBM Plex Mono',monospace;margin:0;overflow-wrap:anywhere}}
.verbs{{margin-top:14px}}
.vb{{display:grid;grid-template-columns:1fr 1fr;gap:12px;font:400 .8rem/1.7 'IBM Plex Mono',monospace;
  border-top:1px dotted var(--line);padding:2px 0}}
.vb span:first-child{{color:var(--muted)}}
.tools{{display:flex;gap:12px;align-items:center;margin:0 0 16px;flex-wrap:wrap}}
input[type=search]{{flex:1;min-width:220px;background:var(--surface);border:1px solid var(--line);
  border-radius:3px;padding:9px 12px;color:var(--ink);font:400 .85rem 'IBM Plex Mono',monospace}}
input[type=search]:focus-visible{{outline:2px solid var(--amber);outline-offset:1px}}
.count{{font:400 .78rem 'IBM Plex Mono',monospace;color:var(--muted);font-variant-numeric:tabular-nums}}
.tokwrap{{border:1px solid var(--line);border-radius:3px;overflow-x:auto;background:var(--surface)}}
table{{width:100%;border-collapse:collapse;font:400 .84rem/1.6 'IBM Plex Mono',monospace}}
th{{text-align:left;font:600 .65rem/1 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);padding:11px 14px;border-bottom:1px solid var(--line);
  position:sticky;top:0;background:var(--surface)}}
td{{padding:7px 14px;border-bottom:1px dotted var(--line);vertical-align:top}}
td:first-child{{color:var(--muted);width:44%}}
tr:last-child td{{border-bottom:0}}
@media (max-width:720px){{
  .pair,.vb{{grid-template-columns:1fr}}
  .side.fr{{border-left:0;border-top:1px solid var(--line)}}
  .sig{{margin-left:0}}
}}
</style>
<div class="wrap">
<h1>Relecture des hypothèses</h1>
<p class="sub">Les phrases à trous du manoir Blake, anglais contre français. Cette partie ne se
relit pas comme une traduction ordinaire : la phrase s’affiche <i>pendant</i> que le joueur cherche,
donc avec de mauvaises réponses dans les trous.</p>

<div class="stats">
  <div class="stat">{len(rows)}<span>gabarits</span></div>
  <div class="stat">{len(tok)}<span>mots-jetons</span></div>
  <div class="stat">{sum(len(r['verbs']) for r in rows)}<span>verbes</span></div>
  <div class="stat">{sum(1 for r in rows if r['ok'])}/{len(rows)}<span>séquences conformes</span></div>
</div>

<div class="rules">
  <h2>Les cinq règles dures</h2>
  <ol>
    <li><b>La séquence de trous est intouchable.</b> Le jeu les adresse par position : le français
        doit garder le même nombre, le même type et le même ordre.</li>
    <li><b>L’article appartient au jeton, pas au gabarit.</b> Le gabarit ignore le genre de ce qui
        va tomber dans le trou — chaque mot-jeton porte donc son déterminant.</li>
    <li><b>Jamais <code>de [r]</code> ni <code>à [r]</code>.</b> Ce sont les deux prépositions qui se
        contractent avec l’article.</li>
    <li><b>Aucune élision devant un trou.</b> Le gabarit ne peut pas choisir entre <i>que</i> et
        <i>qu’</i>, <i>le</i> et <i>l’</i>.</li>
    <li><b>Aucun accord avec un trou.</b> Les verbes sont à l’infinitif, forme invariable.</li>
  </ol>
</div>

<h2 class="sec">Gabarits</h2>
{''.join(cards)}

<h2 class="sec">Mots-jetons — ils remplissent les trous <b class="r">r</b></h2>
<div class="tools">
  <input type="search" id="q" placeholder="Filtrer les mots-jetons…" aria-label="Filtrer les mots-jetons">
  <span class="count" id="c">{len(tok)} entrées</span>
</div>
<div class="tokwrap">
  <table><thead><tr><th>Anglais</th><th>Français</th></tr></thead><tbody id="tb">
  {''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in tok)}
  </tbody></table>
</div>
</div>
<script>
const DATA = {data};
const tb = document.getElementById('tb'), q = document.getElementById('q'), c = document.getElementById('c');
q.addEventListener('input', () => {{
  const s = q.value.trim().toLowerCase();
  const hits = DATA.tokens.filter(([a, b]) => !s || a.toLowerCase().includes(s) || b.toLowerCase().includes(s));
  tb.innerHTML = hits.map(([a, b]) =>
    `<tr><td>${{a.replace(/&/g,'&amp;').replace(/</g,'&lt;')}}</td><td>${{b.replace(/&/g,'&amp;').replace(/</g,'&lt;')}}</td></tr>`).join('');
  c.textContent = hits.length + ' / ' + DATA.tokens.length + ' entrées';
}});
</script>"""

hp = ROOT / "docs" / "relecture-hypotheses.html"
hp.write_text(html, encoding="utf-8")
print(f"page HTML -> {hp.relative_to(ROOT)}")
