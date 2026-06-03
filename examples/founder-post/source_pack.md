# Source pack — daily deploys at a 5-person startup (illustrative)

> Illustrative example. The source is a real public research page; figures are
> rounded/paraphrased for the example — replace with your own sourced facts.

## Facts
- Google's DORA program groups software teams into performance tiers by their delivery + stability metrics — https://dora.dev/research/ (2024)
- Elite performers deploy on demand (multiple times per day); the lowest tier deploys roughly once per month or less — https://dora.dev/research/ (2024)
- DORA finds higher deployment frequency goes with *better* stability for top teams, not worse — https://dora.dev/research/ (2024)

## Numbers
- Elite: multiple deploys/day vs low: ~1 deploy/month (DORA tiers)
- 30-second rollback target (team practice, illustrative)

## Audience questions
- Doesn't shipping faster just mean more bugs?
- How do 5 people deploy daily without breaking things?
- What has to be true before daily deploys are safe?
- Is trunk-based development worth it at small scale?
- When should a startup invest in deploy automation?

## Competitor gaps
- "Move fast" posts repeat the slogan but skip the concrete enablers (trunk-based dev, one trustworthy gate, fast rollback).

## Founder angle
- Adopt the elite *habit* — small, frequent, reversible changes — early. It is a practice, not a headcount.
