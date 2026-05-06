package kubernetes.security

deny[msg] {
  input.kind == "Pod"
  container := input.spec.containers[_]
  container.securityContext.privileged == true
  msg := sprintf("container %s is privileged", [container.name])
}

deny[msg] {
  input.kind == "Pod"
  input.spec.volumes[_].hostPath
  msg := "hostPath volumes are not allowed"
}

deny[msg] {
  input.kind == "Pod"
  container := input.spec.containers[_]
  not container.securityContext.runAsNonRoot
  msg := sprintf("container %s must set runAsNonRoot", [container.name])
}

deny[msg] {
  input.kind == "Pod"
  container := input.spec.containers[_]
  container.securityContext.allowPrivilegeEscalation == true
  msg := sprintf("container %s allows privilege escalation", [container.name])
}
