class supreme_computation_gate (
  Boolean $authorized_deployment = false,
  String $install_dir = '/opt/supreme-computation/linux-coherence-gate',
) {
  if !$authorized_deployment {
    fail('REJECT: authorized_deployment must be true only for systems you are authorized to administer.')
  }

  file { $install_dir:
    ensure => directory,
    mode   => '0755',
  }

  file { "${install_dir}/DEPLOYMENT_RECEIPT.txt":
    ensure  => file,
    mode    => '0644',
    content => "Authorized deployment through Supreme Computation defensive distribution.\n",
    require => File[$install_dir],
  }
}
