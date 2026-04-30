"""
Query helper functions for the Spendly application.

All functions use raw sqlite3 via get_db() and close connections before returning.
No Flask imports - pure database query helpers only.
"""

import sqlite3
from database.db import get_db


def get_user_by_id(user_id):
    """
    Fetches a user record by ID with formatted member_since date.

    Args:
        user_id: User's ID

    Returns:
        dict with name, email, member_since (formatted as "Month YYYY") or None if not found
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, email,
               strftime('%m %Y', created_at) as created_at_month,
               strftime('%Y-%m-%d', created_at) as created_at_date
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    # Format month name from month number
    month_names = {
        '01': 'January', '02': 'February', '03': 'March', '04': 'April',
        '05': 'May', '06': 'June', '07': 'July', '08': 'August',
        '09': 'September', '10': 'October', '11': 'November', '12': 'December'
    }
    month_year = row['created_at_month']
    if month_year:
        month, year = month_year.split()
        member_since = f"{month_names.get(month, month)} {year}"
    else:
        member_since = "Unknown"

    return {
        'id': row['id'],
        'name': row['name'],
        'email': row['email'],
        'member_since': member_since
    }


def get_summary_stats(user_id):
    """
    Fetches summary statistics for a user's expenses.

    Args:
        user_id: User's ID

    Returns:
        dict with total_spent, transaction_count, top_category
        Returns zeros if user has no expenses
    """
    conn = get_db()
    cursor = conn.cursor()

    # Get total spent and transaction count
    cursor.execute(
        """
        SELECT
            COALESCE(SUM(amount), 0) as total_spent,
            COUNT(*) as transaction_count
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id,)
    )
    result = cursor.fetchone()
    total_spent = result['total_spent']
    transaction_count = result['transaction_count']

    # Get top category
    cursor.execute(
        """
        SELECT category
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
        """,
        (user_id,)
    )
    top_result = cursor.fetchone()
    top_category = top_result['category'] if top_result else "—"

    conn.close()

    return {
        'total_spent': total_spent,
        'transaction_count': transaction_count,
        'top_category': top_category
    }


def get_recent_transactions(user_id, limit=10):
    """
    Fetches recent transactions for a user.

    Args:
        user_id: User's ID
        limit: Maximum number of transactions to return (default 10)

    Returns:
        list of dicts with date, description, category, amount
        Ordered newest-first
        Returns empty list if user has no expenses
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT date, description, category, amount
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()

    transactions = []
    for row in rows:
        transactions.append({
            'date': row['date'],
            'description': row['description'],
            'category': row['category'],
            'amount': row['amount']
        })

    return transactions


def get_category_breakdown(user_id):
    """
    Fetches category breakdown for a user's expenses.

    Args:
        user_id: User's ID

    Returns:
        list of dicts with name, amount, pct (percentage)
        Ordered by amount descending
        pct values are integers summing to 100
        Returns empty list if user has no expenses
    """
    conn = get_db()
    cursor = conn.cursor()

    # First get total amount
    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0) as total
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id,)
    )
    total = cursor.fetchone()['total']
    conn.close()

    if total == 0:
        return []

    # Get category totals
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT category as name, SUM(amount) as amount
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY amount DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    categories = []
    percentages = []
    running_total = 0

    for row in rows:
        # Calculate raw percentage
        raw_pct = (row['amount'] / total) * 100
        rounded_pct = round(raw_pct)
        percentages.append(rounded_pct)
        running_total += rounded_pct

        categories.append({
            'name': row['name'],
            'amount': row['amount'],
            'pct': rounded_pct
        })

    # Adjust for rounding errors - add/subtract difference from largest category
    if categories and running_total != 100:
        diff = 100 - running_total
        categories[0]['pct'] += diff

    return categories
