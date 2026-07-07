# Callout Markup

Callouts are used to make practical and conceptual elements visually distinct in the generated PDF.

## Syntax

```markdown
:::key-idea
The producer's true medium is attention through time.
:::
```

```markdown
:::studio-mission
Create a ten-minute recording from one sound.
Do not add another instrument.
:::
```

```markdown
:::listening-exercise
Listen to a reference track and map where your attention moves.
:::
```

```markdown
:::deep-dive
This panel can hold a longer explanation of a concept.
:::
```

```markdown
:::avoid
Do not add another layer before asking what role is missing.
:::
```

## Planned Rendered Output

Each callout should become a styled box in the PDF with:

- a clear title,
- consistent padding,
- subtle background shading,
- reusable visual style,
- automatic spacing before and after.

## Use Cases

| Callout Type | Purpose |
|---|---|
| `key-idea` | Core principle |
| `studio-mission` | Practical assignment |
| `listening-exercise` | Critical listening task |
| `deep-dive` | Extended explanation |
| `avoid` | Common mistake or warning |
