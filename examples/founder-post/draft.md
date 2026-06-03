## Why do we deploy to production every day with a team of five?

Because waiting to "do it properly later" is how startups die slowly. Google's DORA research [1] found
that elite engineering teams deploy on demand — multiple times a day — while the lowest tier ships
roughly once a month or less. At Acme (five people) we copied the elite *habit* early, not the elite
headcount.

Three things made daily deploys safe at our size:

- **Trunk-based development** — short-lived branches, merged the same day.
- **One automated check that must pass** — not ten flaky ones nobody trusts.
- **A 30-second rollback**, so a bad deploy is a shrug, not a fire drill.

**Doesn't shipping faster just mean more bugs?** The opposite: the 2024 DORA report [1] links higher
deploy frequency with *better* stability, because smaller changes are easier to review and to revert.

If you still batch releases for a "big launch," try shipping one small thing to production today.

[1] https://dora.dev/research/
