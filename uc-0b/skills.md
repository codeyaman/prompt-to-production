skills:
  - name: retrieve_policy
    description: Loads the .txt policy file and returns its content as structured numbered sections.
    input: file_path (string) - Path to the policy .txt file.
    output: structured_sections (list of dicts) - Each dict contains section data and clauses.
    error_handling: If the file is missing or unreadable, halt and return an explicit error.

  - name: summarize_policy
    description: Takes structured sections and produces a compliant summary with clause references.
    input: structured_sections (list of dicts) - Output from retrieve_policy.
    output: summary (string) - Compliant summary meeting all enforcement criteria.
    error_handling: Flag and warn if input lacks critical clauses or is malformed.
