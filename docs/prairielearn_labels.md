# Instructor tags in PrairieLearn

Instructor annotations use SketchResponse's existing tags. Each drawing supplies its `tag` string; its tool supplies placement and the host renders its content. The existing tool or canvas `read-only` setting makes a reference drawing and its annotation fixed.

## Authoring

`pl-sketch-initial` and `pl-sketch-solution` accept `tag` for every drawing type: `free-draw`, `spline`, `polyline`, `polygon`, `point`, `line`, `horizontal-line`, and `vertical-line`. `label` on `pl-sketch-tool` names its toolbar button.

A tagged initial drawing requires `read-only="true"` on its tool or canvas. Solution drawings are displayed read-only, so a tagged solution can refer to a tool that students use to draw their answer. Student-created drawings do not acquire default tags.

Tags use PrairieLearn's host MathJax renderer and its usual math delimiters. Plain text and mathematics can appear in the same tag, for example `tag="Reference \(f(x)\)"`; different drawings on one tool can independently contain text, math, or both.

For example, this question provides two fixed reference functions and asks the student to mark the origin:

```html
<pl-question-panel>
  <p>Mark the origin with the red point.</p>
</pl-question-panel>
<pl-sketch answers-name="graph" x-range="-2,2" y-range="-2,2">
  <pl-sketch-tool id="f" type="spline" read-only="true"></pl-sketch-tool>
  <pl-sketch-tool id="g" type="spline" read-only="true"></pl-sketch-tool>
  <pl-sketch-tool id="answer" type="point" color="red"></pl-sketch-tool>
  <pl-sketch-initial
    tool-id="f"
    function="x"
    x-range="-1,1"
    tag="Reference \(f(x)\)"
  ></pl-sketch-initial>
  <pl-sketch-initial
    tool-id="g"
    function="-x"
    x-range="-1,1"
    tag="Reference \(g(x)\)"
  ></pl-sketch-initial>
  <pl-sketch-grade type="match" tool-id="answer" x="0" y="0"></pl-sketch-grade>
  <pl-sketch-grade type="count" tool-id="answer" count="1"></pl-sketch-grade>
  <pl-sketch-solution
    tool-id="answer"
    coordinates="(0,0)"
    tag="Origin \(O\)"
  ></pl-sketch-solution>
</pl-sketch>
```

Each overlapping reference function has its own tool ID, preserving PrairieLearn's existing function-per-tool rules. Multiple tagged points or nonoverlapping curve segments can share a tool and its placement.

Tags use the existing first-point anchor for curves, polygons, points, and line segments. Horizontal and vertical line tags use the midpoint along the line. PrairieLearn supplies offsets `(5, -5)` and start alignment; geometry is still specified in graph coordinates.

## Conversion and ownership

The controller's `_check_drawing` reads `tag` into an optional `SketchDrawing.tag`. `prepare` groups drawings by their existing tool IDs and calls `format_drawing`. That function adds the tag to the relevant client-state point, without changing coordinates, grouping, or IDs. A symbolic function split at discontinuities receives one tag on its first nonempty segment.

For example, coordinates `(-1,-1),(1,1)` on a 420-pixel-square canvas with requested ranges `[-2,2]` produce this state, after PrairieLearn's existing 10-pixel margins (values rounded):

```python
{
    "f": [[
        {"x": 110.0, "y": 310.0, "tag": r"Reference \(f(x)\)"},
        {"x": 310.0, "y": 110.0},
    ]]
}
```

When this instructor state is displayed, the controller enables the existing tool-level placement configuration:

```python
{
    "name": "spline",
    "id": "f",
    "readonly": True,
    "tag": {
        "xoffset": 5,
        "yoffset": -5,
        "align": "start",
        "position": "start",
    },
}
```

That configuration is attached only to displayed instructor drawings. The frontend mounts stable HTML tag contents inside SVG `foreignObject` elements, asks the host to typeset newly mounted or changed content, and measures the result in canvas units. Coordinate and cursor updates retain the host-rendered DOM; removed tags are cleared from MathJax. A solution's tag configuration does not enable tags on the original editable tool. `getState()` and `getGradeable()` already preserve ordinary tag strings; there is no separate label object or per-point editing flag.

## Panel behavior

The controller composes each display from the saved instructor reference state and the relevant response state:

| View             | Drawings displayed                                                                                         |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| Question         | Fixed references plus initial or restored student drawings                                                 |
| Submission       | Fixed references plus the saved student drawings                                                           |
| Answer           | Fixed references plus solution drawings; a solution for the same tool replaces that tool's reference state |
| Solution overlay | Separate read-only solution instances over the question or submission                                      |

Fixed reference drawings are restored from the variant's canonical initial state, including when submitted data omits or changes them. Solution annotation nodes share their overlay's visibility, so hiding a solution hides its tags too.

Generated test answers preserve reference tags, but use only the geometry of editable-tool solutions as student responses. Thus solution-only annotations do not appear on simulated student drawings. Existing tool IDs and grading criteria retain their meanings.

All newly stored fields are optional. Existing variants and submissions without tag settings continue to render. The example-course `sketchTags` question and the real PrairieLearn browser tests exercise the full authoring, rendering, submission, answer, and overlay path with the built packages.
