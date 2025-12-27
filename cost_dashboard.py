import psycopg2
import json
from collections import defaultdict
from datetime import date

DB_CONFIG = {
    "host": "localhost",
    "database": "aws_cost_db",
    "user": "postgres",
    "password": "your_password",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def fetch_cost_dashboard():
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT
        r.service_type,
        r.subscription_id,
        r.resource_id,
        r.resource_name,
        c.usage_date,
        SUM(c.cost) as daily_cost
    FROM aws_resources r
    JOIN aws_costs c ON r.resource_id = c.resource_id
    GROUP BY
        r.service_type,
        r.subscription_id,
        r.resource_id,
        r.resource_name,
        c.usage_date
    ORDER BY c.usage_date;
    """

    cur.execute(query)
    rows = cur.fetchall()

    dashboard = defaultdict(lambda: {
        "total_cost": 0,
        "subscriptions": defaultdict(lambda: {
            "total_cost": 0,
            "resources": defaultdict(lambda: {
                "total_cost": 0,
                "daily_costs": []
            })
        })
    })

    for service, sub, rid, rname, usage_date, cost in rows:
        cost = float(cost)

        dashboard[service]["total_cost"] += cost
        dashboard[service]["subscriptions"][sub]["total_cost"] += cost

        resource = dashboard[service]["subscriptions"][sub]["resources"][rid]
        resource["total_cost"] += cost
        resource["daily_costs"].append({
            "date": usage_date.isoformat(),
            "cost": cost
        })
        resource["resource_name"] = rname

    cur.close()
    conn.close()

    return dashboard

def generate_json_file():
    data = fetch_cost_dashboard()
    with open("cost_dashboard.json", "w") as f:
        json.dump(data, f, indent=2)
    print("JSON file generated: cost_dashboard.json")

if __name__ == "__main__":
    generate_json_file()
