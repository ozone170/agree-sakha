# backend/expand_plans.py
import json, os

EXPANDED = os.path.join(os.path.dirname(__file__), "implementation_plans_expanded.json")
OUT = EXPANDED

# Base plans removed, using expanded directly if needed
base = {}

def make_variant(base_plan, variant):
    p = {}
    summary = base_plan.get("summary", "")
    dur = base_plan.get("duration_weeks", "")
    p["summary"] = f"{summary} ({variant.replace('_',' ').title()} variant)"
    p["duration_weeks"] = dur

    for k, v in base_plan.items():
        if k in ["summary","duration_weeks"]: continue
        if variant == "high_yield":
            if isinstance(v, list):
                new = v + ["Use high-yielding varieties; monitor and increase N application slightly; consider foliar micronutrients"]
            elif isinstance(v, dict):
                new = {}
                for kk, vv in v.items():
                    new[kk] = (vv + ["Increase N slightly; consider foliar micronutrient sprays"]) if isinstance(vv, list) else vv
            else:
                new = v
        elif variant == "organic":
            if isinstance(v, list):
                new = ["Prefer well-decomposed compost/FYM and biofertilizers"] + v
            elif isinstance(v, dict):
                new = {}
                for kk, vv in v.items():
                    new[kk] = (["Use organic inputs like compost, rock phosphate"] + vv) if isinstance(vv, list) else vv
            else:
                new = v
        elif variant == "low_input":
            if isinstance(v, list):
                new = v + ["Adopt conservation practices: mulch, minimal tillage, low fertilizer rates"]
            elif isinstance(v, dict):
                new = {}
                for kk, vv in v.items():
                    new[kk] = (vv + ["Reduce chemical fertilizer by ~30%; rely on legumes/rotation"]) if isinstance(vv, list) else vv
            else:
                new = v
        else:
            new = v
        p[k] = new
    return p

out = {}
for crop, plan in base.items():
    out[crop] = {
        "summary": plan.get("summary",""),
        "duration_weeks": plan.get("duration_weeks",""),
        "variants": {
            "default": plan,
            "high_yield": make_variant(plan, "high_yield"),
            "organic": make_variant(plan, "organic"),
            "low_input": make_variant(plan, "low_input")
        }
    }

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"Wrote expanded plans to {OUT}")
