import psycopg2
import json
from collections import defaultdict
from datetime import datetime

# 🔧 CHANGE THESE
DB_CONFIG = {
    "host": "localhost",
    "database": "aws_cost_db",
    "user": "postgres",
    "password": "12345",
    "port": 5432
}

SUBMITTED_BY = "muhammadsafwancs@mulearn"   # 🔴 REQUIRED TAG

def fetch_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """
    SELECT
        r.service,
        r.subscription,
        c.usage_date,
        SUM(c.cost) AS total_cost
    FROM aws_resources r
    JOIN aws_costs c
        ON r.resource_id = c.resource_id
    GROUP BY r.service, r.subscription, c.usage_date
    ORDER BY r.service, c.usage_date;
    """

    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def build_json(rows):
    services = defaultdict(lambda: {
        "total_cost": 0,
        "subscriptions": defaultdict(lambda: {
            "total_cost": 0,
            "daily_costs": {}
        })
    })

    for service, subscription, date, cost in rows:
        date_str = date.strftime("%Y-%m-%d")

        services[service]["total_cost"] += float(cost)
        services[service]["subscriptions"][subscription]["total_cost"] += float(cost)
        services[service]["subscriptions"][subscription]["daily_costs"][date_str] = float(cost)

    return services

def main():
    rows = fetch_data()
    services_data = build_json(rows)

    output = {
        "submitted_by": SUBMITTED_BY,
        "generated_at": datetime.utcnow().isoformat(),
        "currency": "USD",
        "grouped_by": "service",
        "services": services_data
    }

    with open("cost_dashboard.json", "w") as f:
        json.dump(output, f, indent=4)

    print("✅ cost_dashboard.json generated successfully")

if __name__ == "__main__":
    main()
