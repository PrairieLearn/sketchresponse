# Instructor labels in PrairieLearn

This document describes how SketchResponse's per-drawing labels are intended to integrate with [`pl-sketch`](https://docs.prairielearn.com/elements/pl-sketch/). The SketchResponse support is implemented here; the PrairieLearn attribute described below still needs a separate implementation. Current PrairieLearn does not copy a drawing's `label` into `SketchDrawing`, so the HTML example will not show labels until that integration is added.

## Question author interface

The proposed optional `label` attribute belongs on `pl-sketch-initial` and `pl-sketch-solution`, which already describe individual drawings. There is no `pl-sketch-drawing` element. The existing `label` on `pl-sketch-tool` continues to name the toolbar button; it does not label a curve on the canvas.

For example, this complete `question.html` would display two labelled reference functions on a static graph:

```html
<pl-sketch
  answers-name="reference"
  width="420"
  height="420"
  x-range="-2,2"
  y-range="-2,2"
  read-only="true"
>
  <pl-sketch-tool
    id="curves"
    type="spline"
    color="royalblue"
    read-only="true"
  ></pl-sketch-tool>
  <pl-sketch-initial
    tool-id="curves"
    coordinates="(-1,-1),(1,1)"
    label="f(x)"
  ></pl-sketch-initial>
  <pl-sketch-initial
    tool-id="curves"
    coordinates="(-1,1),(1,-1)"
    label="g(x)"
  ></pl-sketch-initial>
</pl-sketch>
```

Both curves use the same drawing tool but carry different labels. As an alternative to `coordinates`, a `spline` or `free-draw` drawing can use the existing `function="x" x-range="-1,1"` attributes. Sampling, coordinate conversion, and splitting at discontinuities continue to use `format_drawing`; only the first resulting segment receives the drawing's label.

The proposed attribute applies to `free-draw`, `spline`, and `polyline` drawings. A label is plain text unless the SketchResponse plugin explicitly configures LaTeX tags; this proposal does not expose a LaTeX option in PrairieLearn. Omitting the attribute preserves existing unlabelled drawings. The same attribute on `pl-sketch-solution` labels a solution in the answer panel and its solution overlay.

The canvas's `read-only` attribute makes the entire graph static. A tool's `read-only` attribute makes only that tool's drawings static, so a question can combine labelled reference curves with separate student drawing tools and grading criteria. The drawing's label itself is always read-only, including when its tool remains editable. It does not prevent moving or deleting an editable curve and is not an authorization mechanism for submitted data.

For an editable example, the proposed integration would also let students translate a given curve while keeping its name fixed:

```html
<p>Move the labelled curve up by one unit.</p>
<pl-sketch answers-name="translate" x-range="-2,2" y-range="-2,3">
  <pl-sketch-tool id="f" type="free-draw" limit="1"></pl-sketch-tool>
  <pl-sketch-initial
    tool-id="f"
    function="x"
    x-range="-1,1"
    label="f(x)"
  ></pl-sketch-initial>
  <pl-sketch-grade
    type="match-function"
    tool-id="f"
    function="x+1"
    x-range="-1,1"
  ></pl-sketch-grade>
  <pl-sketch-solution
    tool-id="f"
    function="x+1"
    x-range="-1,1"
    label="f(x)"
  ></pl-sketch-solution>
</pl-sketch>
```

Here `f(x)` labels the editable initial curve and the displayed solution. The proposed drawing attribute is independent of the tool's toolbar label and of any default tag for new curves.

## Conversion into SketchResponse configuration

The integration belongs in PrairieLearn's [`apps/prairielearn/elements/pl-sketch/pl-sketch.py`](https://github.com/PrairieLearn/PrairieLearn/blob/master/apps/prairielearn/elements/pl-sketch/pl-sketch.py):

1. `_check_tool` already converts `type="free-draw"` into the `freeform` plugin name; `spline` and `polyline` retain their names. It converts `read-only` into `readonly` and preserves the tool ID.
2. `_check_drawing`, shared by initial and solution drawings, should read the optional `label` and include it in the returned `SketchDrawing`. The PrairieLearn change must also validate supported drawing types and update the element's attribute validation and documentation. Existing drawings without a label must remain valid.
3. `prepare` already groups drawings by tool ID and calls `format_drawing(initials, tool_data[tool_id], ranges_config)`. No new grouping or drawing format is needed. Solutions follow the same path into `solution_state`.
4. `render` already serializes the client configuration for the element's JavaScript. Question panels use `initial_state`, answer panels use `solution_state`, and solution overlays reuse the formatted drawings with a read-only overlay plugin.

For the example, the two `_check_drawing` results would be:

```python
initials = [
    {
        "toolid": "curves",
        "coordinates": [-1.0, -1.0, 1.0, 1.0],
        "fun": None,
        "xrange": [-2.1, 2.1],
        "label": "f(x)",
    },
    {
        "toolid": "curves",
        "coordinates": [-1.0, 1.0, 1.0, -1.0],
        "fun": None,
        "xrange": [-2.1, 2.1],
        "label": "g(x)",
    },
]
```

PrairieLearn adds a 10-pixel margin to the requested graph ranges. Here its `ranges_config` has width and height 420 and both ranges expanded to `[-2.1, 2.1]`. Passing these drawings and the `curves` tool to `format_drawing` produces the following `initialstate` entry, in screen pixels (rounded here for readability):

```python
{
    "curves": [
        [
            {"x": 110.0, "y": 310.0, "tag": "f(x)", "tagReadonly": True},
            {"x": 310.0, "y": 110.0},
        ],
        [
            {"x": 110.0, "y": 110.0, "tag": "g(x)", "tagReadonly": True},
            {"x": 310.0, "y": 310.0},
        ],
    ]
}
```

The corresponding plugin has `name="spline"`, `id="curves"`, `color="royalblue"`, and `readonly=True`, without a `tag` configuration. The frontend renders `f(x)` and `g(x)` next to their respective first points using the default offsets `(5, -5)`. These first-point tags already flow through `getGradeable()`; no grader format change is needed. State serialization also preserves them when a submission is restored.

## Why extend the frontend's existing tags?

This feature reuses the existing first-point `tag`, SVG/KaTeX renderer, and gradeable tag field. It adds per-drawing display and editability rules rather than a second annotation system.

Before this change, the `freeform`, `spline`, and `polyline` plugins only rendered tags when the tool had a `tag` configuration. That configuration also supplies a default tag to every newly drawn curve. It cannot express “show only these instructor-provided labels, and leave new student curves unlabelled.” The frontend now renders a drawing's existing tag without requiring a tool-wide default; a shared renderer supplies offsets when the tool has none.

Tool-level `readonly` already prevents editing tags on a read-only tool. For the static example above, PrairieLearn could instead supply a tool-level `tag` configuration for placement and populate the existing first-point tags in Python, without changing the frontend. That narrower design is sufficient if labels are limited to read-only tools. Merely setting `tag.value` would still not populate the different tags on pre-drawn curves; their first points need their own values.

This PR also supports labelled initial drawings on editable tools, without requiring a separate tool for each label. Existing editable tags open an edit dialog in Select mode, so `tagReadonly` prevents that dialog for the instructor's label while retaining editing for ordinary student tags. It also gives fixed labels the default cursor. A tool-level tag configuration, when present, continues to control placement, LaTeX rendering, and the editable default for new student curves.

For editable spline or polyline initial drawings, the existing curve-completion issue tracked in [#45](https://github.com/PrairieLearn/sketchresponse/pull/45) is separate: before that fix, append an empty curve (`[]`) to the initial state so a new click starts another curve. The static example above does not need that workaround.
