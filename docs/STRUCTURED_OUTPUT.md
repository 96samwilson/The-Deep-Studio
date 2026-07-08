# Structured Output

Future generations should return JSON instead of prose.

Example:

```json
{
  "files":[
    {
      "path":"book/example.md",
      "content":"# Example"
    }
  ]
}
```

This enables deterministic writing into the repository.
