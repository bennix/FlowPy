const fallbackLessons = [
  {
    "slug": "001_starter",
    "name": "订单解析工作流",
    "duration": 181.154667,
    "steps": 16,
    "verified": true,
    "group": null
  },
  {
    "slug": "002_starter",
    "name": "批量抽取与匿名函数",
    "duration": 129.921333,
    "steps": 12,
    "verified": true,
    "group": null
  },
  {
    "slug": "003_starter",
    "name": "函数定义与灵活调用",
    "duration": 114.454667,
    "steps": 10,
    "verified": true,
    "group": null
  },
  {
    "slug": "004_starter",
    "name": "正则谓词过滤",
    "duration": 111.721333,
    "steps": 10,
    "verified": true,
    "group": null
  },
  {
    "slug": "w02_bmi",
    "name": "BMI 计算器",
    "duration": 92.921333,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w02_interactive",
    "name": "交互式 BMI / input()",
    "duration": 80.321333,
    "steps": 7,
    "verified": true,
    "group": null
  },
  {
    "slug": "w02_types_operators",
    "name": "基础类型与运算符",
    "duration": 93.288,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w03_ai_debug_log",
    "name": "AI 调试日志：三次失败与修正",
    "duration": 94.654667,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w04_exceptions_logs",
    "name": "异常捕获与打印调试",
    "duration": 115.354667,
    "steps": 10,
    "verified": true,
    "group": null
  },
  {
    "slug": "w05_guess_number",
    "name": "猜数字游戏：难度与循环",
    "duration": 80.788,
    "steps": 7,
    "verified": true,
    "group": null
  },
  {
    "slug": "w05_loop_early_exit",
    "name": "循环中的 continue / break",
    "duration": 91.688,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w06_gradebook_list",
    "name": "学生成绩管理：列表与元组",
    "duration": 94.054667,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w07_gradebook_dict",
    "name": "学生成绩管理：字典与集合",
    "duration": 94.088,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w07_lookup_comparison",
    "name": "列表和字典的查找对比",
    "duration": 93.488,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w08_contacts_regex",
    "name": "标准库：提取邮箱与手机号",
    "duration": 144.654667,
    "steps": 13,
    "verified": true,
    "group": null
  },
  {
    "slug": "w08_import_math",
    "name": "模块导入与函数属性",
    "duration": 87.088,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w08_loan",
    "name": "标准库：等额本息月供",
    "duration": 93.554667,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w08_lottery",
    "name": "标准库：双色球号码",
    "duration": 93.488,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w08_string_constants",
    "name": "标准库：string 与可重复随机字符串",
    "duration": 70.254667,
    "steps": 6,
    "verified": true,
    "group": null
  },
  {
    "slug": "w09_lambda_higher_order",
    "name": "Lambda 与高阶 map / filter",
    "duration": 154.321333,
    "steps": 14,
    "verified": true,
    "group": null
  },
  {
    "slug": "w09_salary_functions",
    "name": "薪资计算器：完整函数签名",
    "duration": 115.288,
    "steps": 10,
    "verified": true,
    "group": null
  },
  {
    "slug": "w10_modular_gradebook",
    "name": "模块化重构：成绩管理",
    "duration": 108.854667,
    "steps": 10,
    "verified": true,
    "group": null
  },
  {
    "slug": "w10_nested_subgraph",
    "name": "模块化重构：可视化子图",
    "duration": 163.554667,
    "steps": 15,
    "verified": true,
    "group": null
  },
  {
    "slug": "w11_basic_pandas",
    "name": "基础 pandas：表格清洗与筛选",
    "duration": 94.421333,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w11_csv_json_roundtrip",
    "name": "文件读写：CSV 与 JSON",
    "duration": 94.521333,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "w11_survey_collection",
    "name": "问卷收集：校验、去重与保存",
    "duration": 94.421333,
    "steps": 8,
    "verified": true,
    "group": null
  },
  {
    "slug": "feature_execution_trace",
    "name": "运行路径：节点与连线高亮",
    "duration": 171.454667,
    "steps": 8,
    "verified": true,
    "group": "features"
  },
  {
    "slug": "feature_edge_preview",
    "name": "局部调试：连线中间数据预览",
    "duration": 177.288,
    "steps": 9,
    "verified": true,
    "group": "features"
  },
  {
    "slug": "feature_extensions",
    "name": "扩展生态：第三方库与模块导入",
    "duration": 171.288,
    "steps": 9,
    "verified": true,
    "group": "features"
  }
];
const grid = document.querySelector('#lessonGrid');
const count = document.querySelector('#lessonCount');
const video = document.querySelector('#lessonVideo');
let lessons = [];
let category = 'all';
let selected = '001_starter';
const group = item => {
  if (item.group === 'features') return 'features';
  const slug = item.slug;
  const week = Number(slug.slice(1, 3));
  if (!slug.startsWith('w')) return 'intro';
  return week <= 5 ? 'basics' : week <= 8 ? 'data' : 'advanced';
};
const label = slug => slug.startsWith('w') ? `WEEK ${Number(slug.slice(1, 3))}` : '入门';
const time = duration => `${Math.floor(duration / 60).toString().padStart(2, '0')}:${Math.floor(duration % 60).toString().padStart(2, '0')}`;
function render() {
  const query = document.querySelector('#lessonSearch').value.trim().toLowerCase();
  const visible = lessons.filter(item => (category === 'all' || group(item) === category) && `${item.name} ${item.slug} ${label(item.slug)}`.toLowerCase().includes(query));
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
  // A landing page opened directly from disk has a null origin and cannot fetch JSON.
  // Keep all tutorial cards usable in that common preview mode.
  lessons = fallbackLessons;
  render();
});
