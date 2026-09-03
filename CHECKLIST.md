# Shirakami OS Change Boundary Checklist

## Change
- [ ] Issue scope confirmed
- [ ] Existing implementation audited
- [ ] Exact change surface identified
- [ ] Branch created before file changes
- [ ] One change only

## Theory / Protocol Boundary
- [ ] No theory extension
- [ ] No silent Protocol expansion
- [ ] Existing contract remains authoritative

## Agent Boundary
- [ ] Agent responsibility boundary preserved
- [ ] No automatic repair
- [ ] No automatic merge
- [ ] No automatic theory change
- [ ] Human final judgment remains human

## Evidence / Uncertainty
- [ ] Evidence is preserved
- [ ] Evidence is not rewritten
- [ ] Uncertainty is not silently converted to fact
- [ ] Observable result is recorded

## Verification
- [ ] Test added or updated for this change
- [ ] CI passes
- [ ] Scope-expansion check passes
- [ ] Rework is recorded if it occurs

## Merge / Closure
- [ ] PR reviewed
- [ ] Merge performed only after verification
- [ ] Post-merge CI verified
- [ ] Issue updated with evidence
- [ ] Next action is explicitly identified

## Transparency Rule
Every checked item must be explainable from repository evidence. The checklist must not replace evidence, judgment, or the underlying Protocol.
