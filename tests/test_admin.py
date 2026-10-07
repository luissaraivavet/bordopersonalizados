import copy
import http.client
import io
import json
from pathlib import Path
import shutil
import tempfile
import threading
import unittest
from unittest.mock import patch
import zipfile

import admin_server as app


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(app.CONTENT.read_text(encoding='utf-8'))

    def test_original_catalog(self):
        app.validate(self.data)
        self.assertEqual(self.data['settings']['location'], 'Teixeiras, MG')
        bows = [p for p in self.data['products'] if p['collection'] in ('jardim', 'sinfonia')]
        self.assertEqual(len(bows), 39)
        self.assertTrue(all(p['price'] == 49.90 for p in bows))
        kits = [p for p in self.data['products'] if p['collection'] == 'kits']
        self.assertEqual(len(kits), 2)
        self.assertTrue(all(p['price'] == 119.90 and len(p['bundle']) == 3 for p in kits))

    def test_invalid_prices_and_discount(self):
        for value in (-1, float('nan'), float('inf'), True, '55'):
            data = copy.deepcopy(self.data)
            data['products'][0]['price'] = value
            with self.assertRaises(ValueError):
                app.validate(data)
        self.data['settings']['pixDiscount'] = 101
        with self.assertRaises(ValueError):
            app.validate(self.data)

    def test_kit_members_and_visibility(self):
        kit = next(p for p in self.data['products'] if p['id'] == 'trio')
        for members in (['gato'], ['gato', 'gato', 'coruja'], ['gato', 'coruja', 'missing']):
            kit['bundle'] = members
            with self.assertRaises(ValueError):
                app.validate(self.data)
        kit['bundle'] = ['gato', 'coruja', 'leao']
        next(p for p in self.data['products'] if p['id'] == 'gato')['published'] = False
        self.assertNotIn('trio', [p['id'] for p in app.public_content(self.data)['products']])

    def test_foreign_collection_and_duplicate_id(self):
        self.data['products'][0]['collection'] = 'missing'
        with self.assertRaises(ValueError):
            app.validate(self.data)
        self.data['products'][0]['collection'] = 'jardim'
        self.data['products'][0]['id'] = 'jardim'
        with self.assertRaises(ValueError):
            app.validate(self.data)

    def test_unsafe_urls_paths_and_empty_home(self):
        for value in ('javascript:alert(1)', 'http://example.com', 'https://user:secret@example.com'):
            self.data['settings']['instagram'] = value
            with self.assertRaises(ValueError):
                app.validate(self.data)
        for value in ('assets/../admin_server.py', '/etc/passwd', 'https://example.com/photo.jpg'):
            with self.assertRaises(ValueError):
                app.image_path(value)
        self.data['settings']['instagram'] = 'https://instagram.com/bordobordadospersonalizados/'
        for collection in self.data['collections']:
            collection['featured'] = False
        with self.assertRaises(ValueError):
            app.validate(self.data)

    def test_publication_branch_guard(self):
        with patch.object(app, 'status', return_value={'canPublish': False}), patch.object(app, 'apply_content') as write:
            with self.assertRaises(ValueError):
                app.publish(self.data)
            write.assert_not_called()

    def test_hidden_items_remain_private(self):
        self.data['testimonials'] = [{'id': 'private-review', 'name': 'Rascunho', 'text': 'Ainda nao autorizado', 'published': False}]
        self.data['collections'][1]['published'] = False
        public = app.public_content(self.data)
        self.assertEqual(public['testimonials'], [])
        self.assertFalse(any(p['collection'] == 'sinfonia' for p in public['products']))
        self.assertNotIn(b'Ainda nao autorizado', app.script(self.data))
        self.assertEqual(len(self.data['testimonials']), 1)


class PrivateServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        root = Path(cls.temporary.name)
        shutil.copytree(app.ROOT / 'assets', root / 'assets')
        shutil.copytree(app.ROOT / 'admin', root / 'admin')
        shutil.copytree(app.ROOT / 'content', root / 'content')
        shutil.copyfile(app.ROOT / 'index.html', root / 'index.html')
        cls.root_patch = patch.object(app, 'ROOT', root)
        cls.state_patch = patch.object(app, 'STATE', root / '.bordo-admin')
        cls.content_patch = patch.object(app, 'CONTENT', root / 'content/site.json')
        cls.status_patch = patch.object(app, 'status', return_value={'branch': 'test', 'canPublish': False})
        for item in (cls.root_patch, cls.state_patch, cls.content_patch, cls.status_patch):
            item.start()
        cls.server = app.make_server()
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        for item in (cls.status_patch, cls.content_patch, cls.state_patch, cls.root_patch):
            item.stop()
        cls.temporary.cleanup()

    def request(self, path, method='GET', body=None, auth=True, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        values = {'Host': self.server.host}
        if auth:
            values['Cookie'] = 'bordo_session=' + self.server.session
        if method == 'POST':
            values.update({'Origin': 'http://' + self.server.host, 'X-CSRF-Token': self.server.csrf})
        values.update(headers or {})
        raw = json.dumps(body).encode() if isinstance(body, dict) else body
        connection.request(method, path, raw, values)
        response = connection.getresponse()
        result = (response.status, dict(response.getheaders()), response.read())
        connection.close()
        return result

    def test_unauthorized_host_origin_csrf_and_traversal(self):
        self.assertEqual(self.request('/api/content', auth=False)[0], 401)
        self.assertEqual(self.request('/api/content', headers={'Host': 'evil.test'})[0], 403)
        self.assertEqual(self.request('/api/save', 'POST', {}, headers={'Origin': 'https://evil.test'})[0], 403)
        self.assertEqual(self.request('/api/save', 'POST', {}, headers={'X-CSRF-Token': 'wrong'})[0], 403)
        self.assertEqual(self.request('/assets/../.bordo-admin/draft.json')[0], 404)
        self.assertEqual(self.request('/assets/%2e%2e/admin_server.py')[0], 404)

    def test_launch_key_is_single_use(self):
        key = self.server.launch_key
        response = self.request('/entrar?key=' + key, auth=False)
        self.assertEqual(response[0], 303)
        self.assertIn('HttpOnly', response[1]['Set-Cookie'])
        self.assertIn('SameSite=Strict', response[1]['Set-Cookie'])
        self.assertEqual(self.request('/entrar?key=' + key, auth=False)[0], 401)

    def test_save_revision_preview_and_export(self):
        initial = app.CONTENT.read_bytes()
        result = json.loads(self.request('/api/content')[2])
        data = result['content']
        data['products'][3]['price'] = 60
        body = {'content': data, 'revision': result['revision']}
        self.assertEqual(self.request('/api/save', 'POST', body)[0], 200)
        self.assertEqual(self.request('/api/save', 'POST', body)[0], 409)
        self.assertEqual(app.CONTENT.read_bytes(), initial)
        self.assertIn(b'"price": 60', self.request('/preview/assets/content.js')[2])
        response = self.request('/api/export')
        self.assertEqual(response[0], 200)
        with zipfile.ZipFile(io.BytesIO(response[2])) as archive:
            self.assertIn(b'"price": 60', archive.read('assets/content.js'))
            self.assertNotIn('admin_server.py', archive.namelist())
            self.assertFalse(any(name.startswith(('.git/', '.bordo-admin/', 'admin/')) for name in archive.namelist()))

    def test_upload_rejects_html_and_accepts_image(self):
        self.assertEqual(self.request('/api/upload', 'POST', b'<script>bad</script>')[0], 400)
        raw = (app.ROOT / 'assets/brand-logo.png').read_bytes()
        response = self.request('/api/upload', 'POST', raw)
        self.assertEqual(response[0], 200)
        relative = json.loads(response[2])['path']
        self.assertTrue(relative.startswith('assets/uploads/'))
        self.assertEqual((app.ROOT / relative).read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
