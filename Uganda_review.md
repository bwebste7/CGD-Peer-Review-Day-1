# Peer Review: "From Childhood Abduction to Adulthood: Enduring Consequences for Women in Uganda"
**Cassar, Kandpal, Lambert, Mbabaze Mpyangu, and Serra (April 2025)**

---

## Summary

This paper examines the long-term consequences of childhood abduction by the Lord's Resistance Army (LRA) on women in Northern Uganda, studying roughly 550 women approximately 20 years after the conflict ended. Roughly half were abducted as children. The authors leverage the well-documented plausible exogeneity of LRA abductions — first established by Blattman and Annan (2010) — and extend it to a comprehensive battery of outcomes: mental health (depression, perceived stress), stress response mechanisms (tend-and-befriend, fight-or-flight), socioeconomic outcomes, and incentivized behavioral measures of grit, competitiveness, risk tolerance, and prosociality.

The core findings are sobering and important: formerly abducted women show substantially higher rates of depression and perceived stress two decades later, along with lower social support and educational attainment, more biological children, and — in a striking result consistent with post-traumatic growth — greater measured grit. The paper is well-written, carefully executed given its field setting, and addresses a population that is both understudied and policy-relevant. Several methodological concerns merit attention before publication.

---

## Part 1 (Edmans Framework): Contribution, Execution, Exposition

### Contribution

**Strengths:**
- The research question is genuinely important. Child abductions in conflict settings are increasing globally (UN, 2024), and evidence on their *long-term* consequences for *women* is sparse. The existing literature (Annan et al., 2011) is from shortly after the conflict's end; this paper provides the first 20-year follow-up.
- Adding incentivized behavioral games — including a novel tend-and-befriend stress-response instrument — extends the outcomes measured beyond standard survey items and into domains (non-cognitive traits) not previously examined in this context.
- The use of validated clinical instruments (EPDS, PSS-10) provides credible, cross-culturally comparable mental health measures.
- The finding that severe mental health impacts persist 20 years post-conflict, despite the widespread poverty serving as a floor effect for socioeconomic outcomes, is a genuine contribution that could change how scholars and policymakers think about recovery in fragile settings.

**Concerns:**
- The paper could more sharply distinguish its three specific contributions relative to three specific antecedent papers. The "value-added" discussion is diffuse; readers would benefit from a single paragraph that names Annan et al. (2011), Singhal (2019), and Islam et al. (2023) and states explicitly what this paper adds to each.

### Execution

**Strengths:**
- The regression strategy is sensible: village fixed effects absorb community-level confounders; clustering at the workshop level is appropriate; the Romano-Wolf step-down procedure properly addresses the multiple-comparisons problem across a large outcome set.
- Double Lasso robustness checks are a modern and defensible approach to control selection.
- The two-sample validation of the identifying assumption (using independently drawn Kitgum samples from Cassar et al. (2025) and Lambert (2025)) partially compensates for the absence of pre-abduction balance data in the primary survey.
- Workshop design choices — random ID assignment, female enumerators, private interviews, logistics to minimize waiting and fatigue — are thoughtful and well-described.

**Major concerns:**

1. **Absence of pre-abduction balance checks in the primary survey.** The authors acknowledge this as an "inadvertent oversight." The identifying assumption is that abductions were plausibly random conditional on observable pre-war characteristics. The authors compensate by showing balance in two external samples, but neither sample is the same population surveyed here, and one (Cassar et al., 2025) cannot be linked to the current sample at the individual level. The paper should more clearly bound the sensitivity of results to plausible violations of this assumption (e.g., a simple Oster (2019) bounding exercise or a discussion of the direction in which omitted pre-war characteristics would bias results).

2. **Survival and attrition bias.** Women who died during captivity, died afterward, or permanently migrated are not observed. If the most severely affected abductees are disproportionately missing from the sample, the estimated effects are a lower bound on true harm. The paper acknowledges this qualitatively but provides no quantitative sense of how large this bias could plausibly be. At minimum, the authors should note how abduction-related mortality rates in the literature compare across FA and NA groups.

3. **Age imbalance between FA and NA women.** Formerly abducted women are on average five years younger (29 vs. 34), a statistically significant difference. The authors acknowledge this and control for age, but the imbalance is substantial enough to raise the question of whether life-stage differences (e.g., younger women may not yet have reached the same educational or marital outcomes as older women) could confound the results even after conditioning on a linear age control. Results could be presented for a more restricted age-matched subsample as an additional robustness check.

4. **Robustness of key results.** Several results that appear in primary tables do not survive the Double Lasso procedure:
   - The Cohen stress index and "Severely Stressed" indicator lose significance.
   - All socioeconomic outcomes (education, children, social support) lose significance, though the authors note this is likely because the Lasso selects the Edinburgh index as a control.
   The conclusion should be more candid about which findings are robust and which are fragile.

5. **Social Support Index truncation.** The Social Support Index is reported only for women with a current spouse or partner (430 of 541). The 39% of women who are single, separated, or widowed are excluded. If abduction affects partner outcomes (as the paper finds it affects number of children), this selection could be non-random. Results should be presented for all women using the partner-agnostic subscale questions, or the limitation should be more prominently flagged.

### Exposition

- The paper is clearly written and well-organized. The contribution is stated in the introduction and the results are presented in logical order.
- The abstract effectively summarizes the core findings but could devote one more sentence to the behavioral game findings.
- The conclusion appropriately identifies limitations but is vague on policy implications (see below).

---

## Part 2 (Humphreys Framework): Major Themes

### Theme 1: Identification — "Borrowed" Balance Checks and Their Limits

The identification strategy rests on the claim that LRA abductions were plausibly exogenous — a claim well-established by Blattman and Annan (2010) for boys and validated for women via two external samples. However, several subtleties deserve attention:

- The age imbalance (FA women are younger) is itself the most important confound, since younger women were exposed to the conflict during later years when it may have been less intense, the humanitarian response may have been different, and they may have had less time to accumulate education or other outcomes. Age controls absorb a first-order version of this, but non-linear effects could remain.
- Father's presence in the household is marginally significant (p=0.05) in the unconditional Panel B of Table 1, suggesting that girls from households without fathers may have been slightly more vulnerable to abduction. If household structure predicts adult mental health independently, this could create upward bias in mental health estimates.
- The pre-registration covers the study's design but the sample was expanded after initial funding. The paper should discuss whether primary hypotheses were amended between registrations.

### Theme 2: Self-Report Mental Health Measures and Ecological Validity

The EPDS and PSS-10 are well-validated clinical instruments and appropriate for this setting. But two issues remain:

- Both instruments ask about the past week (EPDS) or past month (PSS-10). They capture current mental health status, not a permanent trait. Data were collected over three waves (January–July 2022). If waves differ systematically in the composition of FA vs. NA participants, or if a seasonal event (e.g., agricultural stress) differentially affected one group, this could confound results. The authors control for collection wave, which partially addresses this.
- The stress response measures (tend, befriend, fight, flight) are self-reported Likert items about how the respondent *says* she typically reacts to stress. This reflects self-perception, not observed behavior under stress. The ecological validity of these measures is limited, and the paper should be careful not to over-interpret them as actual behavioral evidence.

### Theme 3: Behavioral Games — Construct and External Validity

The incentivized games are adapted thoughtfully for a low-literacy population. However:

- **Grit task**: The two grit measures differ in what they capture — Stage 2 choices reflect in-the-moment persistence; Stage 3 captures planning under temporal distance. The large effect size on Grit Measure 1 (32% above NA mean) is striking. Controlling for Stage 1 performance and risk preferences is appropriate. However, if FA women are more accustomed to completing difficult tasks under duress (not as a personality trait but as a learned survival behavior), the grit measure may be conflating genuine persistence with trauma-conditioned vigilance.
- **Competitiveness task (ball toss)**: Physical ability, fatigue, familiarity with throwing games, and self-confidence all affect this outcome. While the authors control for self-reported confidence, residual confounders remain. The insignificant result (Romano-Wolf p=0.11) should not be interpreted as absence of an effect; power to detect modest competitiveness differences may be low.
- **Prosociality (dictator game)**: A ceiling effect is evident — the average share given across all recipients is only 22.9%, while the endowment is 40,000 shillings in a setting where this represents multiple weeks of income. Non-trivial fractions of participants gave zero (31% for some recipients). The finding of *lower* prosociality among FA women is counterintuitive relative to the broader conflict literature and is marginally significant only; the paper appropriately calls this "suggestive."

### Theme 4: Mechanisms

The paper documents reduced-form impacts but does not test mechanisms. Two key channels are implicated but unidentified:

1. **Mental health → socioeconomic outcomes**: The paper notes the bidirectional relationship between mental health and economic well-being, and that depression emerged as a control in the Double Lasso for socioeconomic outcomes. If abduction affects economic outcomes *through* mental health, then the reduced-form coefficients on socioeconomic outcomes conflate direct and mediated effects.
2. **Social support → mental health**: The paper notes lower social support among FA women and its link to mental health, but does not attempt mediation analysis. Even descriptive path analysis could illuminate whether the mental health impacts operate through the observed reduction in social support.

The paper would benefit from at least a brief discussion of likely mechanisms, even if formal mediation tests are not feasible.

### Theme 5: Policy Implications

The conclusion calls for "targeted mental health interventions" in fragile settings, but does not:
- Name specific interventions with evidence of effectiveness in comparable settings
- Assess the costs relative to benefits, even approximately
- Identify clear winners and losers from such programs
- Address the political economy of implementation

Given that the paper's own footnote (footnote 39) cites evidence that existing reintegration programs (traditional ceremonies, reception centers, reinsertion packages) had "limited positive results," a more critical engagement with the policy landscape would be valuable. The finding that abducted women exhibit *greater grit* is genuinely positive and could inform program design (e.g., channeling this grit into productive activities), but this connection is underdeveloped.

---

## Part 3: Smaller Issues

- **Programming error in trauma index**: The fact that the trauma index was collected for 100% of FA but only 18% of NA women due to a programming error is significant. While the authors note this in a footnote, it should be acknowledged more prominently and its implications for comparisons using the trauma index should be discussed.

- **Footnote 23 — inadvertent oversight**: The acknowledgment that pre-abduction characteristics were not collected in the primary survey due to an "inadvertent oversight and miscommunication" should be discussed more fully in the main text, not buried in a footnote. This is a key identification issue.

- **Missing data for activities 3 and 4**: One full workshop of data for the risk and prosociality tasks is missing. The paper should verify that this workshop had similar FA/NA composition to other workshops, and report whether the missing workshop affects balance.

- **Age of 62 outlier**: One woman reports age 62, outside the target sample range. The paper notes this but doesn't clarify whether this observation is retained in analysis. It should be excluded or flagged as robustness.

- **Social support measured only for partnered women**: 4 of 6 MSSS questions require a partner. As noted above, this creates potential selection issues. Consider reporting the 2 non-partner questions as a separate robustness measure.

- **Heterogeneity by time in captivity**: The paper presents heterogeneity by age at abduction but the duration analysis (Figure A4) is relegated to the appendix. Given that duration is arguably as theoretically important as age, a brief discussion in the main text would be warranted.

- **Interpretation of grit as resilience vs. anxiety**: The paper frames higher grit among FA women as "resilience" and "perseverance." But it is also possible that the grit measure captures hypervigilance or anxiety-driven task persistence rather than a positive trait. Given that FA women also show higher depression, stress, and stress responses, the positive framing of the grit result deserves more nuanced treatment.

- **Comparison to Annan et al. (2011) findings on social support**: The authors note that Annan et al. (2011) found *higher* social support among FA women shortly after the conflict, while this paper finds *lower* support 20 years later. This is a compelling and important finding about how social reintegration can erode over time. It deserves more prominence in the discussion.

- **Causal language**: The paper uses "impact," "effect," and "caused" throughout. While the identification strategy is credible relative to the available alternatives, the non-random survival and potential pre-abduction differences counsel some additional hedging on causal claims.

- **Replication materials**: The paper mentions pre-registration and game instructions in the appendix. It is unclear whether survey instruments, full data, and analysis code will be publicly available. This should be stated explicitly.

---

## Part 4 (Evans/Bellemare Framework): Introduction, Abstract, and Conclusion

### Introduction Assessment

- **Hook**: The introduction opens effectively with the scale of global conflict and the specific vulnerability of women and girls. The motivation is about economics and welfare, not about literature — this is correct.
- **Research question**: Clearly stated.
- **Antecedents**: The key antecedents (Blattman and Annan 2010, Annan et al. 2011) are identified and discussed. Literature is integrated rather than siloed.
- **Value-added**: Present but diffuse. The paper would benefit from a more focused paragraph listing three specific contributions relative to three specific prior papers.
- **Roadmap**: Present.

### Abstract Assessment

The abstract is well-structured: motivates the setting, states the approach, and reports the main findings. It uses both the full sample scale (550 women, half abducted) and the key results (25% increase in depression likelihood, 40% increase in severe stress, greater grit). Minor improvement: the behavioral game findings (grit especially) could be mentioned more specifically.

### Conclusion Assessment

- **Summary**: The conclusion re-summarizes findings effectively with a slightly different framing than the abstract.
- **Limitations**: The conclusion identifies the main limitations (recall bias, survival bias, single region, single time point). This section is honest and appropriately modest.
- **Policy implications**: The conclusion calls for "accessible and effective mental health services" and "multidimensional government programming" but these are vague. Given the finding that *existing* reintegration programs have had limited effects (footnote 39), the conclusion should engage more critically with what *different* programming might look like.
- **Future research**: Longitudinal designs are mentioned. The authors could be more specific: (i) panel data linking short-run and long-run outcomes, (ii) testing whether mental health interventions improve economic outcomes given the documented bidirectional relationship, (iii) extending to conflict-affected women outside Uganda.

---

## Summary Verdict

This is a carefully executed and important paper that makes a genuine contribution to the literature on long-run conflict consequences, gender, and mental health. The core finding — that childhood abductions leave deep and lasting mental health scars on women two decades later, even as economic outcomes converge to a uniformly poor baseline — is credible, important, and policy-relevant. The behavioral game evidence on grit adds a novel dimension.

**Major issues to address:**
1. More explicit sensitivity analysis for the absent pre-abduction balance (Oster bounds or similar)
2. Quantitative discussion of survival/attrition bias magnitude
3. Age-matched robustness check for the main results
4. Clearer statement of which results are robust vs. fragile under Double Lasso
5. More prominent treatment of the Social Support Index truncation (partnered women only)
6. Mechanism discussion, even if informal
7. More concrete policy implications given the evidence that existing reintegration programs have been ineffective

**Strengths to preserve:**
- The 20-year follow-up framing and comparison to Annan et al. (2011)
- The behavioral game methodology adapted for low-literacy populations
- The Romano-Wolf multiple testing correction
- The honest and thorough robustness appendix
- The tend-and-befriend analysis as a novel contribution
- The grit finding, appropriately nuanced, as evidence of human resilience under extreme adversity
