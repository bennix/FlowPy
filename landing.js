const grid = document.querySelector('#lessonGrid');
const count = document.querySelector('#lessonCount');
const video = document.querySelector('#lessonVideo');
let lessons = [];
let category = 'all';
let selected = '001_starter';
const group = slug => {
  const week = Number(slug.slice(1, 3));
  if (!slug.startsWith('w')) return 'intro';
  return week <= 5 ? 'basics' : week <= 8 ? 'data' : 'advanced';
};
const label = slug => slug.startsWith('w') ? `WEEK ${Number(slug.slice(1, 3))}` : '入门';
const time = duration => `${Math.floor(duration / 60).toString().padStart(2, '0')}:${Math.floor(duration % 60).toString().padStart(2, '0')}`;
function render() {
  const query = document.querySelector('#lessonSearch').value.trim().toLowerCase();
  const visible = lessons.filter(item => (category === 'all' || group(item.slug) === category) && `${item.name} ${item.slug} ${label(item.slug)}`.toLowerCase().includes(query));
  count.textContent = `${visible.length} 个实例 / 选择一节，跟着搭建`;
  grid.replaceChildren();
  for (const item of visible) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'lesson-card';
    button.setAttribute('aria-pressed', String(item.slug === selected));
    button.setAttribute('aria-label', `观看 ${item.name}，${time(item.duration)}`);
    const top = document.createElement('span');
    top.className = 'card-top';
    top.textContent = `${label(item.slug)} / ${String(lessons.indexOf(item) + 1).padStart(2, '0')}`;
    const play = document.createElement('span');
    play.className = 'play-icon';
    play.textContent = item.slug === selected ? '◉' : '▷';
    top.append(play);
    const title = document.createElement('h3');
    title.textContent = item.name;
    const bottom = document.createElement('span');
    bottom.className = 'card-bottom';
    bottom.textContent = `${time(item.duration)} · ${item.steps} 步`;
    const badge = document.createElement('strong');
    badge.textContent = '已跑通 ↗';
    bottom.append(badge);
    button.append(top, title, bottom);
    button.addEventListener('click', () => selectLesson(item));
    grid.append(button);
  }
  if (!visible.length) {
    const empty = document.createElement('p');
    empty.textContent = '没有匹配的教程，试试其他关键词或分类。';
    grid.append(empty);
  }
}
function selectLesson(item) {
  selected = item.slug;
  video.pause();
  video.src = `videos/${item.slug}.mp4`;
  video.load();
  document.querySelector('#lessonTitle').textContent = item.name;
  document.querySelector('#lessonCategory').textContent = `${label(item.slug)} / ${time(item.duration)} / ${item.steps} 步`;
  document.querySelector('#downloadVideo').href = `videos/${item.slug}.mp4`;
  render();
  video.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'center'});
  video.play().catch(() => { /* Native controls remain available if autoplay is blocked. */ });
}
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
  category = button.dataset.filter;
  document.querySelectorAll('[data-filter]').forEach(tab => {
    tab.classList.toggle('active', tab === button);
    tab.setAttribute('aria-pressed', String(tab === button));
  });
  render();
}));
document.querySelector('#lessonSearch').addEventListener('input', render);
document.querySelector('#copyCommand').addEventListener('click', async event => {
  const button = event.currentTarget;
  try {
    await navigator.clipboard.writeText(document.querySelector('#installCommand').textContent);
    button.textContent = '已复制 ✓';
  } catch {
    button.textContent = '请选中下方命令复制';
  }
});
fetch('videos/manifest.json').then(response => {
  if (!response.ok) throw new Error('Manifest unavailable');
  return response.json();
}).then(data => { lessons = data; render(); }).catch(() => {
  count.textContent = '课程加载失败';
  document.querySelector('#lessonError').hidden = false;
});
