---
name: wp-rest-api
description: "Manage WordPress sites via the WP REST API — posts, custom post types, taxonomies, media, pages, users, settings, navigation, blocks, and search. Works with any site that has Application Passwords. Includes a Python CLI helper (scripts/wp-client.py) for one-liner operations."
tags:
  - wordpress
  - rest-api
  - cpt
  - application-passwords
  - blog-management
---

# WordPress REST API Management Skill

## Quick Start — Python CLI (recommended)

```bash
# Set credentials (env vars — don't persist to files)
export WP_URL="https://example.org"
export WP_USER="username"
export WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"

# Discover the site structure
python3 ~/.hermes/skills/wordpress-troubleshooting/wp-rest-api/scripts/wp-client.py discover

# Count published posts
python3 ~/.hermes/skills/wordpress-troubleshooting/wp-rest-api/scripts/wp-client.py count posts --status publish

# List recent business listings
python3 ~/.hermes/skills/wordpress-troubleshooting/wp-rest-api/scripts/wp-client.py list business-listing --status publish --per-page 10

# Create a draft post
python3 ~/.hermes/skills/wordpress-troubleshooting/wp-rest-api/scripts/wp-client.py create posts '{"title": "Hello World", "content": "<p>Test</p>", "status": "draft"}'
```

The Python CLI auto-handles pagination, auth, JSON output, and sensible error messages. All features below document both curl and the Python client.

## Connection pattern

```bash
WP_URL="https://example.org"
WP_USER="username"
WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"
```

**IMPORTANT — proper quoting**: Application passwords contain spaces. Always quote the `-u` argument:

```bash
# ✅ Correct — password is quoted as one unit
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/users/me"

# ❌ Wrong — AUTH as a variable will break on spaces
AUTH="-u $WP_USER:$WP_PASS"  # DON'T do this
curl -s $AUTH "$WP_URL/..."  # password splits into multiple args
```

Test connection:
```bash
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/users/me" | python3 -m json.tool
```

> Expected: 200 with user info. If 401, check Application Password hasn't been revoked.

## Core endpoints

| Resource | REST base | Notes |
|---|---|---|
| Posts | `/wp/v2/posts` | Blog posts |
| Pages | `/wp/v2/pages` | Standard pages |
| Custom post types | `/wp/v2/{rest_base}` | e.g. `/wp/v2/business-listing` |
| Media | `/wp/v2/media` | Upload via POST with `Content-Type: multipart/form-data` |
| Categories | `/wp/v2/categories` | Taxonomy `category` |
| Tags | `/wp/v2/tags` | Taxonomy `post_tag` |
| Custom taxonomies | `/wp/v2/{taxonomy}` | e.g. `/wp/v2/business-category` |
| Users | `/wp/v2/users` | `/me` for current user |
| Search | `/wp/v2/search` | Full site search with type filter |
| Settings | `/wp/v2/settings` | Site title, tagline, timezone, etc. |
| Navigation | `/wp/v2/navigation` | Navigation menus |
| Menu Items | `/wp/v2/menu-items` | Individual menu links |
| Blocks | `/wp/v2/blocks` | Reusable block patterns |

## Using `_fields` and `_embed`

**`_fields`** — critical for saving bandwidth. Only request what you need:

```bash
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts?_fields=id,title,slug,status,date,categories"
```

**`_embed`** — expands related resources (author name/avatar, featured image URL) inline:

```bash
# Single post with author + featured media inline
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts/123?_embed" | python3 -c "
import json, sys
d = json.load(sys.stdin)
author = d.get('_embedded',{}).get('author',[{}])[0].get('name','?')
media_url = d.get('_embedded',{}).get('wp:featuredmedia',[{}])[0].get('source_url','(none)')
print(f'Autor: {author}')
print(f'Featured: {media_url}')
"
```

## Using the Python CLI (wp-client.py)

The script lives at `scripts/wp-client.py` inside this skill directory. All commands:

```bash
# Set once, then run any command
export WP_URL="..."
export WP_USER="..."
export WP_PASS="..."

SCRIPT=~/.hermes/skills/wordpress-troubleshooting/wp-rest-api/scripts/wp-client.py
```

### discover — Full site audit (start here for any new site)
```bash
python3 $SCRIPT discover
```
Shows: user info, all post types + rest_base, all taxonomies + which post types they belong to, ACF availability, content counts for each type.

### list — Paginated listing
```bash
python3 $SCRIPT list posts --status publish --per-page 10
python3 $SCRIPT list business-listing --status publish --fields id,title,status
python3 $SCRIPT list pages --per-page 5 --page 2
```

### get, get-by-slug — Single item
```bash
python3 $SCRIPT get posts 123
python3 $SCRIPT get posts 123 --embed          # includes author/media inline
python3 $SCRIPT get-by-slug posts hello-world
```

### create, update, delete — CRUD
```bash
python3 $SCRIPT create posts '{"title":"New Post","content":"<p>Body</p>","status":"publish","categories":[1]}'
python3 $SCRIPT update posts 123 '{"title":"Updated Title","status":"draft"}'
python3 $SCRIPT delete posts 123              # trash
python3 $SCRIPT delete posts 123 --force      # permanent
```

### count — Quick totals
```bash
python3 $SCRIPT count business-listing --status publish
python3 $SCRIPT count posts --status draft
python3 $SCRIPT count posts                      # all statuses
```

### search — Full site text search
```bash
python3 $SCRIPT search "ranch"
python3 $SCRIPT search "ranch" --type post
```

### taxonomy — List taxonomy terms
```bash
python3 $SCRIPT taxonomy categories --per-page 100
python3 $SCRIPT taxonomy business-category
```

### settings — Site settings
```bash
python3 $SCRIPT settings                        # get current settings
python3 $SCRIPT settings --set '{"title":"My Site","description":"Tagline here"}'
```

### types, taxonomies — Schema exploration
```bash
python3 $SCRIPT types           # all post types + rest_base
python3 $SCRIPT taxonomies      # all taxonomies + linked types
```

## Common operations (curl)

### 1. List posts with filters

```bash
# Published posts, 10 per page
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts?per_page=10&status=publish"

# Posts in a specific category
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts?categories=5&per_page=20"

# Posts by date range
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts?after=2026-01-01T00:00:00&before=2026-06-01T00:00:00"

# Just the fields I need
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts?_fields=id,title,slug,status,date,categories"

# Total count from headers
curl -sI -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts" | grep -i 'x-wp-total\|x-wp-totalpages'
```

**Pagination**: `?page=N` (1-indexed) + `?per_page=N` (max 100). Check `X-WP-Total` / `X-WP-TotalPages` response headers.

### 2. Get a single post

```bash
# By ID
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts/123" | python3 -m json.tool

# By slug
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts?slug=my-post-slug" | python3 -m json.tool

# With embedded author + featured image
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts/123?_embed" | python3 -m json.tool
```

### 3. Create a post

```bash
curl -s -X POST -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Post Title",
    "content": "<!-- wp:paragraph --><p>Post content here.</p><!-- /wp:paragraph -->",
    "status": "publish",
    "categories": [1, 5],
    "tags": [3, 7],
    "slug": "my-post-slug"
  }' | python3 -m json.tool
```

**Status values**: `publish`, `draft`, `pending`, `private`, `future` (requires `date` field).

### 4. Update a post

```bash
# PATCH sends only changed fields
curl -s -X PATCH -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts/123" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "status": "draft"}' | python3 -m json.tool
```

### 5. Delete a post

```bash
# Trash (default)
curl -s -X DELETE -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts/123"

# Force delete (bypasses trash)
curl -s -X DELETE -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts/123?force=true"
```

### 6. Custom Post Types

CPTs work the same as posts — use their `rest_base`:

```bash
# List
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/business-listing?per_page=5&status=publish"

# Get
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/business-listing/4081" | python3 -m json.tool

# Create with custom taxonomy IDs
curl -s -X POST -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/business-listing" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Business", "status": "publish", "business-category": [126], "business-tag": [201, 274]}' | python3 -m json.tool

# Update
curl -s -X PATCH -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/business-listing/4081" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Business Name"}'

# Delete
curl -s -X DELETE -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/business-listing/4081"
```

### 7. Taxonomies

```bash
# List all categories
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/categories?per_page=100&hide_empty=false"

# Create a category
curl -s -X POST -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/categories" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Category", "slug": "new-category", "parent": 0}'

# Same for any custom taxonomy
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/business-category?per_page=100"
```

**Finding taxonomy slugs**: CPT responses often include custom taxonomy fields (e.g. `business-category`, `business-tag`, `listing-tier`). Query those taxonomy endpoints to see term IDs and names.

### 8. Media (upload)

```bash
# Upload a local image — returns media ID
curl -s -X POST -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/media" \
  -H "Content-Disposition: attachment; filename=photo.jpg" \
  -H "Content-Type: image/jpeg" \
  --data-binary @/path/to/photo.jpg | python3 -m json.tool

# Use returned `id` as `featured_media` on a post
curl -s -X PATCH -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/posts/123" \
  -H "Content-Type: application/json" \
  -d '{"featured_media": 456}'
```

### 9. Pages

```bash
# List
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/pages?per_page=10"

# Create
curl -s -X POST -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/pages" \
  -H "Content-Type: application/json" \
  -d '{"title": "About", "content": "<p>About us page</p>", "status": "publish"}'
```

### 10. Site settings

```bash
# Get current settings
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/settings" | python3 -m json.tool

# Update title and tagline
curl -s -X POST -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/settings" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Site", "description": "A great site"}'
```

### 11. Navigation menus

```bash
# List navigation menus
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/navigation?per_page=50"

# List menu items
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/menu-items?per_page=100"
```

### 12. Search

```bash
# Full text search
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/search?search=ranch&per_page=10"

# Search specific post type
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/search?search=ranch&type=post&per_page=10"
```

### 13. Meta fields / ACF

```bash
# Check if ACF REST API is active
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/acf/v3/options/options"

# Check ACF data on a specific post
curl -s -u "$WP_USER:$WP_PASS" "$WP_URL/wp-json/wp/v2/business-listing/4081" | python3 -c "
import json, sys
d = json.load(sys.stdin)
acf = d.get('acf', [])
meta = {k:v for k,v in d.get('meta', {}).items() if not k.startswith('_')}
print('ACF:', json.dumps(acf, indent=2)[:300])
print('Meta:', json.dumps(meta, indent=2)[:300])
"
```

## Discovery workflow

When handed a new WP site, run the Python client:

```bash
python3 $SCRIPT discover
```

This one command does it all: tests auth, lists all post types + rest_base, lists all taxonomies + which types they belong to, checks for ACF REST, and shows content counts per type.

Manual equivalent:
1. **Test auth**: `GET /wp/v2/users/me`
2. **List post types**: `GET /wp/v2/types`
3. **List taxonomies**: `GET /wp/v2/taxonomies`
4. **Check ACF**: hit ACF endpoints
5. **Sample data**: grab 1 item each of the main types to understand structure

## Pitfalls

- **Application Passwords contain spaces** — always use `-u "$USER:$PASS"` (quoted). Never put auth in a variable and expand it unquoted.
- **Taxonomy IDs, not slugs** — post creation uses numeric term IDs. Look them up from the taxonomy endpoint first.
- **Pagination cap at 100** — use `page=N` to iterate. The Python CLI auto-paginates; curl needs manual loops.
- **Content format** — WordPress 5.0+ expects block HTML. Plain `<p>` tags work but Gutenberg may not offer full editing. Use `<!-- wp:paragraph --><p>text</p><!-- /wp:paragraph -->` for proper block content.
- **HTML entities** — WP returns `&#8211;` for en-dashes, `&#038;` for ampersands. Decode with: `python3 -c 'import html; print(html.unescape("text"))'`
- **Empty `acf` field** — `acf: []` doesn't mean no ACF data exists; ACF REST endpoint may not be active. Check the Admin UI.
- **Featured images** — set via `featured_media` field with a numeric media ID from `/wp/v2/media`.
- **CORS/blockers** — some WP configs block REST API from external IPs. If curl fails with 403/401 when credentials are correct, a security plugin may be blocking.
- **Response headers** — use `-sI` (HEAD request) or `-s -o /dev/null -w "%{http_code}"` to check status without downloading body.
- **Encoding** — the Python CLI handles JSON and HTML entities. For curl, always pipe through `| python3 -m json.tool` for readability.