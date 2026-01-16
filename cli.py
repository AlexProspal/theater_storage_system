import psycopg2
import psycopg2.extras
from datetime import datetime

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


# ====================================
# DB CONNECTION HELPERS
# ====================================
def get_db():
    return psycopg2.connect(**DB_CONFIG)


def fetch_all(query, params=None):
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, params or [])
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        conn.close()


def execute(query, params=None, return_rowcount=False):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(query, params or [])
        rowcount = cur.rowcount
        conn.commit()
        cur.close()
        if return_rowcount:
            return rowcount
    finally:
        conn.close()


# ====================================
# CLI HELPERS
# ====================================
def prompt(msg, required=False, allow_blank_as_none=False):
    while True:
        val = input(msg).strip()
        if val == "" and allow_blank_as_none:
            return None
        if required and not val:
            print("  -> This field is required.")
            continue
        return val


def prompt_int(msg, required=False, allow_blank_as_none=False):
    while True:
        val = input(msg).strip()
        if val == "" and allow_blank_as_none:
            return None
        if not val:
            if required:
                print("  -> This field is required.")
                continue
            else:
                return None
        try:
            return int(val)
        except ValueError:
            print("  -> Please enter an integer.")


def choose_from_list(rows, display_fn, allow_none=False, prompt_text="Choose an option"):
    """
    rows: list of dict-like rows
    display_fn: function(row) -> string
    Returns the selected row (dict) or None.
    """
    if not rows:
        print("  (No options.)")
        return None

    while True:
        print()
        for idx, row in enumerate(rows, start=1):
            print(f"  {idx}. {display_fn(row)}")
        if allow_none:
            print("  0. None")
        choice = input(f"{prompt_text} (#): ").strip()
        if allow_none and choice == "0":
            return None
        try:
            idx = int(choice)
            if 1 <= idx <= len(rows):
                return rows[idx - 1]
        except ValueError:
            pass
        print("  -> Invalid choice, try again.")


def press_enter():
    input("\nPress Enter to continue...")


# ====================================
# MEMBERS
# ====================================
def list_members():
    rows = fetch_all(
        "SELECT member_id, name, email, phone, role FROM Member ORDER BY name;"
    )
    if not rows:
        print("\n(No members)")
        return

    print("\nMembers:")
    print("-" * 60)
    for r in rows:
        print(
            f"[{r['member_id']}] {r['name']} "
            f"(role: {r['role'] or 'N/A'}, "
            f"email: {r['email'] or 'N/A'}, phone: {r['phone'] or 'N/A'})"
        )


def add_member():
    print("\nAdd Member")
    print("==========")
    name = prompt("Name *: ", required=True)
    role = prompt("Role (optional): ", allow_blank_as_none=True)
    email = prompt("Email (optional): ", allow_blank_as_none=True)
    phone = prompt("Phone (optional): ", allow_blank_as_none=True)

    execute(
        """
        INSERT INTO Member (name, role, email, phone)
        VALUES (%s, %s, %s, %s);
        """,
        (name, role, email, phone),
    )
    print("-> Member added.")


def member_detail():
    mid = prompt_int("\nEnter member_id to view: ", required=True)
    rows = fetch_all(
        "SELECT member_id, name, email, phone, role FROM Member WHERE member_id = %s;",
        (mid,),
    )
    if not rows:
        print("-> Member not found.")
        return
    m = rows[0]
    print("\nMember Detail")
    print("=============")
    print(f"Name : {m['name']}")
    print(f"Role : {m['role'] or 'N/A'}")
    print(f"Email: {m['email'] or 'N/A'}")
    print(f"Phone: {m['phone'] or 'N/A'}")

    # Show checkouts (current & past, like web app)
    items = fetch_all(
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
        (mid,),
    )
    print("\nCheckouts for this member:")
    print("---------------------------")
    if not items:
        print("(No checkouts)")
    else:
        for row in items:
            d = row["checkout_date"].strftime("%Y-%m-%d")
            print(
                f"- {row['tag_code']} | {row['name']} | "
                f"Production: {row['production_title'] or 'N/A'} | "
                f"Date: {d} | Notes: {row['notes'] or ''}"
            )


# ====================================
# PRODUCTIONS
# ====================================
def list_productions():
    rows = fetch_all(
        """
        SELECT production_id, title, season, open_date, close_date
        FROM Production
        ORDER BY title;
        """
    )
    if not rows:
        print("\n(No productions)")
        return

    print("\nProductions:")
    print("-" * 60)
    for p in rows:
        open_s = p["open_date"].strftime("%Y-%m-%d") if p["open_date"] else "N/A"
        close_s = p["close_date"].strftime("%Y-%m-%d") if p["close_date"] else "N/A"
        print(
            f"[{p['production_id']}] {p['title']} "
            f"(season: {p['season'] or 'N/A'}, run: {open_s} – {close_s})"
        )


def add_production():
    print("\nAdd Production")
    print("==============")
    title = prompt("Title *: ", required=True)
    season = prompt("Season (optional): ", allow_blank_as_none=True)
    open_date = prompt("Open date (YYYY-MM-DD, optional): ", allow_blank_as_none=True)
    close_date = prompt("Close date (YYYY-MM-DD, optional): ", allow_blank_as_none=True)

    execute(
        """
        INSERT INTO Production (title, season, open_date, close_date)
        VALUES (%s, %s, %s, %s);
        """,
        (title, season, open_date, close_date),
    )
    print("-> Production added.")


def production_detail():
    pid = prompt_int("\nEnter production_id to view: ", required=True)
    rows = fetch_all(
        """
        SELECT production_id, title, season, open_date, close_date
        FROM Production
        WHERE production_id = %s;
        """,
        (pid,),
    )
    if not rows:
        print("-> Production not found.")
        return
    p = rows[0]
    print("\nProduction Detail")
    print("=================")
    print(f"Title : {p['title']}")
    print(f"Season: {p['season'] or 'N/A'}")
    open_s = p["open_date"].strftime("%Y-%m-%d") if p["open_date"] else "N/A"
    close_s = p["close_date"].strftime("%Y-%m-%d") if p["close_date"] else "N/A"
    print(f"Run   : {open_s} – {close_s}")

    # Items checked out for this production
    items = fetch_all(
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
        (pid,),
    )
    print("\nCheckouts for this production:")
    print("------------------------------")
    if not items:
        print("(No checkouts)")
    else:
        for row in items:
            d = row["checkout_date"].strftime("%Y-%m-%d")
            print(
                f"- {row['tag_code']} | {row['name']} | "
                f"Member: {row['member_name'] or 'N/A'} | "
                f"Date: {d} | Notes: {row['notes'] or ''}"
            )


# ====================================
# CATEGORIES
# ====================================
def list_categories():
    rows = fetch_all(
        "SELECT category_id, name, description FROM Category ORDER BY name;"
    )
    if not rows:
        print("\n(No categories)")
        return

    print("\nCategories:")
    print("-" * 60)
    for c in rows:
        print(
            f"[{c['category_id']}] {c['name']} - {c['description'] or '(no description)'}"
        )


def add_category():
    print("\nAdd Category")
    print("============")
    name = prompt("Name *: ", required=True)
    desc = prompt("Description (optional): ", allow_blank_as_none=True)
    execute(
        """
        INSERT INTO Category (name, description)
        VALUES (%s, %s);
        """,
        (name, desc),
    )
    print("-> Category added.")


def category_detail():
    cid = prompt_int("\nEnter category_id to view items: ", required=True)
    rows = fetch_all(
        "SELECT category_id, name, description FROM Category WHERE category_id = %s;",
        (cid,),
    )
    if not rows:
        print("-> Category not found.")
        return
    c = rows[0]
    print("\nCategory Detail")
    print("===============")
    print(f"Name       : {c['name']}")
    print(f"Description: {c['description'] or 'No description yet.'}")

    search = prompt("Search items (blank for no filter): ", allow_blank_as_none=True)
    where_extra = ""
    params = [cid]
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

    items = fetch_all(
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
        """
        + where_extra
        + """
        ORDER BY i.tag_code;
        """,
        params,
    )

    print("\nItems in this category:")
    print("-----------------------")
    if not items:
        print("(No items in this category)")
        return

    for row in items:
        status = "Checked out" if row["is_out"] else "In stock"
        print(
            f"- [{row['item_id']}] {row['tag_code']} | {row['name']} | "
            f"Location: {row['location_code'] or ''} | "
            f"Size: {row['size'] or ''} | Color: {row['color'] or ''} | "
            f"Notes: {row['notes'] or ''} | Status: {status}"
        )


# ====================================
# STORAGE LOCATIONS
# ====================================
def list_locations():
    rows = fetch_all(
        "SELECT location_id, code, description FROM StorageLocation ORDER BY code;"
    )
    if not rows:
        print("\n(No storage locations)")
        return

    print("\nStorage Locations:")
    print("-" * 60)
    for l in rows:
        print(
            f"[{l['location_id']}] {l['code']} - {l['description'] or '(no description)'}"
        )


def add_location():
    print("\nAdd Storage Location")
    print("====================")
    code = prompt("Code *: ", required=True)
    desc = prompt("Description (optional): ", allow_blank_as_none=True)
    execute(
        """
        INSERT INTO StorageLocation (code, description)
        VALUES (%s, %s);
        """,
        (code, desc),
    )
    print("-> Location added.")


def location_detail():
    lid = prompt_int("\nEnter location_id to view items: ", required=True)
    rows = fetch_all(
        "SELECT location_id, code, description FROM StorageLocation WHERE location_id = %s;",
        (lid,),
    )
    if not rows:
        print("-> Storage location not found.")
        return
    loc = rows[0]
    print("\nStorage Location Detail")
    print("=======================")
    print(f"Code       : {loc['code']}")
    print(f"Description: {loc['description'] or 'No description yet.'}")

    search = prompt("Search items (blank for no filter): ", allow_blank_as_none=True)
    where_extra = ""
    params = [lid]
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

    items = fetch_all(
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
        """
        + where_extra
        + """
        ORDER BY i.tag_code;
        """,
        params,
    )

    print("\nItems stored here:")
    print("------------------")
    if not items:
        print("(No items stored here)")
        return

    for row in items:
        status = "Checked out" if row["is_out"] else "In stock"
        print(
            f"- [{row['item_id']}] {row['tag_code']} | {row['name']} | "
            f"Category: {row['category_name'] or ''} | "
            f"Size: {row['size'] or ''} | Color: {row['color'] or ''} | "
            f"Notes: {row['notes'] or ''} | Status: {status}"
        )


# ====================================
# ITEMS
# ====================================
def list_items():
    print("\nList Items (optional search)")
    search = prompt("Search (blank for all): ", allow_blank_as_none=True)

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

    rows = fetch_all(base_query.format(where_clause=where_clause), params)
    if not rows:
        print("\n(No items)")
        return

    print("\nItems:")
    print("-" * 80)
    for r in rows:
        status = "Checked out" if r["is_out"] else "In stock"
        print(
            f"[{r['item_id']}] {r['tag_code']} | {r['name']} | "
            f"Cat: {r['category_name'] or ''} | Loc: {r['location_code'] or ''} | "
            f"Size: {r['size'] or ''} | Color: {r['color'] or ''} | "
            f"Notes: {r['notes'] or ''} | Status: {status}"
        )


def add_item():
    print("\nAdd Item")
    print("========")

    # List categories/locations to help user choose
    categories = fetch_all("SELECT category_id, name FROM Category ORDER BY name;")
    locations = fetch_all("SELECT location_id, code FROM StorageLocation ORDER BY code;")

    tag_code = prompt("Tag code *: ", required=True)
    name = prompt("Name *: ", required=True)

    print("\nSelect category (or leave blank to skip):")
    cat_row = choose_from_list(
        categories,
        lambda c: f"{c['category_id']}: {c['name']}",
        allow_none=True,
        prompt_text="Category",
    )
    category_id = cat_row["category_id"] if cat_row else None

    print("\nSelect location (or leave blank to skip):")
    loc_row = choose_from_list(
        locations,
        lambda l: f"{l['location_id']}: {l['code']}",
        allow_none=True,
        prompt_text="Location",
    )
    location_id = loc_row["location_id"] if loc_row else None

    size = prompt("Size (optional): ", allow_blank_as_none=True)
    color = prompt("Color (optional): ", allow_blank_as_none=True)
    notes = prompt("Notes (optional): ", allow_blank_as_none=True)

    execute(
        """
        INSERT INTO Item
          (tag_code, name, category_id, size, color, notes, location_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
        (tag_code, name, category_id, size, color, notes, location_id),
    )
    print("-> Item added.")


def edit_item():
    item_id = prompt_int("\nEnter item_id to edit: ", required=True)
    rows = fetch_all(
        """
        SELECT item_id, tag_code, name, category_id, size, color, notes, location_id
        FROM Item
        WHERE item_id = %s;
        """,
        (item_id,),
    )
    if not rows:
        print("-> Item not found.")
        return
    item = rows[0]
    categories = fetch_all("SELECT category_id, name FROM Category ORDER BY name;")
    locations = fetch_all("SELECT location_id, code FROM StorageLocation ORDER BY code;")

    print("\nEdit Item (press Enter to keep current value)")
    print("---------------------------------------------")
    print(f"Current tag_code: {item['tag_code']}")
    tag_code = prompt("New tag_code: ", allow_blank_as_none=True) or item["tag_code"]

    print(f"Current name: {item['name']}")
    name = prompt("New name: ", allow_blank_as_none=True) or item["name"]

    print("\nSelect category (or 0 to keep current / none):")
    cat_row = choose_from_list(
        categories,
        lambda c: f"{c['category_id']}: {c['name']}",
        allow_none=True,
        prompt_text="Category",
    )
    if cat_row is None:
        category_id = item["category_id"]
    else:
        category_id = cat_row["category_id"]

    print("\nSelect location (or 0 to keep current / none):")
    loc_row = choose_from_list(
        locations,
        lambda l: f"{l['location_id']}: {l['code']}",
        allow_none=True,
        prompt_text="Location",
    )
    if loc_row is None:
        location_id = item["location_id"]
    else:
        location_id = loc_row["location_id"]

    print(f"Current size: {item['size'] or ''}")
    size = prompt("New size: ", allow_blank_as_none=True)
    if size is None:
        size = item["size"]

    print(f"Current color: {item['color'] or ''}")
    color = prompt("New color: ", allow_blank_as_none=True)
    if color is None:
        color = item["color"]

    print(f"Current notes: {item['notes'] or ''}")
    notes = prompt("New notes: ", allow_blank_as_none=True)
    if notes is None:
        notes = item["notes"]

    execute(
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
        (tag_code, name, category_id, size, color, notes, location_id, item_id),
    )
    print("-> Item updated.")


def delete_item():
    item_id = prompt_int("\nEnter item_id to delete: ", required=True)
    # Quick existence check
    count = fetch_all(
        "SELECT COUNT(*) AS c FROM Item WHERE item_id = %s;", (item_id,)
    )[0]["c"]
    if count == 0:
        print("-> Item not found.")
        return

    confirm = input("Are you sure you want to delete this item? (y/N): ").strip().lower()
    if confirm != "y":
        print("-> Cancelled.")
        return

    execute("DELETE FROM Item WHERE item_id = %s;", (item_id,))
    print("-> Item deleted.")


# ====================================
# CHECKOUTS
# ====================================
def list_checkouts():
    rows = fetch_all(
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
    if not rows:
        print("\n(No checkouts)")
        return

    print("\nCheckouts:")
    print("-" * 80)
    for r in rows:
        d = r["checkout_date"].strftime("%Y-%m-%d")
        print(
            f"[{r['checkout_id']}] {r['tag_code']} | {r['item_name']} | "
            f"Member: {r['member_name'] or ''} | "
            f"Prod: {r['production_title'] or ''} | "
            f"Date: {d} | Notes: {r['notes'] or ''}"
        )


def new_checkout():
    print("\nNew Checkout")
    print("============")

    # Items NOT currently checked out
    items = fetch_all(
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
    if not items:
        print("-> No items available for checkout.")
        return

    members = fetch_all("SELECT member_id, name FROM Member ORDER BY name;")
    prods = fetch_all("SELECT production_id, title FROM Production ORDER BY title;")

    print("\nChoose item to checkout:")
    item_row = choose_from_list(
        items,
        lambda i: f"{i['item_id']} | {i['tag_code']} — {i['name']}",
        allow_none=False,
        prompt_text="Item",
    )
    item_id = item_row["item_id"]

    print("\nChoose member (or 0 for none):")
    member_row = choose_from_list(
        members,
        lambda m: f"{m['member_id']} | {m['name']}",
        allow_none=True,
        prompt_text="Member",
    )
    member_id = member_row["member_id"] if member_row else None

    print("\nChoose production (or 0 for none):")
    prod_row = choose_from_list(
        prods,
        lambda p: f"{p['production_id']} | {p['title']}",
        allow_none=True,
        prompt_text="Production",
    )
    prod_id = prod_row["production_id"] if prod_row else None

    notes = prompt("Notes (optional): ", allow_blank_as_none=True)

    execute(
        """
        INSERT INTO Checkout (item_id, member_id, production_id, notes)
        VALUES (%s, %s, %s, %s);
        """,
        (item_id, member_id, prod_id, notes),
    )
    print("-> Item checked out.")


def return_checkout():
    list_checkouts()
    cid = prompt_int("\nEnter checkout_id to mark returned: ", required=True)
    rowcount = execute(
        "DELETE FROM Checkout WHERE checkout_id = %s;",
        (cid,),
        return_rowcount=True,
    )
    if rowcount == 0:
        print("-> Checkout not found.")
    else:
        print("-> Item returned (checkout deleted).")


# ====================================
# MAIN MENU
# ====================================
def main_menu():
    while True:
        print("\n==============================")
        print(" Theater Inventory (CLI)")
        print("==============================")
        print("1. Members")
        print("2. Productions")
        print("3. Categories")
        print("4. Storage Locations")
        print("5. Items")
        print("6. Checkouts")
        print("Q. Quit")

        choice = input("Choose an option: ").strip().lower()
        if choice == "1":
            members_menu()
        elif choice == "2":
            productions_menu()
        elif choice == "3":
            categories_menu()
        elif choice == "4":
            locations_menu()
        elif choice == "5":
            items_menu()
        elif choice == "6":
            checkouts_menu()
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("-> Invalid choice.")


def members_menu():
    while True:
        print("\nMembers Menu")
        print("------------")
        print("1. List members")
        print("2. Add member")
        print("3. View member detail & checkouts")
        print("B. Back")
        choice = input("Choose: ").strip().lower()
        if choice == "1":
            list_members()
            press_enter()
        elif choice == "2":
            add_member()
            press_enter()
        elif choice == "3":
            member_detail()
            press_enter()
        elif choice == "b":
            break
        else:
            print("-> Invalid choice.")


def productions_menu():
    while True:
        print("\nProductions Menu")
        print("----------------")
        print("1. List productions")
        print("2. Add production")
        print("3. View production detail & checkouts")
        print("B. Back")
        choice = input("Choose: ").strip().lower()
        if choice == "1":
            list_productions()
            press_enter()
        elif choice == "2":
            add_production()
            press_enter()
        elif choice == "3":
            production_detail()
            press_enter()
        elif choice == "b":
            break
        else:
            print("-> Invalid choice.")


def categories_menu():
    while True:
        print("\nCategories Menu")
        print("---------------")
        print("1. List categories")
        print("2. Add category")
        print("3. View category items (with optional search)")
        print("B. Back")
        choice = input("Choose: ").strip().lower()
        if choice == "1":
            list_categories()
            press_enter()
        elif choice == "2":
            add_category()
            press_enter()
        elif choice == "3":
            category_detail()
            press_enter()
        elif choice == "b":
            break
        else:
            print("-> Invalid choice.")


def locations_menu():
    while True:
        print("\nStorage Locations Menu")
        print("----------------------")
        print("1. List locations")
        print("2. Add location")
        print("3. View location items (with optional search)")
        print("B. Back")
        choice = input("Choose: ").strip().lower()
        if choice == "1":
            list_locations()
            press_enter()
        elif choice == "2":
            add_location()
            press_enter()
        elif choice == "3":
            location_detail()
            press_enter()
        elif choice == "b":
            break
        else:
            print("-> Invalid choice.")


def items_menu():
    while True:
        print("\nItems Menu")
        print("----------")
        print("1. List/search items")
        print("2. Add item")
        print("3. Edit item")
        print("4. Delete item")
        print("B. Back")
        choice = input("Choose: ").strip().lower()
        if choice == "1":
            list_items()
            press_enter()
        elif choice == "2":
            add_item()
            press_enter()
        elif choice == "3":
            edit_item()
            press_enter()
        elif choice == "4":
            delete_item()
            press_enter()
        elif choice == "b":
            break
        else:
            print("-> Invalid choice.")


def checkouts_menu():
    while True:
        print("\nCheckouts Menu")
        print("--------------")
        print("1. List checkouts")
        print("2. New checkout")
        print("3. Mark returned")
        print("B. Back")
        choice = input("Choose: ").strip().lower()
        if choice == "1":
            list_checkouts()
            press_enter()
        elif choice == "2":
            new_checkout()
            press_enter()
        elif choice == "3":
            return_checkout()
            press_enter()
        elif choice == "b":
            break
        else:
            print("-> Invalid choice.")


# ====================================
# ENTRY POINT
# ====================================
if __name__ == "__main__":
    main_menu()
