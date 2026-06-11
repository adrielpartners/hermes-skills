#!/usr/bin/env python3
"""wp-client — WordPress REST API CLI.

Usage:
  export WP_URL= WP_USER= WP_PASS=
  python3 wp-client.py discover
  python3 wp-client.py list posts [--status publish] [--per-page 5] [--fields id,title,status]
  python3 wp-client.py list business-listing [--status publish]
  python3 wp-client.py get posts 123 [--embed]
  python3 wp-client.py get-by-slug posts my-post-slug
  python3 wp-client.py create posts '{"title":"Hi","status":"draft"}'
  python3 wp-client.py update posts 123 '{"title":"Updated"}'
  python3 wp-client.py delete posts 123
  python3 wp-client.py count business-listing --status publish
  python3 wp-client.py search "ranch" [--type post]
  python3 wp-client.py taxonomy categories [--per-page 100]
  python3 wp-client.py taxonomy business-category [--per-page 100]
  python3 wp-client.py settings [--get] [--set '{"title":"New Title"}']
  python3 wp-client.py types             # List all post types & rest_base
  python3 wp-client.py taxonomies        # List all taxonomies

Credentials: WP_URL, WP_USER, WP_PASS env vars, or --url/--user/--pass flags.
"""

import json, os, sys, urllib.request, urllib.error, argparse, html

class WPClient:
    def __init__(self, url, user, password):
        self.base = url.rstrip('/') + '/wp-json'
        self.auth = urllib.request.HTTPBasicAuthHandler(
            urllib.request.HTTPPasswordMgrWithPriorAuth()
        )
        mgr = urllib.request.HTTPPasswordMgrWithPriorAuth()
        mgr.add_password(None, self.base, user, password, is_authenticated=True)
        self.auth = urllib.request.HTTPBasicAuthHandler(mgr)
        self.opener = urllib.request.build_opener(self.auth)

    def _req(self, method, path, data=None, params=None):
        url = f"{self.base}{path}"
        if params:
            qs = '&'.join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items() if v is not None)
            url += '?' + qs
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(url, data=body, method=method)
        if body:
            req.add_header('Content-Type', 'application/json')
        try:
            resp = self.opener.open(req)
            headers = dict(resp.headers)
            raw = resp.read()
            result = json.loads(raw) if raw else {}
            return result, headers
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            try:
                err = json.loads(body)
            except json.JSONDecodeError:
                err = {'code': e.code, 'message': body[:500]}
            print(f"❌ HTTP {e.code}: {err.get('message', err)}", file=sys.stderr)
            sys.exit(1)

    def _paginate(self, path, params=None):
        """Auto-paginate to get ALL results."""
        params = params or {}
        params.setdefault('per_page', 100)
        params['page'] = 1
        all_results = []
        while True:
            items, headers = self._req('GET', path, params=params)
            if not isinstance(items, list):
                return items  # not a list endpoint
            all_results.extend(items)
            total = int(headers.get('X-WP-Total', 0))
            total_pages = int(headers.get('X-WP-TotalPages', 1))
            if params['page'] >= total_pages:
                break
            params['page'] += 1
        return all_results

    def discover(self):
        """Full site discovery."""
        print("=== Site Discovery ===\n")

        # User info
        me, _ = self._req('GET', '/wp/v2/users/me')
        print(f"User: {me.get('name', '?')} ({me.get('slug', '?')})")
        print(f"URL:  {me.get('link', '?')}\n")

        # Post types
        types, _ = self._req('GET', '/wp/v2/types')
        print("--- Post Types ---")
        for slug, t in sorted(types.items()):
            print(f"  {slug:25s} → {t['name']:25s} rest_base: {t.get('rest_base','?')}")
        print()

        # Taxonomies
        taxs, _ = self._req('GET', '/wp/v2/taxonomies')
        print("--- Taxonomies ---")
        for slug, t in sorted(taxs.items()):
            types_list = ', '.join(t.get('types', []))
            print(f"  {slug:25s} → {t['name']:25s} (types: {types_list})")
        print()

        # ACF check
        try:
            acf_opts, _ = self._req('GET', '/acf/v3/options/options')
            print("ACF REST API: ACTIVE (options available)")
        except SystemExit:
            print("ACF REST API: not available")

        # Counts
        print("\n--- Content Counts ---")
        for slug, t in types.items():
            rb = t.get('rest_base', slug)
            cnt, _ = self._req('GET', f'/wp/v2/{rb}?_fields=id&per_page=1')
            h = _
            total = h.get('X-WP-Total', '?')
            print(f"  {slug:25s} {str(total):>6s} items")

    def list_items(self, rest_base, status=None, per_page=10, fields=None, page=1):
        params = {'per_page': per_page, 'page': page, 'status': status} if status else {'per_page': per_page, 'page': page}
        # WordPress treats status=publish vs ? without status differently
        if status:
            params['status'] = status
        if fields:
            params['_fields'] = fields
        items, headers = self._req('GET', f'/wp/v2/{rest_base}', params=params)
        total = headers.get('X-WP-Total', '?')
        pages = headers.get('X-WP-TotalPages', '?')
        print(f"Total: {total}  |  Page {page}/{pages}")
        print(f"{'ID':>6s} | {'Status':10s} | {'Title'}")
        print("-" * 80)
        for item in items if isinstance(items, list) else [items]:
            tid = item.get('id', '?')
            st = item.get('status', '?')
            title = html.unescape(item.get('title', {}).get('rendered', '(no title)'))
            print(f"{tid:>6d} | {st:10s} | {title[:60]}")

    def get_item(self, rest_base, item_id, embed=False):
        params = {}
        if embed:
            params['_embed'] = '1'
        item, _ = self._req('GET', f'/wp/v2/{rest_base}/{item_id}', params=params)
        print(json.dumps(item, indent=2, default=str))

    def get_by_slug(self, rest_base, slug):
        items, headers = self._req('GET', f'/wp/v2/{rest_base}', params={'slug': slug})
        if not items:
            print(f"No {rest_base} found with slug: {slug}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(items[0], indent=2, default=str))

    def create_item(self, rest_base, data):
        item, _ = self._req('POST', f'/wp/v2/{rest_base}', data=data)
        print(f"✅ Created {rest_base} #{item.get('id')}: {html.unescape(item.get('title', {}).get('rendered', ''))}")
        return item

    def update_item(self, rest_base, item_id, data):
        item, _ = self._req('PATCH', f'/wp/v2/{rest_base}/{item_id}', data=data)
        print(f"✅ Updated {rest_base} #{item_id}: {html.unescape(item.get('title', {}).get('rendered', ''))}")

    def delete_item(self, rest_base, item_id, force=False):
        params = {'force': 'true'} if force else {}
        result, _ = self._req('DELETE', f'/wp/v2/{rest_base}/{item_id}', params=params)
        deleted = result.get('deleted', False)
        prev = result.get('previous', {})
        title = html.unescape(prev.get('title', {}).get('rendered', item_id))
        status = "✅ Permanently deleted" if force else "🗑️ Trashed"
        print(f"{status} {rest_base} #{item_id}: {title}")

    def count(self, rest_base, status='publish'):
        params = {'_fields': 'id', 'per_page': 1}
        if status:
            params['status'] = status
        _, headers = self._req('GET', f'/wp/v2/{rest_base}', params=params)
        total = headers.get('X-WP-Total', 0)
        print(f"{total} {rest_base} (status: {status or 'all'})")

    def search(self, query, search_type=None, per_page=10):
        params = {'search': query, 'per_page': per_page}
        if search_type:
            params['type'] = search_type
        items, headers = self._req('GET', '/wp/v2/search', params=params)
        total = headers.get('X-WP-Total', '?')
        print(f"Search results for '{query}': {total} total\n")
        print(f"{'ID':>6s} | {'Type':15s} | {'Title'}")
        print("-" * 70)
        for item in items if isinstance(items, list) else []:
            tid = item.get('id', '?')
            tp = item.get('type', '?')
            title = html.unescape(item.get('title', '?'))
            url = item.get('url', '')
            print(f"{tid:>6d} | {tp:15s} | {title[:50]}")
            if url:
                print(f"{'':>6s} | {'':15s} | {url}")

    def list_taxonomy(self, taxonomy, per_page=100, hide_empty=False):
        params = {'per_page': per_page, 'hide_empty': 'true' if hide_empty else 'false'}
        items, headers = self._req('GET', f'/wp/v2/{taxonomy}', params=params)
        total = headers.get('X-WP-Total', '?')
        print(f"Total: {total}\n")
        print(f"{'ID':>6s} | {'Count':>5s} | {'Parent':>6s} | {'Name'}")
        print("-" * 70)
        for item in items if isinstance(items, list) else []:
            tid = item.get('id', '?')
            cnt = item.get('count', 0)
            parent = item.get('parent', 0)
            name = html.unescape(item.get('name', '?'))
            slug = item.get('slug', '')
            print(f"{tid:>6d} | {cnt:>5d} | {parent:>6d} | {name}")
            print(f"{'':>6s} | {'':>5s} | {'':>6s} | {slug}")

    def settings(self, action='get', data=None):
        if action == 'get':
            settings, _ = self._req('GET', '/wp/v2/settings')
            print(json.dumps(settings, indent=2, default=str))
        elif action == 'set':
            if not data:
                print("❌ --set requires JSON data", file=sys.stderr)
                sys.exit(1)
            result, _ = self._req('POST', '/wp/v2/settings', data=data)
            print("✅ Settings updated")
            print(json.dumps(result, indent=2, default=str))

    def types(self):
        types, _ = self._req('GET', '/wp/v2/types')
        print(f"{'Slug':25s} {'Name':25s} {'Rest Base':20s} {'Hierarchical'}")
        print("-" * 85)
        for slug, t in sorted(types.items()):
            hier = "✓" if t.get('hierarchical', False) else "✗"
            print(f"{slug:25s} {t['name']:25s} {t.get('rest_base','?'):20s} {hier}")

    def taxonomies(self):
        taxs, _ = self._req('GET', '/wp/v2/taxonomies')
        for slug, t in sorted(taxs.items()):
            types_list = ', '.join(t.get('types', []))
            hier = "✓" if t.get('hierarchical', False) else "✗"
            print(f"{slug:25s} {t['name']:25s} hier={hier}  types: [{types_list}]")


def main():
    parser = argparse.ArgumentParser(description='WordPress REST API Client')
    parser.add_argument('--url', help='WordPress site URL')
    parser.add_argument('--user', help='WordPress username')
    parser.add_argument('--pass', dest='password', help='Application password')

    sub = parser.add_subparsers(dest='command', required=True)

    # discover
    sub.add_parser('discover', help='Full site discovery')

    # list
    list_p = sub.add_parser('list', help='List items')
    list_p.add_argument('rest_base', help='Post type rest_base (e.g. posts, pages, business-listing)')
    list_p.add_argument('--status', help='Filter by status (publish, draft, etc.)')
    list_p.add_argument('--per-page', type=int, default=10, help='Items per page (default 10)')
    list_p.add_argument('--fields', help='Comma-separated fields (e.g. id,title,status)')
    list_p.add_argument('--page', type=int, default=1, help='Page number')

    # get
    get_p = sub.add_parser('get', help='Get single item by ID')
    get_p.add_argument('rest_base')
    get_p.add_argument('item_id', type=int)
    get_p.add_argument('--embed', action='store_true', help='Include embedded data (author, media)')

    # get-by-slug
    gbs = sub.add_parser('get-by-slug', help='Get item by slug')
    gbs.add_argument('rest_base')
    gbs.add_argument('slug')

    # create
    create_p = sub.add_parser('create', help='Create item (pass JSON body as arg)')
    create_p.add_argument('rest_base')
    create_p.add_argument('data', help='JSON data string or @file.json')

    # update
    update_p = sub.add_parser('update', help='Update item (PATCH, pass JSON as arg)')
    update_p.add_argument('rest_base')
    update_p.add_argument('item_id', type=int)
    update_p.add_argument('data', help='JSON data string or @file.json')

    # delete
    del_p = sub.add_parser('delete', help='Delete item')
    del_p.add_argument('rest_base')
    del_p.add_argument('item_id', type=int)
    del_p.add_argument('--force', action='store_true', help='Permanent delete (skip trash)')

    # count
    count_p = sub.add_parser('count', help='Count items by status')
    count_p.add_argument('rest_base')
    count_p.add_argument('--status', default='publish', help='Status filter (default: publish)')

    # search
    search_p = sub.add_parser('search', help='Full site search')
    search_p.add_argument('query')
    search_p.add_argument('--type', dest='search_type', help='Restrict to type (post, page, etc.)')
    search_p.add_argument('--per-page', type=int, default=10)

    # taxonomy
    tax_p = sub.add_parser('taxonomy', help='List taxonomy terms')
    tax_p.add_argument('taxonomy', help='Taxonomy slug (categories, tags, business-category, etc.)')
    tax_p.add_argument('--per-page', type=int, default=100)

    # settings
    settings_p = sub.add_parser('settings', help='Get or update site settings')
    settings_p.add_argument('--get', action='store_true', help='Get current settings')
    settings_p.add_argument('--set', help='Update settings (JSON string)')

    # types
    sub.add_parser('types', help='List all post types')

    # taxonomies
    sub.add_parser('taxonomies', help='List all taxonomies')

    args = parser.parse_args()

    # Credentials
    url = args.url or os.environ.get('WP_URL')
    user = args.user or os.environ.get('WP_USER')
    password = args.password or os.environ.get('WP_PASS')

    if not all([url, user, password]):
        print("❌ Missing credentials. Provide --url/--user/--pass or set WP_URL/WP_USER/WP_PASS env vars.", file=sys.stderr)
        sys.exit(1)

    client = WPClient(url, user, password)

    try:
        if args.command == 'discover':
            client.discover()
        elif args.command == 'list':
            client.list_items(args.rest_base, args.status, args.per_page, args.fields, args.page)
        elif args.command == 'get':
            client.get_item(args.rest_base, args.item_id, args.embed)
        elif args.command == 'get-by-slug':
            client.get_by_slug(args.rest_base, args.slug)
        elif args.command == 'create':
            data = json.loads(args.data[1:] if args.data.startswith('@') else args.data)
            client.create_item(args.rest_base, data)
        elif args.command == 'update':
            data = json.loads(args.data[1:] if args.data.startswith('@') else args.data)
            client.update_item(args.rest_base, args.item_id, data)
        elif args.command == 'delete':
            client.delete_item(args.rest_base, args.item_id, args.force)
        elif args.command == 'count':
            client.count(args.rest_base, args.status)
        elif args.command == 'search':
            client.search(args.query, args.search_type, args.per_page)
        elif args.command == 'taxonomy':
            client.list_taxonomy(args.taxonomy, args.per_page)
        elif args.command == 'settings':
            if args.get:
                client.settings('get')
            elif args.set:
                client.settings('set', json.loads(args.set))
            else:
                client.settings('get')
        elif args.command == 'types':
            client.types()
        elif args.command == 'taxonomies':
            client.taxonomies()
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()