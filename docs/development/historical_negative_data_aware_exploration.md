# Historical-Negative-Data-Aware Materials Exploration

## Research positioning

The project aims to reproduce the functional workflow of an industrial materials-informatics platform: historical experimental data → predictive models → exploration of the experimental space → recommendation of the next experiment. The focus is not to reproduce a proprietary implementation, but to establish a transparent and reproducible workflow.

The central methodological question is:

> Can historical failed experiments be used as negative information to improve the identification of feasible experimental regions and the success probability of the next experimental batch?

The workflow is therefore formulated as **historical-negative-data-aware materials exploration**.

## Overall workflow

```text
Historical experiments
├── Successful experiments
│   ├── Composition
│   ├── Process conditions
│   └── Measured properties
└── Failed experiments
    ├── Composition
    ├── Process conditions
    └── Failure type / failure severity
            ↓
      Data preprocessing
            ↓
      Feasibility model + property-specific models
            ↓
      Experimental-space search
            ↓
      Remove low-feasibility regions
            ↓
      Predict individual target properties
            ↓
      Integrate candidate regions
            ↓
      Recommend new composition/process conditions
            ↓
      New experiment → data update → model update
```

## Stage 1 — Feasibility screening

Failed experiments should not be mixed directly with valid numerical property measurements. First, they are used to train a feasibility classifier:

\[
P(\mathrm{success}\mid x),
\qquad
x=(\mathrm{composition},\mathrm{temperature},\mathrm{time},\mathrm{pressure},\ldots).
\]

The labels are:

| Experimental record | Feasibility label |
|---|---:|
| Successful experiment | 1 |
| Failed experiment | 0 |

The classifier identifies feasible regions, high-risk regions, and regions that remain insufficiently explored. A candidate with a low predicted success probability is deprioritized before detailed property optimization.

## Stage 2 — Property-specific modelling

Only successful or otherwise valid measurements are used for the corresponding property models. Separate surrogate models are built for each target, for example:

\[
\hat y_{\mathrm{strength}}(x),\quad
\hat y_{\mathrm{conductivity}}(x),\quad
\hat y_{\mathrm{hardness}}(x),\quad
\hat y_{\mathrm{oxidation\ resistance}}(x).
\]

This keeps the meaning of each model explicit and avoids forcing properties with different physical meanings and missing-data patterns into one opaque score.

Each model defines a promising region, such as a high-strength or high-conductivity region. The final candidate space is obtained by integrating the regions while retaining the feasibility constraint:

\[
R_{\mathrm{candidate}}
=R_{\mathrm{feasible}}
\cap R_{\mathrm{strength}}
\cap R_{\mathrm{conductivity}}
\cap R_{\mathrm{hardness}}
\cap\cdots.
\]

The output is a promising experimental range rather than an apparently precise single optimum. This is more appropriate when composition error, process variation, and measurement noise are non-negligible.

## Bayesian optimization and candidate recommendation

Candidate selection should use both the predicted property and model uncertainty:

\[
x_{\mathrm{next}}
=\arg\max_x\; a\!\left(\mu(x),\sigma(x),P(\mathrm{success}\mid x)\right),
\]

where \(\mu(x)\) is the predicted performance, \(\sigma(x)\) is predictive uncertainty, and \(a\) is an acquisition function. The feasibility probability acts as a filter or penalty so that optimization does not repeatedly select experimentally impossible regions.

When several samples can be prepared in parallel, batch Bayesian optimization should be considered so that all recommendations do not collapse into one local neighborhood. The specific batch strategy is to be selected after the available dataset size and experimental throughput are confirmed.

## Evaluation plan

The key comparison is:

```text
Successful-data-only workflow
            versus
Successful + failed-data workflow
```

The comparison should use a time-ordered or leave-one-batch-out evaluation to avoid information leakage. Candidate metrics include:

| Question | Example metric |
|---|---|
| Does negative data reduce infeasible recommendations? | Fraction of recommended points in failed/high-risk regions |
| Does it improve the next experimental batch? | Feasible-success rate |
| Does it improve search efficiency? | Experiments required to reach a target property |
| Does it preserve useful exploration? | Coverage of the unexplored space and uncertainty reduction |
| Does it identify robust regions? | Performance over a neighborhood, not only at one point |

The central hypothesis is:

\[
\text{successful data only}
<
\text{successful data + historical failed data}
\]

with respect to candidate feasibility, search efficiency, or the number of experiments required to reach the target property.

## Publication-level contribution

The contribution should not be described as merely “reproducing an industrial platform.” The intended contribution is the combination of:

1. Systematic use of historical failed experiments as negative feasibility information.
2. Separate surrogate models for different material properties.
3. Integration of feasible regions and property-specific promising regions.
4. Recommendation of robust experimental ranges rather than only a single numerical optimum.
5. Quantitative comparison against a successful-data-only baseline.

## Required information before implementation

The following items should be filled in from the company dataset before the workflow is finalized:

- [ ] Definition of “successful experiment” and “failed experiment”.
- [ ] Failure categories and, if available, a failure-severity scale.
- [ ] Available composition and process variables.
- [ ] Target properties and units.
- [ ] Minimum valid measurement criteria for each property.
- [ ] Number of historical experiments and batch structure.
- [ ] Candidate experimental constraints and forbidden regions.
- [ ] Evaluation target and the experimental budget per iteration.

