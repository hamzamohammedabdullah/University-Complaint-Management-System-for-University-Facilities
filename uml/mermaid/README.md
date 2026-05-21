# Mermaid diagrams for UniCMS

This folder contains Mermaid (.mmd) files representing class diagrams, sequence diagrams, component diagrams, use-cases, dataflow diagrams and the complaint lifecycle statechart.

Files:
- `accounts_class.mmd`, `complaints_class.mmd` — class diagrams
- `seq_*.mmd` — sequence diagrams for login, register, submit complaint, notifications
- `components.mmd` — component diagram
- `usecases.mmd` — use-case flowchart
- `dataflow.mmd` — dataflow diagram
- `complaint_lifecycle.mmd` — statechart for complaint lifecycle

Render options:
1. VS Code: install the 'Markdown Preview Mermaid Support' or 'Mermaid Preview' extensions and open the `.mmd` file.
- CLI: install `@mermaid-js/mermaid-cli` (node) and run:

```powershell
npm install -g @mermaid-js/mermaid-cli
mmdc -i accounts_class.mmd -o accounts_class.png
```

If you need SVG or PDF output, mmdc supports `-t` and `-w` flags; see Mermaid CLI docs.

If you want, I can render these into PNG/SVG here (requires installing Node/npm dependencies) and include them in the `uml/output/` folder.
2. Open mermaid.live on your browser, copy and paste the individual codes to get the rendered image
