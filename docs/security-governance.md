# Qlik Security & Governance

This portfolio demonstrates the design boundary for application security without embedding real users, credentials or production authorization data.

## Section Access design

For a production Qlik Sense application, row-level reduction should be implemented with a dedicated Section Access table rather than hard-coded user rules inside the business model.

Example design:

```qlik
SECTION ACCESS;
LOAD
    Upper(UserId) as USERID,
    Upper(Role) as ACCESS,
    Upper(Region) as REGION
INLINE [
USERID, ROLE, REGION
INTERNAL\SA_SCHEDULER, ADMIN, *
USER1, USER, WEST
USER2, USER, SOUTH
];

SECTION APPLICATION;
```

The example is illustrative only. Real identities and authorization mappings must come from the organisation's controlled identity/access process.

## Reduction strategy

The reduction field must exist consistently in the application model. For regional security, `REGION` can reduce the associated fact/dimension records. If multiple reduction fields are used, their interaction must be explicitly tested because an incorrect association can expose more data than intended or remove legitimate access.

Security validation should include:

- authorized user can see only permitted rows
- user with multiple authorized regions receives the intended union of access
- unauthorized region is not selectable or visible through associated fields
- admin/service account behavior is explicitly defined
- null/blank reduction values cannot accidentally bypass the intended rule
- section-access fields are not exposed as ordinary application data unless intentionally required

## Sensitive data

Do not place credentials, API keys, passwords, real customer identifiers or production authorization mappings in this repository.

Where a field is sensitive but required for the model, apply the organisation's approved masking/tokenisation strategy upstream where possible. Security should not depend on hiding a field from a chart alone.

## Governance controls

Recommended production controls:

1. Git pull request review for load-script changes.
2. CI/static validation before promotion.
3. Separate DEV, TEST and PROD Qlik connections.
4. Controlled QMC application/task ownership.
5. Explicit Section Access review before production release.
6. Reload and DQ audit records retained according to operational policy.
7. No secrets committed to Git.
8. Documented rollback path.

## Important distinction

Section Access is an application authorization mechanism; it is not a replacement for source-system permissions, Qlik platform permissions, network controls or enterprise identity governance. Those layers should remain independently controlled.

## Portfolio scope

This repository provides the security design and a safe illustrative pattern. It does not claim that a production Section Access policy or real identity integration has been executed against a Qlik Sense environment.