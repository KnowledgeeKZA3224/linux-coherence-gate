# Deployment Boundary

This distribution is for defensive administration of systems the operator owns or is explicitly authorized to manage.

Required boundary conditions:

- no silent or deceptive installation;
- no hidden embedding in unrelated packages;
- no credential bypass;
- no propagation to unapproved hosts;
- no persistence mechanism outside the administrator's declared configuration;
- every release must retain its source commit, hash manifest, and verification receipt.

The distribution may use ordinary administration systems such as Ansible or Puppet only when their inventories and targets are explicitly controlled by an authorized administrator.
