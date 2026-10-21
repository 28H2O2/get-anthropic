import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

import build_data
import main
import translator
from fetchers import common


class PipelineTests(unittest.TestCase):
    def test_date_precision_and_lastmod(self):
        self.assertEqual(common.parse_date('October 2026'), '2026-10')
        self.assertEqual(common.parse_date('2026'), '2026')
        self.assertEqual(common.parse_date('Feb 30, 2026'), '')
        xml = b'<urlset><url><loc>https://www.anthropic.com/news/old</loc><lastmod>2026-10-21</lastmod></url></urlset>'
        with patch.object(common, 'get', return_value=Mock(content=xml)):
            article = common.discover('anthropic_news')[0]
        self.assertEqual(article['date'], '')
        self.assertEqual(article['sitemap_lastmod'], '2026-10-21')

    def test_migrated_sources_and_pagination(self):
        pages = {
            'https://www.anthropic.com/engineering': '<a href="/research/new"><h3>New article</h3><time>Oct 20, 2026</time></a><a rel="next" href="?page=2">Next</a>',
            'https://www.anthropic.com/engineering?page=2': '<a href="/research/older">Older</a>',
        }
        def get(url):
            return Mock(url=url, content=pages[url].encode())
        with patch.object(common, 'get', side_effect=get):
            articles = common.discover('engineering')
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]['date'], '2026-10-20')
        self.assertTrue(common.is_article('https://claude.com/resources/articles/new', 'claude_blog'))
        self.assertFalse(common.is_article('https://www.anthropic.com/news/models', 'anthropic_news'))
        self.assertFalse(common.is_article('https://www.anthropic.com/research/team/frontier-red-team', 'anthropic_research'))

    def test_article_metadata_and_clean_body(self):
        html = '''<meta property="article:published_time" content="2025-03-20T00:00:00Z"><link rel="canonical" href="https://www.anthropic.com/research/real"><h1>Real title</h1><article><nav>Navigation</nav><p class="text-caption">Published October 21, 2026</p><p>This is a complete introduction about the real article and its useful technical findings. It contains enough text to identify the article body.</p><aside><p>Related navigation that should never become part of the excerpt even when it is long enough.</p></aside></article>'''
        a = common.extract_article(html, 'https://www.anthropic.com/research/alias')
        self.assertEqual(a['date'], '2025-03-20')
        self.assertEqual(a['url'], 'https://www.anthropic.com/research/real')
        self.assertNotIn('Navigation', a['content'])
        self.assertNotIn('Related navigation', a['content'])
        self.assertNotIn('Published', a['content'])

    def test_request_timeout_is_retried_three_times(self):
        with patch.object(common.requests, 'get', side_effect=common.requests.Timeout), patch.object(common.time, 'sleep'):
            with self.assertRaises(common.requests.Timeout):
                common.get('https://example.com')
            self.assertEqual(common.requests.get.call_count, 3)

    def test_distill_float_date_and_rich_text_footnote(self):
        body = 'This complete introductory paragraph explains the technical findings and is long enough to serve as the article content.'
        html = f'<h1>Title</h1><div class="RichTextWrapper">A footnote without paragraphs that is long enough to pass a text length check. {body}</div><d-article><div style="float: right;">October 19, 2026</div><p>{body}</p></d-article>'
        article = common.extract_article(html, 'https://alignment.anthropic.com/2026/graft/')
        self.assertEqual(article['date'], '2026-10-19')
        self.assertEqual(article['content'], body)

    def test_translation_failure_raises_after_three_tries(self):
        with patch.object(translator, '_once', side_effect=TimeoutError), patch.object(translator.time, 'sleep'):
            with self.assertRaises(TimeoutError):
                translator.translate('', 'This is a full sentence about meaningful technical results.')
            self.assertEqual(translator._once.call_count, 3)
        self.assertFalse(translator.valid_translation('[阿里云翻译失败: timeout]'))
        self.assertFalse(translator.valid_translation('模型在 {{1 }} 的工作中得到应用。'))

    def test_placeholder_whitespace_and_sentence_budget(self):
        self.assertEqual(translator._restore_nouns('在 {{ 1 }} 工作', {'{{1}}': 'Anthropic'}), '在 Anthropic 工作')
        text = 'First complete sentence. ' + ('Long complete sentence about results. ' * 50)
        value = translator.excerpt(text)
        self.assertLessEqual(len(value), 800)
        self.assertTrue(value.endswith('.'))
        self.assertFalse(value.endswith('res'))

    def test_aliyun_string_success_code(self):
        response = Mock()
        response.body.code = '200'
        response.body.data.translated = 'Claude 的有效中文摘录内容。'
        with patch('alibabacloud_alimt20181012.client.Client') as client, patch.dict('os.environ', {'ALIYUN_ACCESS_KEY_ID': 'test', 'ALIYUN_ACCESS_KEY_SECRET': 'test'}):
            client.return_value.translate_general.return_value = response
            self.assertEqual(translator._aliyun('Claude article'), 'Claude 的有效中文摘录内容。')

    def test_failure_retry_outside_old_three_day_window(self):
        meta = {'date': '2026-10-13', 'fetch_status': 'ok', 'summary_status': 'failed'}
        self.assertTrue(main.should_translate(meta, '2026-09-21', '2026-10-21'))
        meta = {'date': '', 'first_seen_at': '2026-10-01', 'fetch_status': 'failed', 'metadata_checked_at': '2026-10-01'}
        self.assertTrue(main.needs_metadata(meta, '2026-09-21', '2026-10-21'))
        meta['fetch_status'] = 'ok'
        self.assertTrue(main.should_translate(meta, '2026-09-21', '2026-10-21'))

    def test_canonical_merge_keeps_valid_translation(self):
        old = {'summary_zh': '这是已经生成的有效中文摘录。', 'date': '2026-10-13', 'date_verified': True, 'date_precision': 'day', 'source': 'anthropic_research'}
        merged = main.merge_records(old, {'date': '2026-10-21', 'source': 'engineering', 'aliases': ['https://example.com/old']})
        self.assertEqual(merged['date'], '2026-10-13')
        self.assertEqual(merged['summary_status'], 'ready')
        self.assertEqual(merged['source'], 'engineering')
        self.assertTrue(merged['summary_zh'])
        self.assertEqual(main.article_source('https://www.anthropic.com/news/distillation-defenses', 'anthropic_news', 'anthropic_research'), 'anthropic_news')

    def test_latest_valid_legacy_migration_and_idempotency(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for day, text in [('2026-10-01', '较早的有效中文摘录内容。'), ('2026-10-02', '最新的有效中文摘录内容。'), ('2026-10-03', '[阿里云翻译失败: timeout]')]:
                path = root / day / 'digest.md'; path.parent.mkdir()
                path.write_text(f'---\n### [Title](https://example.com/a)\n\n**原文**: https://example.com/a\n\n**中文摘要**：\n\n{text}\n')
            index = {'https://example.com/a': {'title': 'Title', 'source': 'anthropic_news', 'processed': True}}
            migrated = main.migrate(index, root)
            self.assertEqual(migrated['https://example.com/a']['summary_zh'], '最新的有效中文摘录内容。')
            self.assertEqual(main.migrate(migrated, root), migrated)

    def test_zero_source_stops_build_without_overwriting_public_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); public = root / 'public'; public.mkdir()
            index = root / 'article_index.json'; index.write_text('{}')
            (root / 'fetch_status.json').write_text(json.dumps({'sources': {'engineering': {'status': 'failed'}}}))
            target = public / 'data.json'; target.write_text('previous healthy data')
            with patch.object(build_data, 'BASE_DIR', root), patch.object(build_data, 'INDEX_FILE', index), patch.object(build_data, 'PUBLIC_DIR', public):
                with self.assertRaises(RuntimeError):
                    build_data.build()
            self.assertEqual(target.read_text(), 'previous healthy data')

    def test_failed_undated_article_remains_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            today = build_data.datetime.now(build_data.ZoneInfo('Asia/Taipei')).date().isoformat()
            records = {'https://claude.com/resources/articles/new': {'source': 'claude_blog', 'title': 'New article', 'date': '', 'first_seen_at': today, 'summary_status': 'failed', 'fetch_status': 'failed'}}
            path = root / 'article_index.json'; path.write_text(json.dumps(records))
            (root / 'fetch_status.json').write_text(json.dumps({'sources': {'claude_blog': {'status': 'ok', 'discovered': 1}}, 'status': 'degraded'}))
            with patch.object(build_data, 'BASE_DIR', root), patch.object(build_data, 'INDEX_FILE', path), patch.object(build_data, 'PUBLIC_DIR', root / 'public'):
                data = build_data.build()
            self.assertEqual(data['health']['summary_coverage']['failed'], 1)
            self.assertEqual(data['digests'][0]['articles'][0]['summary_status'], 'failed')

    def test_translation_failure_is_persisted_and_retried(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'config.json').write_text(json.dumps({'sources': {'anthropic_news': True}}))
            url = 'https://www.anthropic.com/news/new'
            found = [{'url': url, 'source': 'anthropic_news', 'date': '', 'title': ''}]
            article = {'url': url, 'title': 'Title', 'date': '2026-10-13', 'date_precision': 'day', 'content': 'A complete useful sentence explaining the research.'}
            with patch.object(main, 'BASE_DIR', root), patch.object(main, 'INDEX_FILE', root / 'article_index.json'), patch.object(main, 'STATUS_FILE', root / 'fetch_status.json'), patch.object(main, 'discover', return_value=found), patch.object(main, 'fetch_article', return_value=article), patch('sys.argv', ['main.py', '--date', '2026-10-21']):
                with patch.object(main, 'translate', side_effect=TimeoutError):
                    main.main()
                failed = json.loads((root / 'article_index.json').read_text())[url]
                self.assertFalse(failed['processed'])
                self.assertEqual(failed['summary_status'], 'failed')
                with patch.object(main, 'translate', return_value='这是一段有效且可再次生成的中文摘录。'):
                    main.main()
                retried = json.loads((root / 'article_index.json').read_text())[url]
                self.assertTrue(retried['processed'])
                self.assertEqual(retried['summary_status'], 'ready')

    def test_run_translates_only_recent_and_second_run_does_not_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'config.json').write_text(json.dumps({'sources': {'anthropic_news': True}, 'translate_engine': 'aliyun'}))
            discovered = [{'url': 'https://www.anthropic.com/news/new', 'source': 'anthropic_news', 'date': '', 'title': ''}, {'url': 'https://www.anthropic.com/news/old', 'source': 'anthropic_news', 'date': '', 'title': ''}]
            def fetch(url):
                return {'url': url, 'title': 'Title', 'date': '2026-10-20' if url.endswith('new') else '2025-01-01', 'date_precision': 'day', 'content': 'A full introductory sentence with enough article content to translate correctly.'}
            with patch.object(main, 'BASE_DIR', root), patch.object(main, 'INDEX_FILE', root / 'article_index.json'), patch.object(main, 'STATUS_FILE', root / 'fetch_status.json'), patch.object(main, 'discover', return_value=discovered), patch.object(main, 'fetch_article', side_effect=fetch), patch.object(main, 'translate', return_value='这是一段有效的中文摘录内容。') as translate, patch('sys.argv', ['main.py', '--date', '2026-10-21']):
                self.assertEqual(main.main(), 0)
                self.assertEqual(translate.call_count, 2)
                self.assertEqual(main.main(), 0)
                self.assertEqual(translate.call_count, 2)
                index = json.loads((root / 'article_index.json').read_text())
                self.assertFalse(index['https://www.anthropic.com/news/old']['processed'])
                self.assertTrue(index['https://www.anthropic.com/news/new']['processed'])


if __name__ == '__main__':
    unittest.main()
