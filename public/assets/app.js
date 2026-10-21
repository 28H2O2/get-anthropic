
(function () {
  'use strict';

  const LANGUAGE_KEY = 'anthropic-daily-language';
  const COPY = {
    zh: {
      skip: '跳到正文', brand: '资讯日报', home: 'Anthropic 资讯日报首页', navigation: '主导航',
      latest: '最新动态', archive: '文章归档', updatesNav: '网站更新', updates: '网站更新记录',
      filterSources: '按来源筛选', browseSources: '浏览来源', siteName: 'Anthropic 资讯日报',
      searchPlaceholder: '搜索标题或内容…', search: '搜索标题或内容', loadingArticles: '正在载入文章…', backTop: '回到顶部',
      allSources: '全部来源', unknownYear: '日期待确认', unknownDate: '发布日未提供',
      excerptZh: '中文摘录', excerptEn: '英文原文摘录', readOriginal: '阅读原文',
      summaryFailed: '摘录暂未生成成功，下次更新时会重试。你可以先阅读原文。',
      summaryPending: '中文摘录正在准备，你可以先阅读原文。',
      originalPending: '英文原文摘录正在准备，你可以先阅读原文。',
      noResults: '没有找到匹配的文章', tryFilters: '试试其他关键词，或切换来源。', clearFilters: '清除筛选',
      articles: n => `${n} 篇`, articleCount: n => `${n} 篇文章`, noData: '暂无数据',
      noSuccess: '尚无成功更新记录', unknownTime: '更新时间待确认', unknownHealth: '更新状态待确认',
      updated: '内容已更新', partial: '部分内容待更新', readyLabel: '已有中文摘录',
      pendingFailed: (pending, failed) => `待生成 ${pending} 篇 · 暂时失败 ${failed} 篇`,
      healthy: '正常', recovering: '待恢复', lastSuccess: '最近成功更新', translationNote: '摘录：机器翻译',
      loadingChanges: '正在载入更新记录…', newest: '最新', changesFailed: '更新记录暂时无法载入', reload: '重新加载',
      feedFailed: '连接暂时中断', feedRetry: '文章仍保存在网站上，重新加载即可再次尝试。',
      foundational: '基础文档', constitutionDesc: 'Claude 的价值观与行为准则',
      description: '每天汇集 Anthropic 官方研究、产品与工程进展，提供中文摘录与原文归档。',
    },
    en: {
      skip: 'Skip to content', brand: 'News daily', home: 'Anthropic News Daily home', navigation: 'Main navigation',
      latest: 'Latest', archive: 'Archive', updatesNav: 'Updates', updates: 'Website updates',
      filterSources: 'Filter by source', browseSources: 'Browse sources', siteName: 'Anthropic News Daily',
      searchPlaceholder: 'Search titles or content…', search: 'Search titles or content', loadingArticles: 'Loading articles…', backTop: 'Back to top',
      allSources: 'All sources', unknownYear: 'Date unconfirmed', unknownDate: 'Publication date unavailable',
      excerptZh: 'Chinese excerpt', excerptEn: 'Original excerpt', readOriginal: 'Read original',
      summaryFailed: 'The excerpt could not be generated. We will retry on the next update. You can read the original article now.',
      summaryPending: 'The Chinese excerpt is being prepared. You can read the original article now.',
      originalPending: 'The original excerpt is being prepared. You can read the full article now.',
      noResults: 'No matching articles', tryFilters: 'Try another search or choose a different source.', clearFilters: 'Clear filters',
      articles: n => `${n} ${n === 1 ? 'article' : 'articles'}`, articleCount: n => `${n} ${n === 1 ? 'article' : 'articles'}`, noData: 'No articles yet',
      noSuccess: 'No successful update yet', unknownTime: 'Update time unconfirmed', unknownHealth: 'Update status unconfirmed',
      updated: 'Content updated', partial: 'Some content pending', readyLabel: 'Chinese excerpts',
      pendingFailed: (pending, failed) => `Pending ${pending} · Failed ${failed}`,
      healthy: 'Healthy', recovering: 'Unavailable', lastSuccess: 'Last successful update', translationNote: 'Chinese excerpts: machine translated',
      loadingChanges: 'Loading updates…', newest: 'Latest', changesFailed: 'Unable to load updates', reload: 'Try again',
      feedFailed: 'Unable to load articles', feedRetry: 'Your articles are still available. Try loading them again.',
      foundational: 'Foundational document', constitutionDesc: "Claude’s values and guiding principles",
      description: 'Follow official Anthropic research, product, and engineering news, with article excerpts and an archive of original sources.',
    },
  };

  const SOURCE_DESCRIPTION_EN = {
    anthropic_news: 'Official news and product announcements',
    anthropic_research: 'Research papers and technical articles',
    cookbook: 'Official development examples and tutorials',
    transformer_circuits: 'Interpretability research from the Anthropic Circuits team',
    red_team: 'Frontier Red Team security research',
    claude_blog: 'Claude articles for individuals and businesses',
    alignment: 'Alignment science research',
    engineering: 'Engineering practices at Anthropic',
  };

  function initialLanguage() {
    const requested = new URLSearchParams(location.search).get('lang');
    if (requested === 'en' || requested === 'zh') return requested;
    try { return localStorage.getItem(LANGUAGE_KEY) === 'en' ? 'en' : 'zh'; }
    catch { return 'zh'; }
  }

  function t(key, ...args) {
    const text = COPY[state.language][key];
    return typeof text === 'function' ? text(...args) : text;
  }

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
    if (!s) return { year: t('unknownYear'), day: t('unknownDate') };
    const p = s.split('-');
    if (state.language === 'en') return { year: p[0], day: new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', timeZone: 'UTC' }).format(new Date(`${s}T00:00:00Z`)) };
    return { year: p[0], day: Number(p[1]) + '月' + Number(p[2]) + '日' };
  }

  function cardHtml(a) {
    const hasZh = a.title_zh && a.title_zh !== a.title_en;
    const english = state.language === 'en';
    const originalExcerpt = english && a.summary_en?.trim().length > 5;
    const hasSummary = english ? originalExcerpt : (a.summary_status === 'ready' && a.summary_zh?.trim().length > 5);
    const summary = originalExcerpt ? a.summary_en : a.summary_zh;
    const title = !english && hasZh ? a.title_zh : a.title_en;
    return `<article class="article-card">
      <div class="article-meta"><span class="source-mark" aria-hidden="true"></span>${esc(a.source || SOURCE_TITLE[a.source_key] || '')}<span class="excerpt-label">${t(english ? 'excerptEn' : 'excerptZh')}</span></div>
      <h3 class="article-title" lang="${!english && hasZh ? 'zh-CN' : 'en'}"><a href="${safeUrl(a.url)}" target="_blank" rel="noopener noreferrer">${esc(title)}</a></h3>
      ${!english && hasZh ? `<p class="title-en" lang="en">${esc(a.title_en)}</p>` : ''}
      <p class="card-summary${hasSummary ? '' : ' is-empty'}" lang="${english ? 'en' : 'zh-CN'}">${hasSummary ? esc(summary.replace(/^【机器翻译摘要】\n?/, '')) : t(english ? 'originalPending' : (a.summary_status === 'failed' ? 'summaryFailed' : 'summaryPending'))}</p>
      <a class="read-link" href="${safeUrl(a.url)}" target="_blank" rel="noopener noreferrer">${t('readOriginal')} <span aria-hidden="true">↗</span></a>
    </article>`;
  }

  function safeUrl(value) {
    try { const url = new URL(value); return /^https?:$/.test(url.protocol) ? esc(url.href) : '#'; }
    catch { return '#'; }
  }

  function digestsHtml(digests) {
    if (!digests || !digests.length) return `<div class="empty-state"><h3>${t('noResults')}</h3><p>${t('tryFilters')}</p><button class="text-button" data-reset>${t('clearFilters')}</button></div>`;
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
    <span class="date-count">${t('articles', day.articles.length)}</span>
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
        <div class="constitution-eyebrow">${t('foundational')}</div>
        <div class="constitution-title">${esc(it.title)}</div>
        <div class="constitution-desc">${esc(state.language === 'en' ? (it.desc_en || t('constitutionDesc')) : it.desc)}</div>
      </div>
    </div>
    <div class="constitution-arrow">
      <span class="constitution-cta">${t('readOriginal')} →</span>
    </div>
  </a>
</div>`).join('');
    return cards;
  }

  function archiveHtml(allUrls, orderArr) {
    const order = orderArr || Object.keys(allUrls);
    return order.filter(k => allUrls[k] && allUrls[k].length).map(key => {
      const items = allUrls[key] || [];
      const desc = state.language === 'en' ? (SOURCE_DESCRIPTION_EN[key] || '') : (items[0]?.desc || '');
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
  <ul class="archive-list">${links || `<li>${t('noData')}</li>`}</ul>
</section>`;
    }).join('');
  }


  const state = { source: '', query: '', view: 'latest', language: initialLanguage() };
  let feedData;
  let changesPromise;
  let feedFailed = false;
  const sourceKeys = Object.keys(SOURCE_URL);
  const main = document.getElementById('js-main');
  const result = document.getElementById('js-results');
  const search = document.getElementById('js-search');

  function humanTime(value, includeYear = false) {
    if (!value) return t('noSuccess');
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return t('unknownTime');
    return new Intl.DateTimeFormat(state.language === 'en' ? 'en' : 'zh-CN', { timeZone: 'Asia/Taipei', ...(includeYear ? { year: 'numeric' } : {}), month: state.language === 'en' ? 'short' : 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(d);
  }

  function matches(item) {
    const text = [item.title, item.title_en, item.title_zh, item.summary_zh, item.summary_en, item.url].filter(Boolean).join(' ').toLocaleLowerCase();
    return !state.query || text.includes(state.query.toLocaleLowerCase());
  }

  function sourceButtons() {
    const counts = Object.fromEntries(sourceKeys.map(key => [key, state.view === 'archive'
      ? (feedData.all_urls?.[key] || []).length
      : (feedData.digests || []).flatMap(d => d.articles).filter(a => a.source_key === key).length]));
    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    document.getElementById('js-sources').innerHTML = [['', t('allSources')], ...sourceKeys.map(key => [key, SOURCE_TITLE[key]])].map(([key, title]) => `<button class="source-button${state.source === key ? ' active' : ''}" data-source="${key}" aria-pressed="${state.source === key}"><span>${esc(title)}</span><span class="source-count">${key ? counts[key] : total}</span></button>`).join('');
  }

  function healthHtml() {
    const h = feedData.health;
    if (!h) return `<span class="sync-label">${t('unknownHealth')}</span>`;
    const c = h.summary_coverage || {};
    const ok = h.status === 'ok' && !c.failed;
    return `<details class="health-panel"><summary><span class="status-dot ${ok ? '' : 'warn'}"></span><span>${t(ok ? 'updated' : 'partial')}</span><span class="sync-time">${humanTime(h.last_success_at)}</span><span class="chevron" aria-hidden="true">⌄</span></summary>
      <div class="health-body"><div class="health-overview"><strong>${esc(c.ready ?? 0)}<small> / ${esc(c.total ?? 0)}</small></strong><span>${t('readyLabel')}</span><span class="coverage">${Math.round((c.ratio || 0) * 100)}%</span></div>
      <p class="health-note">${esc(t('pendingFailed', c.pending ?? 0, c.failed ?? 0))}</p>
      <ul>${Object.entries(h.sources || {}).map(([key, info]) => `<li><span>${esc(SOURCE_TITLE[key] || key)}</span><span class="source-status ${info.status === 'ok' ? '' : 'warn-text'}">${t(info.status === 'ok' ? 'healthy' : 'recovering')}</span></li>`).join('')}</ul>
      <p class="health-note">${t('lastSuccess')}: ${humanTime(h.last_success_at, true)} · UTC+8</p><p class="health-note">${t('translationNote')}</p></div></details>`;
  }

  function renderFeed() {
    sourceButtons();
    const days = (feedData.digests || []).map(day => ({ ...day, articles: day.articles.filter(a => (!state.source || a.source_key === state.source) && matches(a)) })).filter(day => day.articles.length);
    const all = Object.fromEntries(Object.entries(feedData.all_urls || {}).map(([key, items]) => [key, (!state.source || key === state.source) ? items.filter(matches) : []]));
    const count = state.view === 'archive' ? Object.values(all).reduce((n, a) => n + a.length, 0) : days.reduce((n, d) => n + d.articles.length, 0);
    document.getElementById('js-result-count').textContent = t('articleCount', count);
    result.innerHTML = state.view === 'archive'
      ? (count ? archiveHtml(all, feedData.archive_order) : digestsHtml([])) + ((!state.source && !state.query) ? staticRefsHtml(feedData.static_refs || []) : '')
      : digestsHtml(days);
  }

  async function renderChanges() {
    result.innerHTML = `<div class="loading-state">${t('loadingChanges')}</div>`;
    try {
      changesPromise ||= fetch('./changelog.json').then(r => { if (!r.ok) throw new Error('load'); return r.json(); }).catch(e => { changesPromise = null; throw e; });
      const entries = await changesPromise;
      if (state.view !== 'updates') return;
      result.innerHTML = `<div class="release-list">${entries.map((entry, i) => {
        const translated = state.language === 'en' && entry.title_en && Array.isArray(entry.changes_en);
        const title = translated ? entry.title_en : entry.title;
        const type = translated ? entry.type_en : entry.type;
        const changes = translated ? entry.changes_en : entry.changes;
        return `<article class="release" lang="${translated ? 'en' : 'zh-CN'}"><div class="release-meta"><time datetime="${esc(entry.date)}">${esc(entry.date.replaceAll('-', '.'))}</time><span class="release-type">${esc(type)}</span>${i === 0 ? `<span class="release-latest">${t('newest')}</span>` : ''}</div><h2>${esc(title)}</h2><ul>${changes.map(change => `<li>${esc(change)}</li>`).join('')}</ul></article>`;
      }).join('')}</div>`;
    } catch {
      if (state.view === 'updates') result.innerHTML = `<div class="empty-state"><h3>${t('changesFailed')}</h3><button class="text-button" data-retry-changes>${t('reload')}</button></div>`;
    }
  }

  function route() {
    state.view = ['archive', 'updates'].includes(location.hash.slice(1)) ? location.hash.slice(1) : 'latest';
    const updates = state.view === 'updates';
    document.querySelectorAll('[data-view]').forEach(a => { const active = a.dataset.view === state.view; a.classList.toggle('active', active); if (active) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
    document.getElementById('js-sidebar').hidden = updates;
    document.getElementById('js-toolbar').hidden = updates || !feedData;
    main.classList.toggle('updates-view', updates);
    document.getElementById('js-page-title').textContent = t(state.view);
    document.title = `${t(state.view)} · ${t('siteName')}`;
    if (updates) renderChanges();
    else if (feedData) renderFeed();
    else result.innerHTML = feedFailed
      ? `<div class="empty-state"><h2>${t('feedFailed')}</h2><p>${t('feedRetry')}</p><button class="text-button" data-reload>${t('reload')}</button></div>`
      : `<div class="loading-state">${t('loadingArticles')}</div>`;
  }

  function applyLanguage() {
    document.documentElement.lang = state.language === 'en' ? 'en' : 'zh-CN';
    document.querySelector('meta[name="description"]').content = t('description');
    document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll('[data-i18n-aria]').forEach(el => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
    document.querySelectorAll('[data-language]').forEach(el => { el.setAttribute('aria-pressed', String(el.dataset.language === state.language)); });
    const healthOpen = document.querySelector('.health-panel')?.open;
    if (feedData) document.getElementById('js-health').innerHTML = healthHtml();
    if (healthOpen && document.querySelector('.health-panel')) document.querySelector('.health-panel').open = true;
    route();
  }

  function setLanguage(language) {
    if (!['zh', 'en'].includes(language)) return;
    state.language = language;
    try { localStorage.setItem(LANGUAGE_KEY, language); } catch { /* Language switching also works without storage. */ }
    const url = new URL(location.href);
    url.searchParams.set('lang', language);
    history.replaceState(null, '', url);
    applyLanguage();
  }

  async function init() {
    feedFailed = false;
    route();
    try {
      const res = await fetch('./data.json');
      if (!res.ok) throw new Error('load');
      feedData = await res.json();
      applyLanguage();
    } catch (err) {
      feedFailed = true;
      route();
      console.error(err);
    }
  }

  search.addEventListener('input', () => { state.query = search.value.trim(); if (feedData) renderFeed(); });
  document.addEventListener('click', event => {
    const language = event.target.closest('[data-language]');
    if (language) { setLanguage(language.dataset.language); return; }
    const panel = document.querySelector('.health-panel');
    if (panel?.open && !panel.contains(event.target)) panel.open = false;
    const button = event.target.closest('[data-source]');
    if (button) { state.source = button.dataset.source; renderFeed(); document.querySelector(`[data-source="${state.source}"]`)?.focus({ preventScroll: true }); }
    if (event.target.closest('[data-reset]')) { state.source = ''; state.query = ''; search.value = ''; renderFeed(); search.focus(); }
    if (event.target.closest('[data-reload]')) init();
    if (event.target.closest('[data-retry-changes]')) renderChanges();
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape') { const panel = document.querySelector('.health-panel'); if (panel?.open) { panel.open = false; panel.querySelector('summary').focus(); } } });
  window.addEventListener('hashchange', () => { if (['', '#latest', '#archive', '#updates'].includes(location.hash)) { route(); window.scrollTo({ top: 0, behavior: 'instant' }); document.getElementById('js-page-title').focus({ preventScroll: true }); } });
  const fab = document.getElementById('js-fab');
  fab.addEventListener('click', () => window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }));
  window.addEventListener('scroll', () => { fab.hidden = window.scrollY < 500; }, { passive: true });
  applyLanguage();
  init();
})();
