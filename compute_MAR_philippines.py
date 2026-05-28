"""
Compute Philippines MAR (Mean Adequacy Ratio) using:
  - moduleA-all_1.dta : Pantawid 4Ps baseline household survey
      AfoodHH   : annual HH food expenditure (PHP)
      hhcount   : household size
      treated   : 0/1
      prov      : 4-digit PSGC province code (e.g. '0746')
  - FIES Data.dta : barangay-level food group budget shares and prices
      agg_food_gp : 1-15 food groups (see below)
      w           : budget share weight (fractions summing to ~0.66 per barangay)
      median_cost : PHP per unit (see unit notes below)
      prov_code   : 2-digit province number string
      year        : 2009, 2012, or 2015

Strategy:
  1. Use FIES year=2009 aggregated to province level (only 12% of moduleA
     barangays appear in FIES, so province-level is required).
  2. Normalise w across groups 1-15 within each province to get food-group
     spending shares that sum to 1.
  3. Weekly HH expenditure per group = (AfoodHH / 52) × share_group.
  4. Convert to kg: kg_group = exp_group / price_per_kg_group.
  5. Map food groups to Philippine FAO nutritional data (per 100g).
  6. Compute nutrient intakes → NAR (capped at 1) → MAR.

FIES food groups and unit assumptions:
  1  Regular milled commercial rice  → PHP/kg
  2  Other raw rice/grains           → PHP/kg
  3  Roots/tubers                    → PHP/kg  (potato proxy)
  4  Fresh eggs                      → PHP/piece  (50g/piece assumed)
  5  Processed eggs                  → PHP/piece  (50g/piece assumed)
  6  Fresh fish                      → PHP/kg
  7  Processed fish                  → PHP/kg
  8  Fresh meat                      → PHP/kg
  9  Processed meat                  → PHP/kg
  10 Fresh fruit                     → PHP/kg  (banana proxy)
  11 Fresh vegetables                → PHP/kg  (leafy greens proxy)
  12 Rice/grains processed           → PHP/g → ×1000 for per-kg  (small-unit pricing)
  13 Coffee/cocoa/tea                → skipped (negligible nutrients)
  14 Sugar                           → PHP/kg
  15 Milk products                   → PHP/g → ×1000 for per-kg  (small-unit pricing)

WHO/FAO 2004 RDAs:
  Protein   50 g/day
  Calcium 1000 mg/day
  Iron      19.6 mg/day
  Vit C     45 mg/day
"""

import pandas as pd
import numpy as np
import pyreadstat
import openpyxl

# ── Paths ──────────────────────────────────────────────────────────────────────
MODULE_A_PATH = '/tmp/moduleA-all_1.dta'
FIES_PATH     = '/tmp/FIES Data.dta'
XLSX_PATH     = '/root/.claude/uploads/6b9b5afe-ad83-48c5-9847-c6a180bed53f/c769998f-Table_A2_A8_4.11.25.xlsx'
OUTPUT_CSV    = '/home/user/CGD-Peer-Review-Day-1/MAR_by_country_treatment.csv'
ATE_CSV       = '/home/user/CGD-Peer-Review-Day-1/MAR_ATE_by_country.csv'

NUTRIENTS = ['protein', 'calcium', 'iron', 'vitc']
RDAS = {'protein': 50.0, 'calcium': 1000.0, 'iron': 19.6, 'vitc': 45.0}

# ── FIES food group → FAO food name + unit type ────────────────────────────────
# unit: 'kg' = median_cost is PHP/kg; 'piece' = PHP/piece (eggs); 'gram' = PHP/g
FIES_GROUP_MAP = {
    1:  ('rice',         'kg'),
    2:  ('rice',         'kg'),
    3:  ('potato',       'kg'),
    4:  ('egg',          'piece'),   # ~50g per piece
    5:  ('egg',          'piece'),
    6:  ('fish',         'kg'),
    7:  ('fish',         'kg'),
    8:  ('chicken',      'kg'),      # fresh meat: chicken is closest single FAO item
    9:  ('chicken',      'kg'),      # processed meat: same proxy
    10: ('banana',       'kg'),
    11: ('leafy greens', 'kg'),
    12: ('bread',        'gram'),    # sub-1 PHP cost → treat as PHP/gram
    13: None,                        # coffee/tea: skip
    14: ('sugar',        'kg'),
    15: ('milk',         'gram'),    # sub-1 PHP cost → treat as PHP/gram
}
EGG_KG_PER_PIECE = 0.05  # 50g per egg


# ── 1. Load FAO nutritional data for Philippines ───────────────────────────────
wb  = openpyxl.load_workbook(XLSX_PATH, data_only=True)
ws  = wb['FAO Data A2']

fao_rows = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] is None:
        continue
    fao_rows.append({
        'study':   str(row[0]).strip(),
        'food':    str(row[2]).strip().lower() if row[2] else None,
        'protein': row[11],
        'calcium': row[15],
        'iron':    row[16],
        'vitc':    row[17],
    })

fao_df  = pd.DataFrame(fao_rows).dropna(subset=['food'])
fao_phi = fao_df[fao_df['study'] == 'Philippines'].set_index('food')[NUTRIENTS]

print("Philippine FAO nutritional data (per 100g):")
print(fao_phi)


# ── 2. Load household data (moduleA) ──────────────────────────────────────────
mod, _ = pyreadstat.read_dta(MODULE_A_PATH, encoding='latin1')

# Extract 2-digit province number from 4-digit PSGC code (last 2 chars)
mod['prov_num'] = mod['prov'].str[-2:].astype(int)

# Restrict to sample 1 (the main RCT sample)
mod = mod[mod['sample'] == 1].copy()

# Keep rows with usable food expenditure and household size
mod = mod.dropna(subset=['AfoodHH', 'hhcount', 'treated']).copy()
mod = mod[mod['AfoodHH'] > 0].copy()

print(f"\nmoduleA households after cleaning (sample 1): {len(mod)}")
print(f"Provinces covered: {sorted(mod['prov_num'].unique())}")


# ── 3. Build province-level FIES price table (year 2009) ──────────────────────
fies, _ = pyreadstat.read_dta(FIES_PATH, encoding='latin1')

fies_09 = fies[(fies['year'] == 2009) & (fies['agg_food_gp'].notna())].copy()
fies_09['prov_num'] = fies_09['prov_code'].astype(int)

# Province-level mean of w and median_cost across barangays
prov_fies = (
    fies_09.groupby(['prov_num', 'agg_food_gp'])
    .agg(w=('w', 'mean'), median_cost=('median_cost', 'mean'))
    .reset_index()
)

# Normalise budget shares to sum to 1 within each province
prov_totw = prov_fies.groupby('prov_num')['w'].transform('sum')
prov_fies['share'] = prov_fies['w'] / prov_totw

print("\nProvince-level FIES coverage:")
print(f"  FIES provinces: {sorted(prov_fies['prov_num'].unique())}")
print(f"  moduleA provinces: {sorted(mod['prov_num'].unique())}")
matched = set(mod['prov_num'].unique()) & set(prov_fies['prov_num'].unique())
print(f"  Matched: {len(matched)} of {mod['prov_num'].nunique()} moduleA provinces")


# ── 4. Compute per-group price-per-kg (adjusting for unit type) ───────────────
def price_per_kg(cost, unit):
    if unit == 'kg':
        return cost
    if unit == 'piece':
        return cost / EGG_KG_PER_PIECE  # PHP/piece → PHP/kg
    if unit == 'gram':
        return cost * 1000              # PHP/g → PHP/kg
    return np.nan


# ── 5. Build nutrient-intake lookup: group × province → kg per PHP spent ──────
# For each FIES group, compute nutrient content per kg (per 100g × 10)
# Then: intake_per_PHP = (nutrient_per_kg) / price_per_kg

group_nutrients = {}  # group_id → {n: nutrient_per_kg}
for gid, info in FIES_GROUP_MAP.items():
    if info is None:
        continue
    food_name, unit = info
    if food_name not in fao_phi.index:
        continue
    nrow = fao_phi.loc[food_name]
    group_nutrients[gid] = {
        n: (nrow[n] * 10.0 if pd.notna(nrow[n]) else 0.0)  # per 100g × 10 = per kg
        for n in NUTRIENTS
    }

print("\nNutrient content per kg by food group:")
for gid, ndict in group_nutrients.items():
    food = FIES_GROUP_MAP[gid][0]
    print(f"  Group {gid:2d} ({food:15s}): {ndict}")


# ── 6. Merge households with province FIES data and compute MAR ───────────────
results = []

for prov_num, hh_grp in mod.groupby('prov_num'):
    # Get FIES price/share table for this province (fall back to national if missing)
    prov_data = prov_fies[prov_fies['prov_num'] == prov_num]
    if len(prov_data) == 0:
        print(f"  WARNING: no FIES data for province {prov_num}, using national average")
        prov_data = (
            prov_fies.groupby('agg_food_gp')
            .agg(w=('w', 'mean'), share=('share', 'mean'), median_cost=('median_cost', 'mean'))
            .reset_index()
        )
        prov_data['prov_num'] = prov_num

    # Build group→(share, price_per_kg) mapping for this province
    gp_lookup = {}
    for _, row in prov_data.iterrows():
        gid  = int(row['agg_food_gp'])
        info = FIES_GROUP_MAP.get(gid)
        if info is None:
            continue
        _, unit = info
        ppkg = price_per_kg(row['median_cost'], unit)
        if ppkg is None or ppkg <= 0:
            continue
        gp_lookup[gid] = {'share': row['share'], 'price_per_kg': ppkg}

    # Compute household-level intakes
    hh_rows = hh_grp.copy()
    for n in NUTRIENTS:
        hh_rows[f'intake_{n}'] = 0.0

    weekly_food_exp = hh_rows['AfoodHH'] / 52.0  # annual → weekly HH

    for gid, gp in gp_lookup.items():
        if gid not in group_nutrients:
            continue
        exp_group   = weekly_food_exp * gp['share']        # weekly PHP on this group
        kg_group    = exp_group / gp['price_per_kg']       # kg per week (HH total)
        # Per-capita-per-day: divide by hhcount and 7
        kg_pcpd     = kg_group / hh_rows['hhcount'] / 7.0
        for n in NUTRIENTS:
            hh_rows[f'intake_{n}'] += kg_pcpd * 10.0 * (group_nutrients[gid][n] / 10.0 * 10.0)
            # group_nutrients[gid][n] is already per-kg (=per-100g × 10)
            # kg_pcpd × nutrient_per_kg = daily per-capita intake

    results.append(hh_rows)

phil_hh = pd.concat(results, ignore_index=True)

# Fix intake computation: re-derive cleanly
# intake columns above double-multiplied; redo
for n in NUTRIENTS:
    phil_hh[f'intake_{n}'] = 0.0

weekly_food_exp = phil_hh['AfoodHH'] / 52.0

for prov_num in phil_hh['prov_num'].unique():
    prov_mask = phil_hh['prov_num'] == prov_num
    prov_data = prov_fies[prov_fies['prov_num'] == prov_num]
    if len(prov_data) == 0:
        prov_data = (
            prov_fies.groupby('agg_food_gp')
            .agg(w=('w', 'mean'), share=('share', 'mean'), median_cost=('median_cost', 'mean'))
            .reset_index()
        )

    gp_lookup = {}
    for _, row in prov_data.iterrows():
        gid  = int(row['agg_food_gp']) if pd.notna(row['agg_food_gp']) else None
        if gid is None:
            continue
        info = FIES_GROUP_MAP.get(gid)
        if info is None:
            continue
        _, unit = info
        ppkg = price_per_kg(row['median_cost'], unit)
        if ppkg is None or ppkg <= 0:
            continue
        gp_lookup[gid] = {'share': row['share'], 'price_per_kg': ppkg}

    for gid, gp in gp_lookup.items():
        if gid not in group_nutrients:
            continue
        exp_grp_prov  = weekly_food_exp[prov_mask] * gp['share']
        kg_week_prov  = exp_grp_prov / gp['price_per_kg']
        kg_pcpd_prov  = kg_week_prov / phil_hh.loc[prov_mask, 'hhcount'] / 7.0
        for n in NUTRIENTS:
            nut_per_kg = group_nutrients[gid][n]   # already per kg
            phil_hh.loc[prov_mask, f'intake_{n}'] += kg_pcpd_prov * nut_per_kg


# ── 7. NAR and MAR ────────────────────────────────────────────────────────────
nar_cols = []
for n in NUTRIENTS:
    col = f'nar_{n}'
    phil_hh[col] = (phil_hh[f'intake_{n}'] / RDAS[n]).clip(upper=1.0)
    nar_cols.append(col)

phil_hh['MAR']     = phil_hh[nar_cols].mean(axis=1)
phil_hh['rct_num'] = 4.0
phil_hh['country'] = 'Philippines'
phil_hh['treatment'] = phil_hh['treated'].map({0.0: 'Control', 1.0: 'Treatment'})

# Rename hhcount → n_hh to match other countries
phil_hh = phil_hh.rename(columns={'hhcount': 'n_hh'})

# ── 8. Summary ────────────────────────────────────────────────────────────────
summary = (
    phil_hh.groupby('treatment')
    .agg(
        MAR_mean       = ('MAR',            'mean'),
        MAR_sd         = ('MAR',            'std'),
        protein_intake = ('intake_protein', 'mean'),
        calcium_intake = ('intake_calcium', 'mean'),
        iron_intake    = ('intake_iron',    'mean'),
        vitc_intake    = ('intake_vitc',    'mean'),
        nar_protein    = ('nar_protein',    'mean'),
        nar_calcium    = ('nar_calcium',    'mean'),
        nar_iron       = ('nar_iron',       'mean'),
        nar_vitc       = ('nar_vitc',       'mean'),
        n_obs          = ('MAR',            'count'),
    )
    .round(4)
    .reset_index()
)

print("\n── Philippines MAR summary ──")
print(summary.to_string(index=False))

# ── 9. ATE ────────────────────────────────────────────────────────────────────
from scipy import stats

ctrl = phil_hh.loc[phil_hh['treated'] == 0, 'MAR'].dropna()
trt  = phil_hh.loc[phil_hh['treated'] == 1, 'MAR'].dropna()
ate  = trt.mean() - ctrl.mean()
tstat, pval = stats.ttest_ind(trt, ctrl, equal_var=False)

print(f"\nPhilippines ATE: {ate:.4f}  (p={pval:.4f})")
print(f"  Control MAR:   {ctrl.mean():.4f}  (n={len(ctrl)})")
print(f"  Treatment MAR: {trt.mean():.4f}  (n={len(trt)})")


# ── 10. Update combined CSV files ─────────────────────────────────────────────
keep_cols = ['rct_num', 'treated', 'n_hh', 'MAR',
             'intake_protein', 'intake_calcium', 'intake_iron', 'intake_vitc',
             'nar_protein', 'nar_calcium', 'nar_iron', 'nar_vitc',
             'country', 'treatment']

phil_out = phil_hh[keep_cols].copy()

# Load existing results (non-Philippines) and replace Philippines rows
existing = pd.read_csv(OUTPUT_CSV)
existing_no_phi = existing[existing['rct_num'] != 4.0]
combined = pd.concat([existing_no_phi, phil_out], ignore_index=True)
combined.to_csv(OUTPUT_CSV, index=False)
print(f"\nUpdated {OUTPUT_CSV}  ({len(combined)} rows)")

# Update ATE table
ate_df = pd.read_csv(ATE_CSV)
ate_df = ate_df[ate_df['country'] != 'Philippines'].copy()

new_row = pd.DataFrame([{
    'country':        'Philippines',
    'control_MAR':    round(ctrl.mean(), 4),
    'treatment_MAR':  round(trt.mean(), 4),
    'ATE':            round(ate, 4),
    'se':             round(np.sqrt(trt.var()/len(trt) + ctrl.var()/len(ctrl)), 4),
    'pvalue':         round(pval, 4),
    'n_control':      len(ctrl),
    'n_treatment':    len(trt),
    'method':         'FIES 2009 budget shares + moduleA expenditure',
}])

ate_df = pd.concat([ate_df, new_row], ignore_index=True)
ate_df.to_csv(ATE_CSV, index=False)

print(f"Updated {ATE_CSV}")
print("\nFull ATE table:")
print(ate_df.to_string(index=False))
