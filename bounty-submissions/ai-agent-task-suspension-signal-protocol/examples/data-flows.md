# Example Data Flows

## Flow 1: Normal Task Suspension

1. Operator sends `suspend-task.json`.
2. Agent validates protocol, version, target, timestamps, and task scope.
3. Agent appends an audit record with `decision = accepted_suspend`.
4. Agent pauses only `task_42`.
5. Other unrelated tasks continue.

## Flow 2: Resume Suspended Task

1. Operator sends `resume-task.json` with the same `correlation_id`.
2. Agent validates the signal.
3. Agent appends an audit record with `decision = accepted_resume`.
4. Agent resumes `task_42` if no other active suspension applies.

## Flow 3: Expired Signal

1. Agent receives a `suspend` signal after `expires_at`.
2. Agent appends an audit record with `decision = rejected_expired`.
3. Agent does not alter runtime state.

## Flow 4: Capability Suspension

1. Policy engine sends a `suspend` signal scoped to `capability = browser_access`.
2. Agent pauses browser/tool calls.
3. Agent keeps reasoning and non-browser tasks active.
4. Operator or policy engine later sends `resume` for the same capability.

## Flow 5: Global Revoke

1. Legal authority sends `revoke` with `scope.type = agent`.
2. Agent records `accepted_revoke`.
3. Local policy decides whether the runtime must terminate, enter safe mode, or request custodian review.
