aws_resources(
  resource_id VARCHAR PRIMARY KEY,
  resource_name TEXT,
  service_type TEXT,
  subscription_id TEXT
);

aws_costs(
  id SERIAL PRIMARY KEY,
  resource_id VARCHAR,
  cost NUMERIC,
  usage_date DATE
);

top_cost_resources(
  resource_id VARCHAR,
  total_cost NUMERIC
);
