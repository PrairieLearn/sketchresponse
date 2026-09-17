const config = {
  width: 800,
  height: 450,
  xrange: [-4, 4],
  yrange: [-2.25, 2.25],
  enforceBounds: true,
  plugins: [
    { name: 'axes', id: 'axes' },
    { name: 'point', id: 'p' },
    { name: 'line-segment', id: 'line' },
    {
      name: 'group',
      id: 'curves',
      label: 'Curves',
      plugins: [
        { name: 'polyline', id: 'poly' },
        { name: 'spline', id: 'spline' },
      ],
    },
    { name: 'freeform', id: 'free' },
  ],
};

function embed(target, id, options) {
  const container = document.createElement('div');
  container.id = `${id}-si-container`;
  container.className = 'si-container';
  container.tabIndex = 0;
  document.getElementById(target).append(container);
  return new window.sketchresponse.default(container, id, options);
}

embed('question', 'question', config);
const submission = embed('submission', 'submission', {
  ...config,
  readonly: true,
  plugins: [
    ...config.plugins,
    {
      name: 'line-segment',
      id: 'solution',
      readonly: true,
      overlay: true,
      color: 'green',
    },
  ],
  initialstate: {
    p: [{ x: 400, y: 225 }],
    solution: [
      { x: 200, y: 350 },
      { x: 600, y: 100 },
    ],
    line: [
      { x: 200, y: 325 },
      { x: 600, y: 125 },
    ],
  },
});

embed('all-tools', 'all-tools', {
  ...window.loadConfig('allPlugins'),
  width: config.width,
  height: config.height,
});

submission.messageBus.on('ready', () => {
  const wrapper = document.createElement('div');
  wrapper.className = 'position-relative';
  wrapper.innerHTML = `
    <button
      id="overlay-toggle"
      type="button"
      class="js-overlay-toggle btn btn-light border border-dark position-absolute translate-middle bottom-0 end-0 m-3"
      title="Toggle solution display"
      aria-label="Toggle solution display"
      aria-pressed="true"
    >
      <i class="bi bi-layers-fill" aria-hidden="true"></i>
    </button>
  `;
  submission.el.append(wrapper);
  const overlayToggle = wrapper.querySelector('button');
  overlayToggle.addEventListener('click', () => {
    const visible = overlayToggle.getAttribute('aria-pressed') !== 'true';
    overlayToggle.setAttribute('aria-pressed', String(visible));
    submission.el.querySelectorAll('.overlay').forEach((el) => {
      el.style.display = visible ? '' : 'none';
    });
    const icon = overlayToggle.querySelector('i');
    icon.classList.toggle('bi-layers-fill', visible);
    icon.classList.toggle('bi-layers-half', !visible);
  });
});
