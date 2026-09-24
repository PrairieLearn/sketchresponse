// Stored geometry uses the configured canvas dimensions, regardless of display size.
export default function pointerPosition(svg, event) {
  const point = svg.createSVGPoint();
  point.x = event.clientX;
  point.y = event.clientY;
  const { x, y } = point.matrixTransform(svg.getScreenCTM().inverse());
  return { x, y };
}
