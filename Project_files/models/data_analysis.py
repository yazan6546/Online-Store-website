import pandas as pd
import utils.queries.data_analysis as da
from utils.db_utils import get_db_connection


def get_top_10_selling_products():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.TOP_10_SELLING_PRODUCTS, conn)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


def get_low_stock_products():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.LOW_STOCK_PRODUCTS, conn)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_category_count():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.CATEGORY_COUNT, conn)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_yearly_revenue(params):
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.yearly_revenue, conn, params=params)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_best_customers():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.best_customers, conn)
        return df.to_dict(orient='records')

    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_customer_demographics():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.customer_demographics, conn)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


def get_best_selling_product_by_month(year):
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.best_selling_product_by_month, conn, params={'year': year})

        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


def get_stats():
    conn = get_db_connection()
    dict = {}

    try:
        dict['count_customers'] = conn.execute(da.COUNT_CUSTOMERS).fetchone()[0]
        dict['count_orders'] = conn.execute(da.COUNT_ORDERS).fetchone()[0]
        dict['count_products'] = conn.execute(da.COUNT_PRODUCTS).fetchone()[0]
        dict['total_revenue'] = conn.execute(da.TOTAL_REVENUE).fetchone()[0]

        return dict
    except:
        print("Error in get_stats()")
    finally:
        conn.close()


def get_all_revenues():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.all_revenues, conn)
        # Group data by year and create a dictionary of DataFrames
        data_by_year = {year: data.drop(columns=['year']).to_dict(orient='records') for year, data in df.groupby('year')}


        return data_by_year

    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_age_distribution():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.AGE_DISTRIBUTION, conn)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_top_5_products():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.TOP_5_SELLING_PRODUCTS, conn)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_recent_orders():
    conn = get_db_connection()
    try:
        df = pd.read_sql(da.CUSTOMER_RECENT_ORDERS, conn)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


