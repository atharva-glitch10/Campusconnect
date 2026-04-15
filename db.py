import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Aarnav@2506",
    "database": "interest_matching"
}


def get_connection():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


# ── User operations ──────────────────────────────────────────

def add_user(name: str):
    """Insert a new user. Returns a status dict."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()
        return {"status": f"User '{name}' added successfully"}
    except mysql.connector.IntegrityError:
        return {"status": "User already exists"}
    finally:
        cursor.close()
        conn.close()


def get_all_users():
    """Return a list of all user names."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users ORDER BY name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]


# ── Interest operations ──────────────────────────────────────

def add_interest(user: str, interest: str):
    """Assign an interest to a user. Creates the interest if it doesn't exist."""
    interest = interest.lower().strip()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get user_id
        cursor.execute("SELECT user_id FROM users WHERE name = %s", (user,))
        row = cursor.fetchone()
        if not row:
            return {"status": f"User '{user}' not found. Create the user first."}
        user_id = row[0]

        # Get or create interest
        cursor.execute("SELECT interest_id FROM interests WHERE name = %s", (interest,))
        row = cursor.fetchone()
        if row:
            interest_id = row[0]
        else:
            cursor.execute("INSERT INTO interests (name) VALUES (%s)", (interest,))
            interest_id = cursor.lastrowid

        # Link user ↔ interest
        cursor.execute(
            "INSERT INTO user_interests (user_id, interest_id) VALUES (%s, %s)",
            (user_id, interest_id)
        )
        conn.commit()
        return {"status": f"Interest '{interest}' added for {user}"}
    except mysql.connector.IntegrityError:
        return {"status": f"{user} already has interest '{interest}'"}
    finally:
        cursor.close()
        conn.close()


# ── Fetch data for matching ──────────────────────────────────

def get_users_with_interests():
    """
    Return a dict:  { username: [interest1, interest2, ...], ... }
    Used by the matching algorithm.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.name, i.name
        FROM users u
        LEFT JOIN user_interests ui ON u.user_id = ui.user_id
        LEFT JOIN interests i      ON ui.interest_id = i.interest_id
        ORDER BY u.name
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data: dict[str, list[str]] = {}
    for user_name, interest_name in rows:
        data.setdefault(user_name, [])
        if interest_name:
            data[user_name].append(interest_name)
    return data


def get_user_interests(user: str):
    """Return a list of interests for a single user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.name
        FROM interests i
        JOIN user_interests ui ON i.interest_id = ui.interest_id
        JOIN users u           ON u.user_id     = ui.user_id
        WHERE u.name = %s
        ORDER BY i.name
    """, (user,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]