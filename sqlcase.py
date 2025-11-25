# =============================================================================
# WHOLEFOODS RETAIL - Simulation
# =============================================================================

import pandas as pd
import numpy as np
from faker import Faker
import sqlite3
import os
from tqdm import tqdm

np.random.seed(4552)
fake = Faker('en_US')

# -----------------------------
# SETTINGS
# -----------------------------
num_customers    = 840_000
num_transactions = 25_200_000
chunk_size       = 500_000
output_dir       = r"C:\The Shop\LearnSQL"
db_path          = os.path.join(output_dir, 'wholefoods_clean_final.sqlite')
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# 1. Load stores & products
# -----------------------------
print("Loading data...")
stores = pd.read_csv(r"C:\The Shop\LearnSQL\storemetadata.csv")
stores.columns = [c.strip().lower().replace(' ', '_') for c in stores.columns]
stores = stores[['store_id', 'store_name', 'city', 'state', 'address', 'phone', 'url']]

product_files = [
    r"C:\The Shop\LearnSQL\wine-beer-spirits\wine-beer-spirits.csv",
    r"C:\The Shop\LearnSQL\meat\meat.csv",
    r"C:\The Shop\LearnSQL\produce\produce.csv",
    r"C:\The Shop\LearnSQL\snacks-chips-salsas-dips\snacks-chips-salsas-dips.csv",
    r"C:\The Shop\LearnSQL\dairy-eggs\dairy-eggs.csv"
]

dfs = []
for f in product_files:
    df = pd.read_csv(f, low_memory=False)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    if 'regular_price' in df.columns:
        df.rename(columns={'regular_price': 'price'}, inplace=True)
    df = df[['store_id', 'category', 'product_name', 'price', 'slug']].dropna(subset=['slug'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    dfs.append(df.dropna(subset=['price']))

products_all = pd.concat(dfs, ignore_index=True)

# PRODUCTS: only identity
products = (
    products_all[['slug', 'product_name', 'category']]
    .drop_duplicates('slug')
    .reset_index(drop=True)
)

# INVENTORY: one row per product → comma-separated store_ids
inventory = (
    products_all.groupby('slug')['store_id']
    .apply(lambda x: ','.join(map(str, sorted(x.unique().astype(int)))))
    .reset_index()
    .rename(columns={'store_id': 'store_ids'})
    .merge(products[['slug', 'product_name', 'category']], on='slug')
)

# Fast lookups
store_to_products = {sid: g['slug'].values for sid, g in products_all.groupby('store_id')}
city_to_stores = stores.groupby('city')['store_id'].apply(list).to_dict()
all_store_ids = stores['store_id'].values

# -----------------------------
# 2. Customers
# -----------------------------
city_state = stores[['city', 'state']].drop_duplicates()
choices = np.random.choice(len(city_state), num_customers, replace=True)

customers = pd.DataFrame({
    'customer_id': range(1, num_customers + 1),
    'city'       : city_state['city'].values[choices],
    'state'      : city_state['state'].values[choices],
    'email'      : [fake.email() if np.random.rand() > 0.05 else None for _ in range(num_customers)],
    'phone'      : [fake.phone_number() if np.random.rand() > 0.1 else None for _ in range(num_customers)],
    'credit_card': [fake.credit_card_number() if np.random.rand() > 0.2 else None for _ in range(num_customers)],
})
customers['annual_txns'] = np.random.poisson(18, num_customers) + 3
customer_probs = customers['annual_txns'].values / customers['annual_txns'].sum()

# -----------------------------
# 3. Database
# -----------------------------
conn = sqlite3.connect(db_path)
conn.executescript("""
    PRAGMA journal_mode = OFF;
    PRAGMA synchronous = OFF;
    PRAGMA cache_size = -2000000;
    PRAGMA temp_store = MEMORY;
""")

customers.to_sql('customers', conn, if_exists='replace', index=False, chunksize=300_000)
stores.to_sql('stores', conn, if_exists='replace', index=False, chunksize=300_000)
products.to_sql('products', conn, if_exists='replace', index=False, chunksize=300_000)
inventory[['slug', 'store_ids', 'product_name', 'category']].to_sql('inventory', conn, if_exists='replace', index=False, chunksize=300_000)

# -----------------------------
# 4. Generate transactions & line items
# -----------------------------
print("Generating 4M transactions...")
month_weights = np.array([0.07,0.07,0.08,0.08,0.013,0.16,0.08,0.08,0.08,0.08,0.11,0.11])
month_weights /= month_weights.sum()
date_range = pd.date_range('2023-01-01', '2025-12-31', freq='D')
dates_by_month = {m: date_range[date_range.month == m].values for m in range(1,13)}

slug_to_base_price = products_all.groupby('slug')['price'].first().to_dict()

tx_id = 1
pbar = tqdm(total=num_transactions, desc="Tx", unit="M")

for start in range(0, num_transactions, chunk_size):
    sz = min(chunk_size, num_transactions - start)

    # Customers + dates
    cust_idx = np.random.choice(len(customers), sz, p=customer_probs)
    chosen = customers.iloc[cust_idx]
    months = np.random.choice(range(1,13), sz, p=month_weights)
    sale_dates = np.concatenate([np.random.choice(dates_by_month[m], (months==m).sum()) for m in range(1,13)])

    # 82% local shopping
    local = np.random.rand(sz) < 0.82
    store_ids = np.random.choice(all_store_ids, sz)
    if local.any():
        store_ids[local] = [np.random.choice(city_to_stores.get(c, all_store_ids)) for c in chosen.loc[local, 'city']]

    # Transactions
    tx_chunk = pd.DataFrame({
        'transaction_id': range(tx_id, tx_id + sz),
        'customer_id'   : chosen['customer_id'].values,
        'store_id'      : store_ids,
        'sale_date'     : sale_dates
    })
    tx_chunk.to_sql('transactions', conn, if_exists='append', index=False, chunksize=300_000)

    baskets = np.clip(np.random.poisson(2.4, sz) + 1, 1, 30)
    tx_rep = np.repeat(tx_chunk['transaction_id'].values, baskets)
    store_rep = np.repeat(store_ids, baskets)

    slugs = np.array([np.random.choice(store_to_products.get(s, next(iter(store_to_products.values())))) for s in store_rep])
    days = (pd.to_datetime(sale_dates) - pd.Timestamp('2023-01-01')).days
    days_exp = np.repeat(days, baskets)

    base_prices = np.array([slug_to_base_price.get(s, 10.0) for s in slugs])
    drift = np.random.uniform(-0.0005, 0.0005, len(slugs))
    actual_prices = base_prices * (1 + drift) ** days_exp
    quantities = np.random.poisson(1.3, len(slugs)) + 1

    li_chunk = pd.DataFrame({
        'transaction_id': tx_rep,
        'slug'          : slugs,
        'quantity'      : quantities,
        'price'         : actual_prices.round(2)
    })
    li_chunk.to_sql('line_items', conn, if_exists='append', index=False, chunksize=300_000)

    tx_id += sz
    pbar.update(sz)

pbar.close()
conn.close()
