"""Turn hand-written concept fact tables into questions.

A table is a list of dict rows with a "name" key. For each attribute spec
    (attr, topic, fwd_template, rev_template_or_None, unique_only)
we emit:
  forward  : "<fwd with {name}>"            -> row[attr]    (distractors: other rows' values)
  reverse  : "<rev with {value}>"           -> row["name"]  (only if value unique in table when unique_only)
  true/false: correct statement, and one with another row's value swapped in
"""
import re
from common import RNG, mcq, tf, short, norm


def fix(text):
    text = re.sub(r"\b([Aa]) ([aeiouAEIOU])", lambda m: ("an " if m.group(1) == "a" else "An ") + m.group(2), text)
    return text[:1].upper() + text[1:]


def agree(template, name):
    """Subject-verb agreement for plural row names ('mud cracks form', 'varves are')."""
    plural = name.endswith("s") and not name.endswith(("ss", "is", "us")) and not name.startswith(("the ", "The "))
    if not plural or not template.startswith("{name} "):
        return template
    head, rest = template[len("{name} "):].split(" ", 1) if " " in template[len("{name} "):] else (template[len("{name} "):], "")
    verb = {"is": "are", "has": "have", "forms": "form", "typically": "typically"}.get(head, head)
    if head == "typically" and rest.startswith("produces"):
        rest = "produce" + rest[len("produces"):]
    return "{name} " + verb + (" " + rest if rest else "")


def plural_q(template, name):
    """'How does {name} form?' -> 'How do mud cracks form?' for plural names."""
    plural = name.endswith("s") and not name.endswith(("ss", "is", "us"))
    return template.replace("does {name}", "do {name}").replace("{name} is ", "{name} are ") if plural else template


def _others(rows, attr, row):
    v = row[attr]
    return [r[attr] for r in rows if r is not row and r.get(attr) and norm(r[attr]) != norm(v)
            and norm(r[attr]) not in norm(v) and norm(v) not in norm(r[attr])]


def emit(rows, specs, kind, diff=2, tags=(), sp_key="sp"):
    for row in rows:
        sp = row.get(sp_key, [])
        for spec in specs:
            attr, topic, fwd, rev, uniq = spec[:5]
            stmt_t = spec[5] if len(spec) > 5 else None
            v = row.get(attr)
            if not v:
                continue
            others = _others(rows, attr, row)
            kw = dict(diff=row.get("diff", diff), specimens=sp, tags=list(tags) + [kind], source="authored",
                      explanation=row.get("why", ""))
            if fwd and len(others) >= 2:
                mcq(topic, fix(plural_q(fwd, row["name"]).format(name=row["name"])), v, others, n=min(3, len(others)), **kw)
            same = [r for r in rows if r.get(attr) and norm(r[attr]) == norm(v)]
            if rev and (not uniq or len(same) == 1):
                names = [r["name"] for r in rows if r.get(attr) and norm(r[attr]) != norm(v) and r["name"] != row["name"]]
                if len(names) >= 2:
                    mcq(topic, fix(rev.format(value=v)), row["name"], names, n=min(3, len(names)), **kw)
            if stmt_t and others:
                st = agree(stmt_t, row["name"])
                tf(topic, fix(st.format(name=row["name"], value=v)), True, **kw)
                tf(topic, fix(st.format(name=row["name"], value=RNG.choice(others))), False,
                   **dict(kw, explanation=(f"Correct: {v}. " + row.get("why", "")).strip()))


def glossary(entries, kind="vocabulary"):
    """entries: (term, definition, topic, [also-accepted terms])"""
    by_topic = {}
    for t, d, top, acc in entries:
        by_topic.setdefault(top[:5], []).append(t)
    allterms = [e[0] for e in entries]
    for t, d, top, acc in entries:
        pool = [x for x in by_topic[top[:5]] if x != t] + RNG.sample([x for x in allterms if x != t], 6)
        mcq(top, f"Which term means: {d}?", t, pool, diff=1, tags=[kind], source="authored", explanation=f"{t}: {d}.")
        defs = [e[1] for e in entries if e[0] != t and e[2][:5] == top[:5]] or [e[1] for e in entries if e[0] != t]
        mcq(top, f"What does '{t}' mean?", d, defs + [e[1] for e in RNG.sample(entries, 4) if e[0] != t], diff=1, tags=[kind],
            source="authored")
        short(top, f"Give the term for: {d}.", t, [t] + list(acc), diff=2, tags=[kind], source="authored", explanation=f"{t}: {d}.")
