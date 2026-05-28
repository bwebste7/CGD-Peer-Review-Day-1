"""
Compute Mean Adequacy Ratio (MAR) by country x treatment group.

Data sources:
  - Stata: food_for compression.dta  (weekly household food consumption in kg)
  - Excel: Table_A2_A8_4.11.25.xlsx  (FAO nutritional content per 100g edible portion)

MAR definition:
  For each nutrient n: NAR_n = min(intake_n / RDA_n, 1)
  MAR = mean(NAR_n across n)
  Nutrients used: Protein, Calcium, Iron, Vitamin C

RDA reference: WHO/FAO (2004) Vitamin and Mineral Requirements in Human Nutrition
  Protein:   50 g/day
  Calcium: 1000 mg/day
  Iron:    19.6 mg/day  (women 19-50, 15% bioavailability — the conservative WHO/FAO value)
  Vit C:     45 mg/day

Notes:
  - Philippines (rct_num=4) excluded: only expenditure data, no kg quantities.
  - Weekly household kg totals are divided by n_hh and 7 to get daily per-capita intake.
  - Missing kg values treated as 0 (not consumed that week).
"""

import pandas as pd
import numpy as np
import openpyxl
import pyreadstat

# ── Paths ─────────────────────────────────────────────────────────────────────
DTA_PATH   = '/tmp/food_for compression.dta'
XLSX_PATH  = '/root/.claude/uploads/6b9b5afe-ad83-48c5-9847-c6a180bed53f/c769998f-Table_A2_A8_4.11.25.xlsx'
OUTPUT_CSV = '/home/user/CGD-Peer-Review-Day-1/MAR_by_country_treatment.csv'

# ── Nutrients and WHO/FAO 2004 RDAs ──────────────────────────────────────────
NUTRIENTS = ['protein', 'calcium', 'iron', 'vitc']
RDAS = {
    'protein': 50.0,     # g/day
    'calcium': 1000.0,   # mg/day
    'iron':    19.6,     # mg/day
    'vitc':    45.0,     # mg/day
}

# ── Study mapping ─────────────────────────────────────────────────────────────
# rct_num → FAO study label in 'FAO Data A2' sheet
STUDY_TO_FAO = {
    1.0: 'Pal/Progresa',   # mexico_pal
    2.0: 'Pal/Progresa',   # mexico_progresa
    3.0: 'Nicaragua',       # nicaragua_rps
    5.0: 'Uganda',          # uganda_WFP
    # 4.0 Philippines excluded (no kg data)
}

COUNTRY_LABELS = {
    1.0: 'Mexico (PAL)',
    2.0: 'Mexico (Progresa)',
    3.0: 'Nicaragua',
    5.0: 'Uganda',
}

# ── Food variable mapping: FAO food name → Stata kg_ variables ────────────────
# Mexico/PAL/Progresa uses kg_porkbf (combined pork/beef), kg_sugar
# Nicaragua uses kg_beef, kg_pork, kg_sugar
# Uganda uses kg_beef, kg_pork, kg_allsugar, kg_corn + kg_corn_grained + kg_cornflour
FOOD_VARS = {
    'corn':         {
        'default':   ['kg_corn', 'kg_corntortilla', 'kg_cornflour'],
        5.0:         ['kg_corn', 'kg_corn_grained', 'kg_cornflour'],
    },
    'bread':        {'default': ['kg_whitebread', 'kg_sweetbread', 'kg_boxbread', 'kg_bread']},
    'rice':         {'default': ['kg_rice']},
    'potato':       {'default': ['kg_potato']},
    'chicken':      {'default': ['kg_chicken']},
    # porkbf = combined pork/beef in Mexico surveys; separate in Nicaragua/Uganda
    'pork':         {
        'default':   ['kg_pork'],
        1.0:         ['kg_porkbf'],
        2.0:         ['kg_porkbf'],
    },
    'beef':         {
        'default':   ['kg_beef'],
        1.0:         [],   # subsumed in porkbf above
        2.0:         [],
    },
    'sheepgoat':    {'default': ['kg_sheepgt', 'kg_goat']},
    'fish':         {'default': ['kg_fish', 'kg_fishsf', 'kg_sardines', 'kg_tuna',
                                  'kg_shrimp', 'kg_fish_fried']},
    'egg':          {'default': ['kg_egg']},
    'milk':         {'default': ['kg_milk']},
    'beans':        {'default': ['kg_beans']},
    'tomato':       {'default': ['kg_tomato']},
    'carrot':       {'default': ['kg_carrot']},
    'banana':       {'default': ['kg_banana']},
    'onion':        {'default': ['kg_onion', 'kg_onion_wh', 'kg_onion_ye']},
    'leafy greens': {'default': ['kg_leafveg']},
    'cookies':      {'default': ['kg_cookies']},
    'sugar':        {
        'default':   ['kg_sugar'],
        5.0:         ['kg_allsugar'],
    },
    'oil':          {'default': ['kg_oil', 'kg_lard']},
}


def get_vars_for_study(food, rct_num):
    mapping = FOOD_VARS.get(food, {})
    return mapping.get(rct_num, mapping.get('default', []))


# ── 1. Load FAO nutritional data ───────────────────────────────────────────────
wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
ws = wb['FAO Data A2']

fao_rows = []
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
    if row[0] is None:
        continue
    fao_rows.append({
        'study_label': str(row[0]).strip(),
        'food':        str(row[2]).strip().lower() if row[2] else None,
        'kcal':        row[9],
        'carbs':       row[10],
        'protein':     row[11],
        'fat':         row[12],
        'fiber':       row[13],
        'ash':         row[14],
        'calcium':     row[15],
        'iron':        row[16],
        'vitc':        row[17],
    })

fao = pd.DataFrame(fao_rows).dropna(subset=['food'])

# ── 2. Load Stata data ─────────────────────────────────────────────────────────
df, meta = pyreadstat.read_dta(DTA_PATH, encoding='latin1')

# ── 3. Compute per-person per-day nutrient intake and MAR ─────────────────────
all_results = []

for rct_num, fao_label in STUDY_TO_FAO.items():
    sub = df[df['rct_num'] == rct_num].copy()

    # Nutritional lookup for this study
    fao_sub = (
        fao[fao['study_label'] == fao_label]
        .groupby('food')[NUTRIENTS]
        .first()   # one row per food (studies have one entry each)
    )

    # Initialize intake accumulators
    for n in NUTRIENTS:
        sub[f'intake_{n}'] = 0.0

    for food in FOOD_VARS:
        kg_vars = get_vars_for_study(food, rct_num)
        if not kg_vars:
            continue

        # Keep only variables that exist in this dataset
        kg_vars = [v for v in kg_vars if v in sub.columns]
        if not kg_vars:
            continue

        if food not in fao_sub.index:
            continue

        nut_row = fao_sub.loc[food]
        kg_weekly = sub[kg_vars].fillna(0).clip(lower=0).sum(axis=1)

        for n in NUTRIENTS:
            nut_val = nut_row[n]
            if pd.isna(nut_val):
                continue
            # kg * (g/100g conversion) * nutrient_per_100g = kg * 10 * nutrient_per_100g
            sub[f'intake_{n}'] += kg_weekly * 10.0 * nut_val

    # Convert weekly HH total → daily per-capita
    n_hh = sub['n_hh'].replace(0, np.nan)
    for n in NUTRIENTS:
        sub[f'intake_{n}'] = sub[f'intake_{n}'] / n_hh / 7.0

    # NAR (capped at 1) and MAR
    nar_cols = []
    for n in NUTRIENTS:
        col = f'nar_{n}'
        sub[col] = (sub[f'intake_{n}'] / RDAS[n]).clip(upper=1.0)
        nar_cols.append(col)

    sub['MAR'] = sub[nar_cols].mean(axis=1)
    sub['rct_num'] = rct_num

    keep = ['rct_num', 'treated', 'n_hh', 'MAR'] + \
           [f'intake_{n}' for n in NUTRIENTS] + nar_cols
    all_results.append(sub[keep])

result = pd.concat(all_results, ignore_index=True)
result['country']   = result['rct_num'].map(COUNTRY_LABELS)
result['treatment'] = result['treated'].map({0.0: 'Control', 1.0: 'Treatment'})

# ── 4. Summary table ──────────────────────────────────────────────────────────
summary = (
    result.groupby(['country', 'treatment'])
    .agg(
        MAR_mean        = ('MAR',            'mean'),
        MAR_sd          = ('MAR',            'std'),
        protein_intake  = ('intake_protein', 'mean'),
        calcium_intake  = ('intake_calcium', 'mean'),
        iron_intake     = ('intake_iron',    'mean'),
        vitc_intake     = ('intake_vitc',    'mean'),
        nar_protein     = ('nar_protein',    'mean'),
        nar_calcium     = ('nar_calcium',    'mean'),
        nar_iron        = ('nar_iron',       'mean'),
        nar_vitc        = ('nar_vitc',       'mean'),
        n_obs           = ('MAR',            'count'),
    )
    .round(4)
    .reset_index()
)

print(summary.to_string(index=False))
print()
print(f"Saved household-level results to: {OUTPUT_CSV}")

result.to_csv(OUTPUT_CSV, index=False)
