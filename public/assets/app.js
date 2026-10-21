
(function () {
  'use strict';

  const SOURCE_TITLE = {
    anthropic_news:       'Anthropic News',
    anthropic_research:   'Anthropic Research',
    cookbook:             'Claude Cookbook',
    transformer_circuits: 'Transformer Circuits',
    red_team:             'Red Team',
    claude_blog:          'Claude Blog',
    alignment:            'Alignment Science',
    engineering:          'Engineering Blog',
    references:           'References',
  };

  const SOURCE_URL = {
    anthropic_news:       'https://www.anthropic.com/news',
    anthropic_research:   'https://www.anthropic.com/research',
    cookbook:             'https://platform.claude.com/cookbook',
    transformer_circuits: 'https://transformer-circuits.pub',
    red_team:             'https://www.anthropic.com/research/team/frontier-red-team',
    claude_blog:          'https://claude.com/resources/articles',
    alignment:            'https://alignment.anthropic.com',
    engineering:          'https://www.anthropic.com/engineering',
  };

  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function fmtDate(s) {
    // "2026-04-09" → { year:"2026年", day:"04月09日" }
    if (!s) return { year: '日期待确认', day: '发布日未提供' };
    const p = s.split('-');
    return { year: p[0], day: Number(p[1]) + '月' + Number(p[2]) + '日' };
  }

  function cardHtml(a) {
    const hasZh = a.title_zh && a.title_zh !== a.title_en;
    const hasSummary = a.summary_status === 'ready' && a.summary_zh?.trim().length > 5;
    return `<article class="article-card">
      <div class="article-meta"><span class="source-mark" aria-hidden="true"></span>${esc(a.source || SOURCE_TITLE[a.source_key] || '')}<span class="excerpt-label">中文摘录</span></div>
      <h3 class="article-title"><a href="${safeUrl(a.url)}" target="_blank" rel="noopener noreferrer">${esc(hasZh ? a.title_zh : a.title_en)}</a></h3>
      ${hasZh ? `<p class="title-en" lang="en">${esc(a.title_en)}</p>` : ''}
      <p class="card-summary${hasSummary ? '' : ' is-empty'}">${hasSummary ? esc(a.summary_zh.replace(/^【机器翻译摘要】\n?/, '')) : (a.summary_status === 'failed' ? '摘录暂未生成成功，下次更新时会重试。你可以先阅读原文。' : '中文摘录正在准备，你可以先阅读原文。')}</p>
      <a class="read-link" href="${safeUrl(a.url)}" target="_blank" rel="noopener noreferrer">阅读原文 <span aria-hidden="true">↗</span></a>
    </article>`;
  }

  function safeUrl(value) {
    try { const url = new URL(value); return /^https?:$/.test(url.protocol) ? esc(url.href) : '#'; }
    catch { return '#'; }
  }

  function digestsHtml(digests) {
    if (!digests || !digests.length) return '<div class="empty-state"><h3>没有找到匹配的文章</h3><p>试试其他关键词，或切换来源。</p><button class="text-button" data-reset>清除筛选</button></div>';
    return digests.map(day => {
      const { year, day: d } = fmtDate(day.date);
      return `
<section class="date-section">
  <div class="date-heading">
    <h2 class="date-pill">
      <span class="date-year">${esc(year)}</span>
      <span class="date-day">${esc(d)}</span>
    </h2>
    <div class="date-rule"></div>
    <span class="date-count">${day.articles.length} 篇</span>
  </div>
  <div class="cards-grid">${day.articles.map(cardHtml).join('')}</div>
</section>`;
    }).join('');
  }

  function staticRefsHtml(refs) {
    if (!refs || !refs.length) return '';
    const cards = refs.flatMap(group => group.items || []).map(it => `
<div class="constitution-wrap">
  <a class="constitution-card" href="${safeUrl(it.url)}" target="_blank" rel="noopener noreferrer">
    <div class="constitution-body">
      <div class="constitution-icon">§</div>
      <div class="constitution-text">
        <div class="constitution-eyebrow">Foundational Document</div>
        <div class="constitution-title">${esc(it.title)}</div>
        <div class="constitution-desc">${esc(it.desc)}</div>
      </div>
    </div>
    <div class="constitution-arrow">
      <span class="constitution-cta">阅读原文 →</span>
    </div>
  </a>
</div>`).join('');
    return cards;
  }

  function archiveHtml(allUrls, orderArr) {
    const order = orderArr || Object.keys(allUrls);
    return order.filter(k => allUrls[k] && allUrls[k].length).map(key => {
      const items = allUrls[key] || [];
      const desc  = items[0] ? items[0].desc : '';
      const title = SOURCE_TITLE[key] || key;
      const links = items.map(it =>
        `<li><a href="${safeUrl(it.url)}" target="_blank" rel="noopener noreferrer">${esc(it.title || it.url)}</a>${it.date ? `<span class="archive-date">${esc(it.date)}</span>` : ''}</li>`
      ).join('');
      return `
<section class="archive-group">
  <div class="archive-group-meta">
    <h2 class="archive-group-title">
      ${SOURCE_URL[key]
        ? `<a href="${esc(SOURCE_URL[key])}" target="_blank" rel="noopener noreferrer">${esc(title)}</a>`
        : esc(title)}
    </h2>
    <p class="archive-desc">${esc(desc)}</p>
  </div>
  <ul class="archive-list">${links || '<li>暂无数据</li>'}</ul>
</section>`;
    }).join('');
  }


  const state = { source: '', query: '', view: 'latest' };
  let feedData;
  let changesPromise;
  const sourceKeys = Object.keys(SOURCE_URL);
  const main = document.getElementById('js-main');
  const result = document.getElementById('js-results');
  const search = document.getElementById('js-search');

  function humanTime(value) {
    if (!value) return '尚无成功更新记录';
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return '更新时间待确认';
    const parts = Object.fromEntries(new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(d).map(p => [p.type, p.value]));
    return `${parts.month}月${parts.day}日 ${parts.hour}:${parts.minute}`;
  }

  function matches(item) {
    const text = [item.title, item.title_en, item.title_zh, item.summary_zh, item.url].filter(Boolean).join(' ').toLocaleLowerCase();
    return !state.query || text.includes(state.query.toLocaleLowerCase());
  }

  function sourceButtons() {
    const counts = Object.fromEntries(sourceKeys.map(key => [key, state.view === 'archive'
      ? (feedData.all_urls?.[key] || []).length
      : (feedData.digests || []).flatMap(d => d.articles).filter(a => a.source_key === key).length]));
    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    document.getElementById('js-sources').innerHTML = [['', '全部来源'], ...sourceKeys.map(key => [key, SOURCE_TITLE[key]])].map(([key, title]) => `<button class="source-button${state.source === key ? ' active' : ''}" data-source="${key}" aria-pressed="${state.source === key}"><span>${esc(title)}</span><span class="source-count">${key ? counts[key] : total}</span></button>`).join('');
  }

  function healthHtml() {
    const h = feedData.health;
    if (!h) return '<span class="sync-label">更新状态待确认</span>';
    const c = h.summary_coverage || {};
    const ok = h.status === 'ok' && !c.failed;
    return `<details class="health-panel"><summary><span class="status-dot ${ok ? '' : 'warn'}"></span><span>${ok ? '内容已更新' : '部分内容待更新'}</span><span class="sync-time">${humanTime(h.last_success_at)}</span><span class="chevron" aria-hidden="true">⌄</span></summary>
      <div class="health-body"><div class="health-overview"><strong>${esc(c.ready ?? 0)}<small> / ${esc(c.total ?? 0)} 篇</small></strong><span>已有中文摘录</span><span class="coverage">${Math.round((c.ratio || 0) * 100)}%</span></div>
      <p class="health-note">待生成 ${esc(c.pending ?? 0)} 篇 · 暂时失败 ${esc(c.failed ?? 0)} 篇</p>
      <ul>${Object.entries(h.sources || {}).map(([key, info]) => `<li><span>${esc(SOURCE_TITLE[key] || key)}</span><span class="source-status ${info.status === 'ok' ? '' : 'warn-text'}">${info.status === 'ok' ? '正常' : '待恢复'}</span></li>`).join('')}</ul>
      <p class="health-note">最近成功更新：${esc((h.last_success_at || '').slice(0, 4))}年${humanTime(h.last_success_at)} · UTC+8</p><p class="health-note">摘录：机器翻译</p></div></details>`;
  }

  function renderFeed() {
    sourceButtons();
    const days = (feedData.digests || []).map(day => ({ ...day, articles: day.articles.filter(a => (!state.source || a.source_key === state.source) && matches(a)) })).filter(day => day.articles.length);
    const all = Object.fromEntries(Object.entries(feedData.all_urls || {}).map(([key, items]) => [key, (!state.source || key === state.source) ? items.filter(matches) : []]));
    const count = state.view === 'archive' ? Object.values(all).reduce((n, a) => n + a.length, 0) : days.reduce((n, d) => n + d.articles.length, 0);
    document.getElementById('js-result-count').textContent = `${count} 篇文章`;
    result.innerHTML = state.view === 'archive'
      ? (count ? archiveHtml(all, feedData.archive_order) : digestsHtml([])) + ((!state.source && !state.query) ? staticRefsHtml(feedData.static_refs || []) : '')
      : digestsHtml(days);
  }

  async function renderChanges() {
    result.innerHTML = '<div class="loading-state">正在载入更新记录…</div>';
    try {
      changesPromise ||= fetch('./changelog.json').then(r => { if (!r.ok) throw new Error('load'); return r.json(); }).catch(e => { changesPromise = null; throw e; });
      const entries = await changesPromise;
      if (state.view !== 'updates') return;
      result.innerHTML = `<div class="release-list">${entries.map((entry, i) => `<article class="release"><div class="release-meta"><time datetime="${esc(entry.date)}">${esc(entry.date.replaceAll('-', '.'))}</time><span class="release-type">${esc(entry.type)}</span>${i === 0 ? '<span class="release-latest">最新</span>' : ''}</div><h2>${esc(entry.title)}</h2><ul>${entry.changes.map(change => `<li>${esc(change)}</li>`).join('')}</ul></article>`).join('')}</div>`;
    } catch {
      if (state.view === 'updates') result.innerHTML = '<div class="empty-state"><h3>更新记录暂时无法载入</h3><button class="text-button" data-retry-changes>重新加载</button></div>';
    }
  }

  function route() {
    state.view = ['archive', 'updates'].includes(location.hash.slice(1)) ? location.hash.slice(1) : 'latest';
    const updates = state.view === 'updates';
    document.querySelectorAll('[data-view]').forEach(a => { const active = a.dataset.view === state.view; a.classList.toggle('active', active); if (active) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
    document.getElementById('js-sidebar').hidden = updates;
    document.getElementById('js-toolbar').hidden = updates;
    main.classList.toggle('updates-view', updates);
    const titles = { latest: '最新动态', archive: '文章归档', updates: '网站更新记录' };
    document.getElementById('js-page-title').textContent = titles[state.view];
    document.title = `${titles[state.view]} · Anthropic 资讯日报`;
    if (updates) renderChanges(); else renderFeed();
  }

  async function init() {
    try {
      const res = await fetch('./data.json');
      if (!res.ok) throw new Error('load');
      feedData = await res.json();
      document.getElementById('js-health').innerHTML = healthHtml();
      document.getElementById('js-toolbar').hidden = false;
      route();
    } catch (err) {
      result.innerHTML = '<div class="empty-state"><h2>连接暂时中断</h2><p>文章仍保存在网站上，重新加载即可再次尝试。</p><button class="text-button" data-reload>重新加载</button></div>';
      console.error(err);
    }
  }

  search.addEventListener('input', () => { state.query = search.value.trim(); renderFeed(); });
  document.addEventListener('click', event => {
    const panel = document.querySelector('.health-panel');
    if (panel?.open && !panel.contains(event.target)) panel.open = false;
    const button = event.target.closest('[data-source]');
    if (button) { state.source = button.dataset.source; renderFeed(); document.querySelector(`[data-source="${state.source}"]`)?.focus({ preventScroll: true }); }
    if (event.target.closest('[data-reset]')) { state.source = ''; state.query = ''; search.value = ''; renderFeed(); search.focus(); }
    if (event.target.closest('[data-reload]')) init();
    if (event.target.closest('[data-retry-changes]')) renderChanges();
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape') { const panel = document.querySelector('.health-panel'); if (panel?.open) { panel.open = false; panel.querySelector('summary').focus(); } } });
  window.addEventListener('hashchange', () => { if (feedData && ['', '#latest', '#archive', '#updates'].includes(location.hash)) { route(); window.scrollTo({ top: 0, behavior: 'instant' }); document.getElementById('js-page-title').focus({ preventScroll: true }); } });
  const fab = document.getElementById('js-fab');
  fab.addEventListener('click', () => window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }));
  window.addEventListener('scroll', () => { fab.hidden = window.scrollY < 500; }, { passive: true });
  init();
})();
