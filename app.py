from flask import Flask, g, render_template_string, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

# ====================================
# DB CONFIG
# ====================================
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "A27050aa",
    "host": "localhost",
    "port": 5433,
}

app = Flask(__name__)
app.secret_key = "secret"


# ====================================
# DB CONNECTION
# ====================================
def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(**DB_CONFIG)
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db:
        db.close()


# ====================================
# SHARED LAYOUT & STYLES
# ====================================
BASE_HTML_TOP = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Theater Inventory</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root{
      --bg:#0b1020;
      --card-bg:#131933;
      --accent:#ffb347;
      --accent-soft:rgba(255,179,71,0.14);
      --accent-strong:#ff9f1c;
      --text:#f5f7ff;
      --muted:#a0a4c0;
      --border:#262b45;
      --danger:#ff4b5c;
    }
    *{box-sizing:border-box;}
    body{
      margin:0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: radial-gradient(circle at top, #18213f 0, #050814 55%, #000 100%);
      color:var(--text);
    }
    a{color:var(--accent-strong); text-decoration:none;}
    a:hover{text-decoration:underline;}
    .layout{display:flex; min-height:100vh;}
    .sidebar{
      width:220px;
      background:rgba(8,12,26,0.96);
      border-right:1px solid var(--border);
      padding:1.5rem 1rem;
      position:sticky;
      top:0;
      height:100vh;
    }
    .brand{
      font-weight:600;
      letter-spacing:0.04em;
      font-size:1.1rem;
      display:flex;
      align-items:center;
      gap:.5rem;
      margin-bottom:1.5rem;
    }
    .pill{
      width:26px;
      height:26px;
      border-radius:999px;
      background: conic-gradient(from 210deg, #ff9f1c, #ffbf69, #cbf3f0, #2ec4b6, #ff9f1c);
    }
    .nav-section-title{
      font-size:.8rem;
      text-transform:uppercase;
      letter-spacing:.12em;
      color:var(--muted);
      margin:1rem 0 .35rem;
    }
    .nav-list{list-style:none; padding:0;margin:0;}
    .nav-item{margin-bottom:.2rem;}
    .nav-link{
      display:flex;
      align-items:center;
      gap:.4rem;
      padding:.45rem .65rem;
      border-radius:.55rem;
      color:var(--muted);
      font-size:.9rem;
    }
    .nav-link:hover{
      background:rgba(255,255,255,0.04);
      color:var(--text);
      text-decoration:none;
    }
    .nav-link.active{
      background:var(--accent-soft);
      color:var(--accent-strong);
    }
    .main{
      flex:1;
      padding:1.5rem 2rem 2.5rem;
      max-width:1100px;
      margin:0 auto;
    }
    .page-header{
      display:flex;
      justify-content:space-between;
      align-items:flex-end;
      gap:1rem;
      margin-bottom:1.25rem;
    }
    h1{
      font-size:1.6rem;
      margin:0;
    }
    .page-subtitle{
      margin:0;
      color:var(--muted);
      font-size:.9rem;
    }
    .card{
      background:rgba(11,16,37,0.9);
      border-radius:1rem;
      padding:1.25rem 1.4rem;
      border:1px solid rgba(255,255,255,0.03);
      box-shadow:0 18px 45px rgba(0,0,0,0.55);
    }
    .flash-list{list-style:none; padding:0;margin:0 0 1rem;}
    .flash-list li{
      background:var(--accent-soft);
      border:1px solid rgba(255,179,71,0.5);
      color:var(--accent-strong);
      padding:.5rem .75rem;
      border-radius:.65rem;
      font-size:.86rem;
      margin-bottom:.35rem;
      display:flex;
      align-items:center;
      gap:.35rem;
    }
    .badge-dot{
      width:8px;
      height:8px;
      border-radius:999px;
      background:var(--accent-strong);
    }

    table{
      width:100%;
      border-collapse:collapse;
      font-size:.9rem;
    }
    thead tr{background:rgba(255,255,255,0.02);}
    th,td{
      padding:.6rem .75rem;
      border-bottom:1px solid var(--border);
      text-align:left;
    }
    tbody tr:hover{
      background:rgba(255,255,255,0.03);
    }
    th{
      font-weight:500;
      color:var(--muted);
      font-size:.78rem;
      text-transform:uppercase;
      letter-spacing:.09em;
    }
    .status-pill{
      padding:.17rem .5rem;
      border-radius:999px;
      font-size:.75rem;
      font-weight:500;
    }
    .status-in{background:rgba(46,196,182,0.18); color:#2ec4b6;}
    .status-out{background:rgba(255,75,92,0.16); color:#ff6b81;}

    .btn{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      border-radius:.6rem;
      padding:.4rem .85rem;
      font-size:.85rem;
      font-weight:500;
      border:1px solid transparent;
      cursor:pointer;
      background:transparent;
      color:var(--text);
      text-decoration:none;
      gap:.35rem;
    }
    .btn-primary{
      background:linear-gradient(135deg, var(--accent-strong), #ffbf69);
      color:#1b1204;
      box-shadow:0 10px 30px rgba(255,159,28,0.35);
    }
    .btn-primary:hover{
      filter:brightness(1.03);
      text-decoration:none;
    }
    .btn-ghost{
      border-color:rgba(255,255,255,0.12);
      background:rgba(255,255,255,0.02);
      color:var(--muted);
    }
    .btn-ghost:hover{
      background:rgba(255,255,255,0.06);
      color:var(--text);
      text-decoration:none;
    }
    .btn-danger{
      border-color:rgba(255,75,92,0.6);
      color:var(--danger);
    }
    .btn-row{
      display:flex;
      flex-wrap:wrap;
      gap:.5rem;
      margin-bottom:1rem;
    }

    .form-grid{
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
      gap:.9rem 1.1rem;
      margin-bottom:1.1rem;
    }
    .field label{
      display:block;
      font-size:.78rem;
      font-weight:500;
      letter-spacing:.08em;
      text-transform:uppercase;
      color:var(--muted);
      margin-bottom:.25rem;
    }
    input[type="text"],
    input[type="email"],
    select{
      width:100%;
      padding:.45rem .55rem;
      border-radius:.5rem;
      border:1px solid var(--border);
      background:rgba(4,7,20,0.9);
      color:var(--text);
      font-size:.9rem;
    }
    input[type="text"]:focus,
    input[type="email"]:focus,
    select:focus{
      outline:none;
      border-color:var(--accent-strong);
      box-shadow:0 0 0 1px rgba(255,159,28,0.5);
    }
    .search-row{
      display:flex;
      flex-wrap:wrap;
      align-items:center;
      gap:.6rem;
      margin-bottom:1rem;
    }
    .search-row input[type="text"]{
      max-width:260px;
    }
    .chip{
      font-size:.78rem;
      padding:.1rem .5rem;
      border-radius:999px;
      background:rgba(255,255,255,0.03);
      border:1px solid rgba(255,255,255,0.06);
      color:var(--muted);
    }
    @media (max-width:800px){
      .layout{flex-direction:column;}
      .sidebar{
        width:100%;
        height:auto;
        position:static;
        display:flex;
        flex-wrap:wrap;
        align-items:center;
        gap:1rem;
      }
      .main{padding:1.25rem 1.15rem 1.8rem;}
    }
  </style>
</head>
<body>
<div class="layout">
  <aside class="sidebar">
    <div class="brand">
      <div class="pill"></div>
      <div>
        <div>Theater Inventory</div>
        <div style="font-size:.72rem;color:var(--muted);">Costumes • Props • Gear</div>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">Browse</div>
      <ul class="nav-list">
        <li class="nav-item"><a class="nav-link {{ 'active' if active_page=='home' else '' }}" href="{{ url_for('index') }}">Overview</a></li>
        <li class="nav-item"><a class="nav-link {{ 'active' if active_page=='items' else '' }}" href="{{ url_for('list_items') }}">Items</a></li>
        <li class="nav-item"><a class="nav-link {{ 'active' if active_page=='categories' else '' }}" href="{{ url_for('list_categories') }}">Categories</a></li>
        <li class="nav-item"><a class="nav-link {{ 'active' if active_page=='locations' else '' }}" href="{{ url_for('list_locations') }}">Storage</a></li>
      </ul>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">People & Shows</div>
      <ul class="nav-list">
        <li class="nav-item"><a class="nav-link {{ 'active' if active_page=='members' else '' }}" href="{{ url_for('list_members') }}">Members</a></li>
        <li class="nav-item"><a class="nav-link {{ 'active' if active_page=='productions' else '' }}" href="{{ url_for('list_productions') }}">Productions</a></li>
        <li class="nav-item"><a class="nav-link {{ 'active' if active_page=='checkouts' else '' }}" href="{{ url_for('list_checkouts') }}">Checkouts</a></li>
      </ul>
    </div>
  </aside>

  <main class="main">
'''

BASE_HTML_BOTTOM = '''
  </main>
</div>
</body>
</html>
'''

FLASH_BLOCK = '''
{% with msgs = get_flashed_messages() %}
  {% if msgs %}
    <ul class="flash-list">
      {% for m in msgs %}
        <li><span class="badge-dot"></span> {{ m }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
'''


# ====================================
# HOME
# ====================================
@app.route("/")
def index():
    inner = f"""
    <div class="page-header">
      <div>
        <h1>Overview</h1>
        <p class="page-subtitle">Quick actions and shortcuts to your inventory system.</p>
      </div>
    </div>

    {FLASH_BLOCK}

    <!-- Quick Actions -->
    <div class="card" style="margin-bottom:1.25rem;">
      <h2 style="font-size:1rem;margin-top:0;margin-bottom:.6rem;">Quick Actions</h2>
      <div class="btn-row">
        <a href="{{{{ url_for('list_items') }}}}" class="btn btn-primary">View all items</a>
        <a href="{{{{ url_for('list_checkouts') }}}}" class="btn btn-ghost">View checkouts</a>
        <a href="{{{{ url_for('new_checkout') }}}}" class="btn btn-ghost">New checkout</a>
      </div>
    </div>

    <!-- Two main categories of navigation -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.1rem;">

      <!-- Inventory Structure card -->
      <div class="card" style="padding:1rem 1.1rem;">
        <div style="font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-bottom:.25rem;">
          Inventory Structure
        </div>
        <div style="font-size:1.05rem;font-weight:500;margin-bottom:.35rem;">
          Categories &amp; Storage
        </div>
        <p style="font-size:.86rem;color:var(--muted);margin:0 0 .75rem;">
          Manage how items are organized by category and where they are stored.
        </p>
        <div class="btn-row" style="margin-bottom:0;">
          <a href="{{{{ url_for('list_categories') }}}}" class="btn btn-ghost">Categories</a>
          <a href="{{{{ url_for('list_locations') }}}}" class="btn btn-ghost">Storage Locations</a>
        </div>
      </div>

      <!-- People & Shows card -->
      <div class="card" style="padding:1rem 1.1rem;">
        <div style="font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-bottom:.25rem;">
          People &amp; Shows
        </div>
        <div style="font-size:1.05rem;font-weight:500;margin-bottom:.35rem;">
          Members &amp; Productions
        </div>
        <p style="font-size:.86rem;color:var(--muted);margin:0 0 .75rem;">
          Track borrowers and the productions items are assigned to.
        </p>
        <div class="btn-row" style="margin-bottom:0;">
          <a href="{{{{ url_for('list_members') }}}}" class="btn btn-ghost">Members</a>
          <a href="{{{{ url_for('list_productions') }}}}" class="btn btn-ghost">Productions</a>
        </div>
      </div>

    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, active_page="home")


# ====================================
# MEMBERS
# ====================================
@app.route("/members")
def list_members():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT member_id, name, email, phone, role FROM Member ORDER BY name;"
    )
    members = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Members</h1>
        <p class="page-subtitle">Everyone who can borrow items from the inventory.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('add_member') }}}}" class="btn btn-primary">+ Add member</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>Name</th><th>Email</th><th>Phone</th><th>Role</th>
          </tr>
        </thead>
        <tbody>
        {{% for m in members %}}
          <tr>
            <td><a href="{{{{ url_for('member_detail', member_id=m.member_id) }}}}">{{{{ m.name }}}}</a></td>
            <td>{{{{ m.email or "" }}}}</td>
            <td>{{{{ m.phone or "" }}}}</td>
            <td>{{{{ m.role or "" }}}}</td>
          </tr>
        {{% endfor %}}
        {{% if not members %}}
          <tr><td colspan="4">(No members)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, members=members, active_page="members")


@app.route("/members/<int:member_id>")
def member_detail(member_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        "SELECT member_id, name, email, phone, role FROM Member WHERE member_id = %s;",
        (member_id,),
    )
    member = cur.fetchone()
    if not member:
        cur.close()
        flash("Member not found.")
        return redirect(url_for("list_members"))

    cur.execute(
        """
        SELECT
            i.item_id,
            i.tag_code,
            i.name,
            p.title AS production_title,
            ch.checkout_date,
            ch.notes
        FROM Checkout ch
        JOIN Item i ON ch.item_id = i.item_id
        LEFT JOIN Production p ON ch.production_id = p.production_id
        WHERE ch.member_id = %s
        ORDER BY ch.checkout_date DESC;
        """,
        (member_id,),
    )
    items = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>{{{{ member.name }}}}</h1>
        <p class="page-subtitle">Current and past checkouts for this member.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_members') }}}}" class="btn btn-ghost">← Back to members</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card" style="margin-bottom:1rem;">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem;font-size:.9rem;color:var(--muted);">
        <div><strong>Role:</strong> {{{{ member.role or 'N/A' }}}}</div>
        <div><strong>Email:</strong> {{{{ member.email or 'N/A' }}}}</div>
        <div><strong>Phone:</strong> {{{{ member.phone or 'N/A' }}}}</div>
      </div>
    </div>

    <div class="card">
      <h2 style="font-size:1rem;margin-top:0;margin-bottom:.75rem;">Checkouts</h2>
      <table>
        <thead>
          <tr>
            <th>Tag</th><th>Item</th><th>Production</th>
            <th>Date Out</th><th>Notes</th>
          </tr>
        </thead>
        <tbody>
        {{% for i in items %}}
          <tr>
            <td>{{{{ i.tag_code }}}}</td>
            <td>{{{{ i.name }}}}</td>
            <td>{{{{ i.production_title or '' }}}}</td>
            <td>{{{{ i.checkout_date.strftime('%m/%d/%Y') }}}}</td>
            <td>{{{{ i.notes or '' }}}}</td>
          </tr>
        {{% endfor %}}
        {{% if not items %}}
          <tr><td colspan="5">(No checkouts for this member)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template, member=member, items=items, active_page="members"
    )


@app.route("/members/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        name = request.form["name"].strip()
        role = request.form["role"].strip() or None
        email = request.form["email"].strip() or None
        phone = request.form["phone"].strip() or None

        if not name:
            flash("Name required.")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Member (name, role, email, phone)
                VALUES (%s, %s, %s, %s);
                """,
                (name, role, email, phone),
            )
            conn.commit()
            cur.close()
            flash("Member added.")
            return redirect(url_for("list_members"))

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Add Member</h1>
        <p class="page-subtitle">Create a new person who can check out items.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_members') }}}}" class="btn btn-ghost">← Back to members</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="post">
        <div class="form-grid">
          <div class="field">
            <label for="name">Name *</label>
            <input id="name" type="text" name="name" required>
          </div>
          <div class="field">
            <label for="role">Role</label>
            <input id="role" type="text" name="role">
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" type="email" name="email">
          </div>
          <div class="field">
            <label for="phone">Phone</label>
            <input id="phone" type="text" name="phone">
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Save member</button>
      </form>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, active_page="members")


# ====================================
# PRODUCTIONS
# ====================================
@app.route("/productions")
def list_productions():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT production_id, title, season, open_date, close_date
        FROM Production
        ORDER BY title;
        """
    )
    productions = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Productions</h1>
        <p class="page-subtitle">Shows and seasons that items can be checked out for.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('add_production') }}}}" class="btn btn-primary">+ Add production</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>Title</th><th>Season</th><th>Open</th><th>Close</th>
          </tr>
        </thead>
        <tbody>
        {{% for p in productions %}}
          <tr>
            <td><a href="{{{{ url_for('production_detail', production_id=p.production_id) }}}}">{{{{ p.title }}}}</a></td>
            <td>{{{{ p.season or "" }}}}</td>
            <td>{{{{ p.open_date.strftime('%m/%d/%Y') if p.open_date else "" }}}}</td>
            <td>{{{{ p.close_date.strftime('%m/%d/%Y') if p.close_date else "" }}}}</td>
          </tr>
        {{% endfor %}}
        {{% if not productions %}}
          <tr><td colspan="4">(No productions)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template, productions=productions, active_page="productions"
    )


@app.route("/productions/<int:production_id>")
def production_detail(production_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        """
        SELECT production_id, title, season, open_date, close_date
        FROM Production
        WHERE production_id = %s;
        """,
        (production_id,),
    )
    production = cur.fetchone()
    if not production:
        cur.close()
        flash("Production not found.")
        return redirect(url_for("list_productions"))

    cur.execute(
        """
        SELECT
            i.item_id,
            i.tag_code,
            i.name,
            m.name AS member_name,
            ch.checkout_date,
            ch.notes
        FROM Checkout ch
        JOIN Item i ON ch.item_id = i.item_id
        LEFT JOIN Member m ON ch.member_id = m.member_id
        WHERE ch.production_id = %s
        ORDER BY ch.checkout_date DESC;
        """,
        (production_id,),
    )
    items = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>{{{{ production.title }}}}</h1>
        <p class="page-subtitle">Items checked out for this production.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_productions') }}}}" class="btn btn-ghost">← Back to productions</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card" style="margin-bottom:1rem;">
      <div style="display:flex;flex-wrap:wrap;gap:1rem;font-size:.9rem;color:var(--muted);">
        <div><strong>Season:</strong> {{{{ production.season or 'N/A' }}}}</div>
        <div>
          <strong>Run:</strong>
          {{{{ production.open_date.strftime('%m/%d/%Y') if production.open_date else 'N/A' }}}}
          &ndash;
          {{{{ production.close_date.strftime('%m/%d/%Y') if production.close_date else 'N/A' }}}}
        </div>
      </div>
    </div>

    <div class="card">
      <h2 style="font-size:1rem;margin-top:0;margin-bottom:.75rem;">Checkouts</h2>
      <table>
        <thead>
          <tr>
            <th>Tag</th><th>Item</th><th>Checked Out To</th>
            <th>Date Out</th><th>Notes</th>
          </tr>
        </thead>
        <tbody>
        {{% for i in items %}}
          <tr>
            <td>{{{{ i.tag_code }}}}</td>
            <td>{{{{ i.name }}}}</td>
            <td>{{{{ i.member_name or '' }}}}</td>
            <td>{{{{ i.checkout_date.strftime('%m/%d/%Y') }}}}</td>
            <td>{{{{ i.notes or '' }}}}</td>
          </tr>
        {{% endfor %}}
        {{% if not items %}}
          <tr><td colspan="5">(No checkouts for this production)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template, production=production, items=items, active_page="productions"
    )


@app.route("/productions/add", methods=["GET", "POST"])
def add_production():
    if request.method == "POST":
        title = request.form["title"].strip()
        season = request.form["season"].strip() or None
        open_date = request.form["open_date"].strip() or None
        close_date = request.form["close_date"].strip() or None

        if not title:
            flash("Title required.")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Production (title, season, open_date, close_date)
                VALUES (%s, %s, %s, %s);
                """,
                (title, season, open_date, close_date),
            )
            conn.commit()
            cur.close()
            flash("Production added.")
            return redirect(url_for("list_productions"))

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Add Production</h1>
        <p class="page-subtitle">Create a new show or season in the schedule.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_productions') }}}}" class="btn btn-ghost">← Back to productions</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="post">
        <div class="form-grid">
          <div class="field">
            <label for="title">Title *</label>
            <input id="title" type="text" name="title" required>
          </div>
          <div class="field">
            <label for="season">Season</label>
            <input id="season" type="text" name="season" placeholder="2025–2026">
          </div>
          <div class="field">
            <label for="open_date">Open date (YYYY-MM-DD)</label>
            <input id="open_date" type="text" name="open_date">
          </div>
          <div class="field">
            <label for="close_date">Close date (YYYY-MM-DD)</label>
            <input id="close_date" type="text" name="close_date">
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Save production</button>
      </form>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, active_page="productions")


# ====================================
# CATEGORIES
# ====================================
@app.route("/categories")
def list_categories():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT category_id, name, description FROM Category ORDER BY name;"
    )
    categories = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Categories</h1>
        <p class="page-subtitle">Group similar items together (shoes, hats, dresses...)</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('add_category') }}}}" class="btn btn-primary">+ Add category</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>Name</th><th>Description</th>
          </tr>
        </thead>
        <tbody>
        {{% for c in categories %}}
          <tr>
            <td><a href="{{{{ url_for('category_detail', category_id=c.category_id) }}}}">{{{{ c.name }}}}</a></td>
            <td>{{{{ c.description or "" }}}}</td>
          </tr>
        {{% endfor %}}
        {{% if not categories %}}
          <tr><td colspan="2">(No categories)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template, categories=categories, active_page="categories"
    )


@app.route("/categories/<int:category_id>")
def category_detail(category_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        "SELECT category_id, name, description FROM Category WHERE category_id = %s;",
        (category_id,),
    )
    category = cur.fetchone()
    if not category:
        cur.close()
        flash("Category not found.")
        return redirect(url_for("list_categories"))

    search = request.args.get("q", "").strip()

    where_extra = ""
    params = [category_id]
    if search:
        where_extra = """
          AND (
            i.tag_code ILIKE %s OR
            i.name ILIKE %s OR
            COALESCE(l.code, '') ILIKE %s OR
            COALESCE(i.size, '') ILIKE %s OR
            COALESCE(i.color, '') ILIKE %s OR
            COALESCE(i.notes, '') ILIKE %s
          )
        """
        pattern = f"%{search}%"
        params.extend([pattern] * 6)

    cur.execute(
        """
        SELECT
            i.item_id,
            i.tag_code,
            i.name,
            l.code AS location_code,
            i.size,
            i.color,
            i.notes,
            EXISTS (
                SELECT 1
                FROM Checkout ch
                WHERE ch.item_id = i.item_id
            ) AS is_out
        FROM Item i
        LEFT JOIN StorageLocation l ON i.location_id = l.location_id
        WHERE i.category_id = %s
        """ + where_extra + """
        ORDER BY i.tag_code;
        """,
        params,
    )
    items = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>{{{{ category.name }}}}</h1>
        <p class="page-subtitle">All items in this category.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_categories') }}}}" class="btn btn-ghost">← Back to categories</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card" style="margin-bottom:1rem;">
      <p style="margin:0;font-size:.9rem;color:var(--muted);">
        {{{{ category.description or 'No description yet.' }}}}
      </p>
    </div>

    <div class="card">
      <form method="get" class="search-row">
        <div class="field" style="margin:0;">
          <label for="q">Search items</label>
          <input id="q" type="text" name="q" value="{{{{ q or '' }}}}" placeholder="Tag, name, size, color, notes...">
        </div>
        <button type="submit" class="btn btn-ghost">Search</button>
        {{% if q %}}
          <a href="{{{{ url_for('category_detail', category_id=category.category_id) }}}}" class="btn btn-ghost">Clear</a>
          <span class="chip">Filtering by: "{{{{ q }}}}"</span>
        {{% endif %}}
      </form>

      <table>
        <thead>
          <tr>
            <th>Tag</th>
            <th>Name</th>
            <th>Location</th>
            <th>Size</th>
            <th>Color</th>
            <th>Notes</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
        {{% for i in items %}}
          <tr>
            <td>{{{{ i.tag_code }}}}</td>
            <td>{{{{ i.name }}}}</td>
            <td>{{{{ i.location_code or '' }}}}</td>
            <td>{{{{ i.size or '' }}}}</td>
            <td>{{{{ i.color or '' }}}}</td>
            <td>{{{{ i.notes or '' }}}}</td>
            <td>
              <span class="status-pill {{{{ 'status-out' if i.is_out else 'status-in' }}}}">
                {{{{ 'Checked out' if i.is_out else 'In stock' }}}}
              </span>
            </td>
            <td>
              <div class="btn-row" style="margin:0;">
                <a href="{{{{ url_for('edit_item', item_id=i.item_id) }}}}" class="btn btn-ghost">Edit</a>
                <a href="{{{{ url_for('delete_item', item_id=i.item_id) }}}}"
                   class="btn btn-danger"
                   onclick="return confirm('Delete this item?');">
                  Delete
                </a>
              </div>
            </td>
          </tr>
        {{% endfor %}}
        {{% if not items %}}
          <tr><td colspan="8">(No items in this category)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template, category=category, items=items, q=search, active_page="categories"
    )


@app.route("/categories/add", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form["name"].strip()
        desc = request.form["description"].strip() or None

        if not name:
            flash("Name required.")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Category (name, description)
                VALUES (%s, %s);
                """,
                (name, desc),
            )
            conn.commit()
            cur.close()
            flash("Category added.")
            return redirect(url_for("list_categories"))

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Add Category</h1>
        <p class="page-subtitle">Create a new grouping for your inventory.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_categories') }}}}" class="btn btn-ghost">← Back to categories</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="post">
        <div class="form-grid">
          <div class="field">
            <label for="name">Name *</label>
            <input id="name" type="text" name="name" required>
          </div>
          <div class="field" style="grid-column:1/-1;">
            <label for="description">Description</label>
            <input id="description" type="text" name="description" placeholder="Optional notes about this category">
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Save category</button>
      </form>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, active_page="categories")


# ====================================
# STORAGE LOCATIONS
# ====================================
@app.route("/locations")
def list_locations():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT location_id, code, description FROM StorageLocation ORDER BY code;"
    )
    locations = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Storage Locations</h1>
        <p class="page-subtitle">Where everything actually lives backstage.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('add_location') }}}}" class="btn btn-primary">+ Add location</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>Code</th><th>Description</th>
          </tr>
        </thead>
        <tbody>
        {{% for l in locations %}}
          <tr>
            <td><a href="{{{{ url_for('location_detail', location_id=l.location_id) }}}}">{{{{ l.code }}}}</a></td>
            <td>{{{{ l.description or "" }}}}</td>
          </tr>
        {{% endfor %}}
        {{% if not locations %}}
          <tr><td colspan="2">(No storage locations)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template, locations=locations, active_page="locations"
    )


@app.route("/locations/<int:location_id>")
def location_detail(location_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        "SELECT location_id, code, description FROM StorageLocation WHERE location_id = %s;",
        (location_id,),
    )
    location = cur.fetchone()
    if not location:
        cur.close()
        flash("Storage location not found.")
        return redirect(url_for("list_locations"))

    search = request.args.get("q", "").strip()

    where_extra = ""
    params = [location_id]
    if search:
        where_extra = """
          AND (
            i.tag_code ILIKE %s OR
            i.name ILIKE %s OR
            COALESCE(c.name, '') ILIKE %s OR
            COALESCE(i.size, '') ILIKE %s OR
            COALESCE(i.color, '') ILIKE %s OR
            COALESCE(i.notes, '') ILIKE %s
          )
        """
        pattern = f"%{search}%"
        params.extend([pattern] * 6)

    cur.execute(
        """
        SELECT
            i.item_id,
            i.tag_code,
            i.name,
            c.name AS category_name,
            i.size,
            i.color,
            i.notes,
            EXISTS (
                SELECT 1
                FROM Checkout ch
                WHERE ch.item_id = i.item_id
            ) AS is_out
        FROM Item i
        LEFT JOIN Category c ON i.category_id = c.category_id
        WHERE i.location_id = %s
        """ + where_extra + """
        ORDER BY i.tag_code;
        """,
        params,
    )
    items = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Storage: {{{{ location.code }}}}</h1>
        <p class="page-subtitle">Items currently recorded at this location.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_locations') }}}}" class="btn btn-ghost">← Back to locations</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card" style="margin-bottom:1rem;">
      <p style="margin:0;font-size:.9rem;color:var(--muted);">
        {{{{ location.description or 'No description yet.' }}}}
      </p>
    </div>

    <div class="card">
      <form method="get" class="search-row">
        <div class="field" style="margin:0;">
          <label for="q">Search items</label>
          <input id="q" type="text" name="q" value="{{{{ q or '' }}}}" placeholder="Tag, name, category, notes...">
        </div>
        <button type="submit" class="btn btn-ghost">Search</button>
        {{% if q %}}
          <a href="{{{{ url_for('location_detail', location_id=location.location_id) }}}}" class="btn btn-ghost">Clear</a>
          <span class="chip">Filtering by: "{{{{ q }}}}"</span>
        {{% endif %}}
      </form>

      <table>
        <thead>
          <tr>
            <th>Tag</th>
            <th>Name</th>
            <th>Category</th>
            <th>Size</th>
            <th>Color</th>
            <th>Notes</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
        {{% for i in items %}}
          <tr>
            <td>{{{{ i.tag_code }}}}</td>
            <td>{{{{ i.name }}}}</td>
            <td>{{{{ i.category_name or '' }}}}</td>
            <td>{{{{ i.size or '' }}}}</td>
            <td>{{{{ i.color or '' }}}}</td>
            <td>{{{{ i.notes or '' }}}}</td>
            <td>
              <span class="status-pill {{{{ 'status-out' if i.is_out else 'status-in' }}}}">
                {{{{ 'Checked out' if i.is_out else 'In stock' }}}}
              </span>
            </td>
            <td>
              <div class="btn-row" style="margin:0;">
                <a href="{{{{ url_for('edit_item', item_id=i.item_id) }}}}" class="btn btn-ghost">Edit</a>
                <a href="{{{{ url_for('delete_item', item_id=i.item_id) }}}}"
                   class="btn btn-danger"
                   onclick="return confirm('Delete this item?');">
                  Delete
                </a>
              </div>
            </td>
          </tr>
        {{% endfor %}}
        {{% if not items %}}
          <tr><td colspan="8">(No items stored here)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template,
        location=location,
        items=items,
        q=search,
        active_page="locations",
    )


@app.route("/locations/add", methods=["GET", "POST"])
def add_location():
    if request.method == "POST":
        code = request.form["code"].strip()
        desc = request.form["description"].strip() or None

        if not code:
            flash("Code required.")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO StorageLocation (code, description)
                VALUES (%s, %s);
                """,
                (code, desc),
            )
            conn.commit()
            cur.close()
            flash("Location added.")
            return redirect(url_for("list_locations"))

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Add Storage Location</h1>
        <p class="page-subtitle">Add a new rack, bin, room, or drawer.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_locations') }}}}" class="btn btn-ghost">← Back to locations</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="post">
        <div class="form-grid">
          <div class="field">
            <label for="code">Code *</label>
            <input id="code" type="text" name="code" required placeholder="E.g. R1-Bin3">
          </div>
          <div class="field" style="grid-column:1/-1;">
            <label for="description">Description</label>
            <input id="description" type="text" name="description" placeholder="Optional notes about this location">
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Save location</button>
      </form>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, active_page="locations")


# ====================================
# ITEMS
# ====================================
@app.route("/items")
def list_items():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    search = request.args.get("q", "").strip()

    base_query = """
        SELECT
            i.item_id,
            i.tag_code,
            i.name,
            c.name AS category_name,
            l.code AS location_code,
            i.size,
            i.color,
            i.notes,
            EXISTS (
                SELECT 1
                FROM Checkout ch
                WHERE ch.item_id = i.item_id
            ) AS is_out
        FROM Item i
        LEFT JOIN Category c ON i.category_id = c.category_id
        LEFT JOIN StorageLocation l ON i.location_id = l.location_id
        {where_clause}
        ORDER BY i.tag_code;
    """

    params = []
    if search:
        where_clause = """
        WHERE
            i.tag_code ILIKE %s OR
            i.name ILIKE %s OR
            COALESCE(c.name, '') ILIKE %s OR
            COALESCE(l.code, '') ILIKE %s OR
            COALESCE(i.size, '') ILIKE %s OR
            COALESCE(i.color, '') ILIKE %s OR
            COALESCE(i.notes, '') ILIKE %s
        """
        pattern = f"%{search}%"
        params = [pattern] * 7
    else:
        where_clause = ""

    cur.execute(base_query.format(where_clause=where_clause), params)
    items = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Items</h1>
        <p class="page-subtitle">The full library of costumes, props, and equipment.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('add_item') }}}}" class="btn btn-primary">+ Add item</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="get" class="search-row">
        <div class="field" style="margin:0;">
          <label for="q">Search items</label>
          <input id="q" type="text" name="q" value="{{{{ q or '' }}}}" placeholder="Tag, name, category, location, notes...">
        </div>
        <button type="submit" class="btn btn-ghost">Search</button>
        {{% if q %}}
          <a href="{{{{ url_for('list_items') }}}}" class="btn btn-ghost">Clear</a>
          <span class="chip">Filtering by: "{{{{ q }}}}"</span>
        {{% endif %}}
      </form>

      <table>
        <thead>
          <tr>
            <th>Tag</th>
            <th>Name</th>
            <th>Category</th>
            <th>Location</th>
            <th>Size</th>
            <th>Color</th>
            <th>Notes</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
        {{% for i in items %}}
          <tr>
            <td>{{{{ i.tag_code }}}}</td>
            <td>{{{{ i.name }}}}</td>
            <td>{{{{ i.category_name or '' }}}}</td>
            <td>{{{{ i.location_code or '' }}}}</td>
            <td>{{{{ i.size or '' }}}}</td>
            <td>{{{{ i.color or '' }}}}</td>
            <td>{{{{ i.notes or '' }}}}</td>
            <td>
              <span class="status-pill {{{{ 'status-out' if i.is_out else 'status-in' }}}}">
                {{{{ 'Checked out' if i.is_out else 'In stock' }}}}
              </span>
            </td>
            <td>
              <div class="btn-row" style="margin:0;">
                <a href="{{{{ url_for('edit_item', item_id=i.item_id) }}}}" class="btn btn-ghost">Edit</a>
                <a href="{{{{ url_for('delete_item', item_id=i.item_id) }}}}"
                   class="btn btn-danger"
                   onclick="return confirm('Delete this item?');">
                  Delete
                </a>
              </div>
            </td>
          </tr>
        {{% endfor %}}
        {{% if not items %}}
          <tr><td colspan="9">(No items)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, items=items, q=search, active_page="items")


@app.route("/items/add", methods=["GET", "POST"])
def add_item():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT category_id, name FROM Category ORDER BY name;")
    categories = cur.fetchall()
    cur.execute("SELECT location_id, code FROM StorageLocation ORDER BY code;")
    locations = cur.fetchall()
    cur.close()

    if request.method == "POST":
        tag_code = request.form["tag_code"].strip()
        name = request.form["name"].strip()
        category_id = request.form.get("category_id") or None
        location_id = request.form.get("location_id") or None
        size = request.form["size"].strip() or None
        color = request.form["color"].strip() or None
        notes = request.form["notes"].strip() or None

        if not tag_code or not name:
            flash("Tag code and name are required.")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Item
                  (tag_code, name, category_id, size, color, notes, location_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    tag_code,
                    name,
                    int(category_id) if category_id else None,
                    size,
                    color,
                    notes,
                    int(location_id) if location_id else None,
                ),
            )
            conn.commit()
            cur.close()
            flash("Item added.")
            return redirect(url_for("list_items"))

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Add Item</h1>
        <p class="page-subtitle">Add a new costume, prop, or other inventory item.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_items') }}}}" class="btn btn-ghost">← Back to items</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="post">
        <div class="form-grid">
          <div class="field">
            <label for="tag_code">Tag code *</label>
            <input id="tag_code" type="text" name="tag_code" required>
          </div>
          <div class="field">
            <label for="name">Name *</label>
            <input id="name" type="text" name="name" required>
          </div>

          <div class="field">
            <label for="category_id">Category</label>
            <select name="category_id" id="category_id">
              <option value="">-- none --</option>
              {{% for c in categories %}}
                <option value="{{{{ c.category_id }}}}">{{{{ c.name }}}}</option>
              {{% endfor %}}
            </select>
          </div>

          <div class="field">
            <label for="location_id">Location</label>
            <select name="location_id" id="location_id">
              <option value="">-- none --</option>
              {{% for l in locations %}}
                <option value="{{{{ l.location_id }}}}">{{{{ l.code }}}}</option>
              {{% endfor %}}
            </select>
          </div>

          <div class="field">
            <label for="size">Size</label>
            <input id="size" type="text" name="size">
          </div>
          <div class="field">
            <label for="color">Color</label>
            <input id="color" type="text" name="color">
          </div>
          <div class="field" style="grid-column:1/-1;">
            <label for="notes">Notes</label>
            <input id="notes" type="text" name="notes" placeholder="Extra details about condition, fit, etc.">
          </div>
        </div>

        <button type="submit" class="btn btn-primary">Save item</button>
      </form>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template, categories=categories, locations=locations, active_page="items"
    )


# ====================================
# CHECKOUTS
# ====================================
@app.route("/checkouts")
def list_checkouts():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        """
        SELECT
            ch.checkout_id,
            i.tag_code,
            i.name AS item_name,
            m.name AS member_name,
            p.title AS production_title,
            ch.checkout_date,
            ch.notes
        FROM Checkout ch
        JOIN Item i ON ch.item_id = i.item_id
        LEFT JOIN Member m ON ch.member_id = m.member_id
        LEFT JOIN Production p ON ch.production_id = p.production_id
        ORDER BY ch.checkout_date DESC;
        """
    )
    rows = cur.fetchall()
    cur.close()

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Checkouts</h1>
        <p class="page-subtitle">Who has what, and for which production.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('new_checkout') }}}}" class="btn btn-primary">+ New checkout</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>Tag</th><th>Item</th><th>Member</th>
            <th>Production</th><th>Date Out</th><th>Notes</th><th>Action</th>
          </tr>
        </thead>
        <tbody>
        {{% for r in rows %}}
          <tr>
            <td>{{{{ r.tag_code }}}}</td>
            <td>{{{{ r.item_name }}}}</td>
            <td>{{{{ r.member_name or '' }}}}</td>
            <td>{{{{ r.production_title or '' }}}}</td>
            <td>{{{{ r.checkout_date.strftime('%m/%d/%Y') }}}}</td>
            <td>{{{{ r.notes or '' }}}}</td>
            <td>
              <a href="{{{{ url_for('return_checkout', checkout_id=r.checkout_id) }}}}" class="btn btn-ghost">
                Mark returned
              </a>
            </td>
          </tr>
        {{% endfor %}}
        {{% if not rows %}}
          <tr><td colspan="7">(No checkouts)</td></tr>
        {{% endif %}}
        </tbody>
      </table>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(template, rows=rows, active_page="checkouts")


@app.route("/checkout", methods=["GET", "POST"])
def new_checkout():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Only include items that are NOT currently checked out
    cur.execute(
        """
        SELECT i.item_id, i.tag_code, i.name
        FROM Item i
        WHERE NOT EXISTS (
            SELECT 1
            FROM Checkout ch
            WHERE ch.item_id = i.item_id
        )
        ORDER BY i.tag_code;
        """
    )
    items = cur.fetchall()

    cur.execute("SELECT member_id, name FROM Member ORDER BY name;")
    members = cur.fetchall()

    cur.execute("SELECT production_id, title FROM Production ORDER BY title;")
    productions = cur.fetchall()

    cur.close()

    if request.method == "POST":
        item = request.form.get("item_id")
        member = request.form.get("member_id") or None
        prod = request.form.get("production_id") or None
        notes = request.form["notes"].strip() or None

        if not item:
            flash("Item is required.")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Checkout (item_id, member_id, production_id, notes)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    int(item),
                    int(member) if member else None,
                    int(prod) if prod else None,
                    notes,
                ),
            )
            conn.commit()
            cur.close()
            flash("Item checked out.")
            return redirect(url_for("list_checkouts"))

    inner = f"""
    <div class="page-header">
      <div>
        <h1>New Checkout</h1>
        <p class="page-subtitle">Assign an item to a member and optional production.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_checkouts') }}}}" class="btn btn-ghost">← Back to checkouts</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="post">
        <div class="form-grid">
          <div class="field">
            <label for="item_id">Item *</label>
            <select name="item_id" id="item_id" required>
              <option value="">-- choose item --</option>
              {{% for i in items %}}
                <option value="{{{{ i.item_id }}}}">{{{{ i.tag_code }}}} — {{{{ i.name }}}}</option>
              {{% endfor %}}
            </select>
          </div>

          <div class="field">
            <label for="member_id">Member</label>
            <select name="member_id" id="member_id">
              <option value="">-- none --</option>
              {{% for m in members %}}
                <option value="{{{{ m.member_id }}}}">{{{{ m.name }}}}</option>
              {{% endfor %}}
            </select>
          </div>

          <div class="field">
            <label for="production_id">Production</label>
            <select name="production_id" id="production_id">
              <option value="">-- none --</option>
              {{% for p in productions %}}
                <option value="{{{{ p.production_id }}}}">{{{{ p.title }}}}</option>
              {{% endfor %}}
            </select>
          </div>

          <div class="field" style="grid-column:1/-1;">
            <label for="notes">Notes</label>
            <input id="notes" type="text" name="notes" placeholder="Optional details (e.g., due date, quick fit notes)">
          </div>
        </div>

        <button type="submit" class="btn btn-primary">Checkout item</button>
      </form>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template,
        items=items,
        members=members,
        productions=productions,
        active_page="checkouts",
    )


@app.route("/return/<int:checkout_id>")
def return_checkout(checkout_id):
    conn = get_db()
    cur = conn.cursor()
    # Returning an item = delete that checkout row so the item becomes "In stock"
    cur.execute(
        "DELETE FROM Checkout WHERE checkout_id = %s;",
        (checkout_id,),
    )
    conn.commit()
    cur.close()
    flash("Item returned.")
    return redirect(url_for("list_checkouts"))


# ====================================
# EDIT / DELETE ITEMS
# ====================================
@app.route("/items/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Load item
    cur.execute(
        """
        SELECT item_id, tag_code, name, category_id, size, color, notes, location_id
        FROM Item
        WHERE item_id = %s;
        """,
        (item_id,),
    )
    item = cur.fetchone()
    if not item:
        cur.close()
        flash("Item not found.")
        return redirect(url_for("list_items"))

    # Load dropdown data
    cur.execute("SELECT category_id, name FROM Category ORDER BY name;")
    categories = cur.fetchall()
    cur.execute("SELECT location_id, code FROM StorageLocation ORDER BY code;")
    locations = cur.fetchall()
    cur.close()

    if request.method == "POST":
        tag_code = request.form["tag_code"].strip()
        name = request.form["name"].strip()
        category_id = request.form.get("category_id") or None
        location_id = request.form.get("location_id") or None
        size = request.form["size"].strip() or None
        color = request.form["color"].strip() or None
        notes = request.form["notes"].strip() or None

        if not tag_code or not name:
            flash("Tag code and name are required.")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE Item
                SET tag_code = %s,
                    name = %s,
                    category_id = %s,
                    size = %s,
                    color = %s,
                    notes = %s,
                    location_id = %s
                WHERE item_id = %s;
                """,
                (
                    tag_code,
                    name,
                    int(category_id) if category_id else None,
                    size,
                    color,
                    notes,
                    int(location_id) if location_id else None,
                    item_id,
                ),
            )
            conn.commit()
            cur.close()
            flash("Item updated.")
            return redirect(url_for("list_items"))

    inner = f"""
    <div class="page-header">
      <div>
        <h1>Edit Item</h1>
        <p class="page-subtitle">Update details for this inventory item.</p>
      </div>
      <div class="btn-row">
        <a href="{{{{ url_for('list_items') }}}}" class="btn btn-ghost">← Back to items</a>
      </div>
    </div>

    {FLASH_BLOCK}

    <div class="card">
      <form method="post">
        <div class="form-grid">
          <div class="field">
            <label for="tag_code">Tag code *</label>
            <input id="tag_code" type="text" name="tag_code" value="{{{{ item.tag_code }}}}" required>
          </div>
          <div class="field">
            <label for="name">Name *</label>
            <input id="name" type="text" name="name" value="{{{{ item.name }}}}" required>
          </div>

          <div class="field">
            <label for="category_id">Category</label>
            <select name="category_id" id="category_id">
              <option value="">-- none --</option>
              {{% for c in categories %}}
                <option value="{{{{ c.category_id }}}}" {{% if c.category_id == item.category_id %}}selected{{% endif %}}>
                  {{{{ c.name }}}}
                </option>
              {{% endfor %}}
            </select>
          </div>

          <div class="field">
            <label for="location_id">Location</label>
            <select name="location_id" id="location_id">
              <option value="">-- none --</option>
              {{% for l in locations %}}
                <option value="{{{{ l.location_id }}}}" {{% if l.location_id == item.location_id %}}selected{{% endif %}}>
                  {{{{ l.code }}}}
                </option>
              {{% endfor %}}
            </select>
          </div>

          <div class="field">
            <label for="size">Size</label>
            <input id="size" type="text" name="size" value="{{{{ item.size or '' }}}}">
          </div>
          <div class="field">
            <label for="color">Color</label>
            <input id="color" type="text" name="color" value="{{{{ item.color or '' }}}}">
          </div>
          <div class="field" style="grid-column:1/-1;">
            <label for="notes">Notes</label>
            <input id="notes" type="text" name="notes" value="{{{{ item.notes or '' }}}}">
          </div>
        </div>

        <button type="submit" class="btn btn-primary">Save changes</button>
      </form>
    </div>
    """
    template = BASE_HTML_TOP + inner + BASE_HTML_BOTTOM
    return render_template_string(
        template,
        item=item,
        categories=categories,
        locations=locations,
        active_page="items",
    )


@app.route("/items/delete/<int:item_id>")
def delete_item(item_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Item WHERE item_id = %s;", (item_id,))
    if not cur.fetchone():
        cur.close()
        flash("Item not found.")
        return redirect(url_for("list_items"))

    cur.execute("DELETE FROM Item WHERE item_id = %s;", (item_id,))
    conn.commit()
    cur.close()
    flash("Item deleted.")
    return redirect(url_for("list_items"))


# ====================================
# RUN
# ====================================
if __name__ == "__main__":
    app.run(port=8000, debug=True)
