# =============================================================================
# WHOLEFOODS RETAIL SIMULATION – ULTRA-FAST & PYCHARM-FRIENDLY (15–22 min)
# =============================================================================

import os
import sqlite3
import numpy as np
import pandas as pd
from faker import Faker
from tqdm import tqdm
from numba import njit, prange

# -----------------------------
# SETTINGS
# -----------------------------
np.random.seed(4552)
fake = Faker('en_US')

num_customers    = 840_000
num_transactions = 25_200_000
chunk_size       = 500_000
output_dir       = r"C:\The Shop\LearnSQL"
db_path          = os.path.join(output_dir, "wholefoods_clean_final.sqlite")
os.makedirs(output_dir, exist_ok=True)

product_files = [
    r"C:\The Shop\LearnSQL\wine-beer-spirits\wine-beer-spirits.csv",
    r"C:\The Shop\LearnSQL\meat\meat.csv",
    r"C:\The Shop\LearnSQL\produce\produce.csv",
    r"C:\The Shop\LearnSQL\snacks-chips-salsas-dips\snacks-chips-salsas-dips.csv",
    r"C:\The Shop\LearnSQL\dairy-eggs\dairy-eggs.csv"
]
store_metadata_path = r"C:\The Shop\LearnSQL\storemetadata.csv"

k_factors = 5
m_store_prod = 3
price_noise_sigma = 0.02
mu_noise_sigma = 0.25

# -----------------------------
# 1. Load stores & products
# -----------------------------
print("Loading stores & products...")
stores = pd.read_csv(store_metadata_path)
stores.columns = [c.strip().lower().replace(' ', '_') for c in stores.columns]
stores = stores[['store_id', 'store_name', 'city', 'state', 'address', 'phone', 'url']]

dfs = []
for f in product_files:
    df = pd.read_csv(f, low_memory=False)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    if 'regular_price' in df.columns:
        df.rename(columns={'regular_price': 'price'}, inplace=True)
    want = [c for c in ['store_id', 'category', 'product_name', 'price', 'slug'] if c in df.columns]
    df = df[want].dropna(subset=['slug'])
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    dfs.append(df.dropna(subset=['price']) if 'price' in df.columns else df)

products_all = pd.concat(dfs, ignore_index=True)
products = products_all[['slug', 'product_name', 'category']].drop_duplicates('slug').reset_index(drop=True)

# FAST store → product index mapping (this was the killer before)
print("Building fast store to product index mapping...")
slug_to_idx = pd.Series(np.arange(len(products)), index=products['slug'])

store_product_df = (
    products_all[['store_id', 'slug']]
    .merge(slug_to_idx.rename('product_idx'), left_on='slug', right_index=True, how='inner')
)

store_to_products = {
    sid: group['product_idx'].values.astype(np.int32)
    for sid, group in store_product_df.groupby('store_id', sort=False)
}

valid_store_ids = np.sort(np.fromiter(store_to_products.keys(), dtype=np.int64))
store_to_idx = {sid: i for i, sid in enumerate(valid_store_ids)}
num_stores = len(valid_store_ids)

city_to_stores = stores.groupby('city')['store_id'].apply(list).to_dict()

# -----------------------------
# 2. Customers
# -----------------------------
print("Generating customers...")
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

beta_i = np.random.normal(0.0, 0.7, size=num_customers).astype(np.float64)
eta_i  = np.random.normal(0.0, 0.25, size=(num_customers, k_factors)).astype(np.float64)

# -----------------------------
# 3. Factor model & time setup
# -----------------------------
print("Preparing factor model...")
unique_slugs = products['slug'].values
slug_to_idx_dict = {s: i for i, s in enumerate(unique_slugs)}
idx_to_slug_array = unique_slugs                      # direct array lookup – no dict!

num_slugs = len(unique_slugs)

# Base prices
slug_base_price = np.zeros(num_slugs, dtype=np.float64)
prices_by_slug = products_all.groupby('slug')['price'].first()
for slug, price in prices_by_slug.items():
    if slug in slug_to_idx_dict:
        slug_base_price[slug_to_idx_dict[slug]] = price

nonzero = slug_base_price[slug_base_price > 0]
median_price = np.median(nonzero) if len(nonzero) > 0 else 5.0
slug_base_price[slug_base_price == 0] = median_price

alpha_p     = np.random.normal(0.0, 0.6, size=num_slugs).astype(np.float64)
Lambda_p    = np.random.normal(0.0, 0.5, size=(num_slugs, k_factors)).astype(np.float64)
kappa_p     = np.random.normal(0.0, 0.08, size=(num_slugs, k_factors)).astype(np.float64)
store_embed = np.random.normal(0.0, 1.0, size=(num_stores, m_store_prod)).astype(np.float64)
prod_embed  = np.random.normal(0.0, 1.0, size=(num_slugs, m_store_prod)).astype(np.float64)

# Time matrix
all_dates = pd.date_range('2023-01-01', '2025-12-31', freq='D')
date_to_row = {d.date(): i for i, d in enumerate(all_dates)}

F_mat = np.column_stack([
    np.arange(len(all_dates)) / len(all_dates),
    np.sin(2 * np.pi * np.arange(len(all_dates)) / 365.25),
    np.cos(2 * np.pi * np.arange(len(all_dates)) / 365.25),
    np.sin(2 * np.pi * np.arange(len(all_dates)) / 7.0),
    np.cos(2 * np.pi * np.arange(len(all_dates)) / 30.44)
]).astype(np.float64)

dates_by_month = {m: all_dates[all_dates.month == m].values for m in range(1, 13)}

# -----------------------------
# 4. Flattened store to product arrays for Numba
# -----------------------------
flat_slug_idxs = np.concatenate([store_to_products[sid] for sid in valid_store_ids], dtype=np.int32)
store_offsets = np.zeros(num_stores + 1, dtype=np.int64)
store_offsets[1:] = np.cumsum([len(store_to_products[sid]) for sid in valid_store_ids])

# -----------------------------
# 5. DB setup
# -----------------------------
print("Initializing SQLite database...")
conn = sqlite3.connect(db_path)
conn.executescript("""
    PRAGMA journal_mode = WAL;
    PRAGMA synchronous = NORMAL;
    PRAGMA cache_size = -64000;
    PRAGMA temp_store = MEMORY;
""")

# These three tables are small → safe without method='multi'
customers.to_sql('customers',   conn, if_exists='replace', index=False, chunksize=100_000)
stores.to_sql(   'stores',      conn, if_exists='replace', index=False, chunksize=100_000)
products.to_sql( 'products',    conn, if_exists='replace', index=False, chunksize=100_000)

# -----------------------------
# 6. Numba kernel
# -----------------------------
@njit(parallel=True)
def simulate_line_items(tx_ids, cust_ids, store_idxs, day_idxs,
                        alpha_p, beta_i, Lambda_p, eta_i,
                        store_embed, prod_embed,
                        slug_base_price, kappa_p,
                        mu_noise_sigma, price_noise_sigma,
                        F_mat,
                        flat_slug_idxs, store_offsets):
    n = len(tx_ids)
    slug_out  = np.empty(n, dtype=np.int32)
    qty_out   = np.empty(n, dtype=np.int32)
    price_out = np.empty(n, dtype=np.float32)

    for i in prange(n):
        sidx = store_idxs[i]
        cust = cust_ids[i]
        day  = day_idxs[i]
        f_t  = F_mat[day]

        start = store_offsets[sidx]
        end   = store_offsets[sidx + 1]
        candidates = flat_slug_idxs[start:end]

        if candidates.size == 0:
            candidates = np.array([0], dtype=np.int32)

        scores = (alpha_p[candidates] +
                  np.dot(Lambda_p[candidates], f_t) +
                  np.dot(store_embed[sidx], prod_embed[candidates].T))
        scores -= scores.max()
        probs = np.exp(scores)
        probs /= probs.sum()

        r = np.random.random()
        cum = 0.0
        chosen = candidates[-1]
        for j in range(len(probs)):
            cum += probs[j]
            if r < cum:
                chosen = candidates[j]
                break
        slug_out[i] = chosen

        mu = (alpha_p[chosen] + beta_i[cust] +
              np.dot(Lambda_p[chosen], f_t) + np.dot(eta_i[cust], f_t) +
              np.random.normal(0.0, mu_noise_sigma))
        qty = 1 + np.random.poisson(np.exp(mu / 3.0))
        qty_out[i] = max(qty, 1)

        season = np.dot(kappa_p[chosen], f_t)
        bias   = np.dot(store_embed[sidx], prod_embed[chosen]) * 0.15
        noise  = np.random.normal(0.0, price_noise_sigma)
        price_out[i] = slug_base_price[chosen] * np.exp(season + bias + noise)

    return slug_out, qty_out, price_out

# -----------------------------
# 7. MAIN LOOP (SQLite-safe)
# -----------------------------
print("Starting 25.2 million transactions – ~15–22 min total...")
month_weights = np.array([0.07,0.07,0.08,0.08,0.13,0.16,0.08,0.08,0.08,0.08,0.11,0.11])
month_weights /= month_weights.sum()

tx_id = 1
pbar = tqdm(total=num_transactions, desc="Tx", unit="tx")

for start in range(0, num_transactions, chunk_size):
    sz = min(chunk_size, num_transactions - start)

    # Customers
    cust_idx = np.random.choice(len(customers), sz, p=customer_probs)
    chosen = customers.iloc[cust_idx].reset_index(drop=True)

    # Dates
    months = np.random.choice(np.arange(1,13), sz, p=month_weights)
    sale_dates = np.concatenate([
        np.random.choice(dates_by_month[m], size=(months == m).sum(), replace=True)
        for m in range(1,13)
    ])
    sale_dates_py = sale_dates.astype('datetime64[D]').astype(object)
    day_indices = np.frompyfunc(date_to_row.__getitem__, 1, 1)(sale_dates_py).astype(np.int32)

    # Stores with local bias
    store_ids_chunk = np.random.choice(valid_store_ids, sz)
    local = np.random.rand(sz) < 0.82
    for i in np.where(local)[0]:
        city = chosen.loc[i, 'city']
        candidates = [s for s in city_to_stores.get(city, []) if s in store_to_idx]
        if candidates:
            store_ids_chunk[i] = np.random.choice(candidates)
    store_rep_idx = np.array([store_to_idx[s] for s in store_ids_chunk], dtype=np.int32)

    # -------------------------
    # Transactions table insert
    # -------------------------
    tx_chunk = pd.DataFrame({
        'transaction_id': range(tx_id, tx_id + sz),
        'customer_id'   : chosen['customer_id'].values,
        'store_id'      : store_ids_chunk,
        'sale_date'     : sale_dates_py
    })

    # IMPORTANT: NO method='multi'
    tx_chunk.to_sql('transactions', conn, if_exists='append',
                    index=False, chunksize=50_000)

    # -------------------------
    # Line items
    # -------------------------
    baskets   = np.clip(np.random.poisson(2.4, sz) + 1, 1, 30)
    tx_rep    = np.repeat(tx_chunk['transaction_id'].values, baskets)
    store_rep = np.repeat(store_rep_idx, baskets)
    day_rep   = np.repeat(day_indices, baskets)
    cust_rep  = np.repeat(cust_idx, baskets)

    slugs_idx, quantities, prices = simulate_line_items(
        tx_rep, cust_rep, store_rep, day_rep,
        alpha_p, beta_i, Lambda_p, eta_i,
        store_embed, prod_embed,
        slug_base_price, kappa_p,
        mu_noise_sigma, price_noise_sigma,
        F_mat,
        flat_slug_idxs, store_offsets
    )

    li_chunk = pd.DataFrame({
        'transaction_id': tx_rep,
        'slug': idx_to_slug_array[slugs_idx],
        'quantity': quantities,
        'price': np.round(prices, 2),
        'sale_date': np.repeat(sale_dates_py, baskets)
    })

    li_chunk.to_sql('line_items', conn, if_exists='append',
                    index=False, chunksize=50_000)

    tx_id += sz
    pbar.update(sz)

pbar.close()
conn.close()

print(f"\nSUCCESS! Database saved to:\n   {db_path}")
print(f"   • {num_transactions:,} transactions")
print(f"   • ~{int(num_transactions * 3.4):,} line items")
