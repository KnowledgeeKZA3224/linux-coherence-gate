# Mirror Contract

The release artifact hash is the identity.

For each release, publish the exact same bytes and record:

- source commit SHA;
- artifact SHA-256;
- release timestamp;
- mirror location;
- independent verification result.

Recommended mirror classes:

1. GitHub Release for ordinary discovery.
2. Approved object storage for operational availability.
3. Optional content-addressed storage such as IPFS or Arweave for immutable public reference.

A mirror is valid only when its downloaded artifact hashes to the canonical release digest. A different digest is a different artifact and must never inherit the original release identity.
