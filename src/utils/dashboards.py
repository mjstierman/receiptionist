import logging

def top_ten_categories(db):
    """ Get the top ten categories by total amount spent """
    query = """
        SELECT c.name, SUM(r.amount) as total_amount
        FROM receipts r
        JOIN categories c ON r.category = c.id
        GROUP BY c.name
        ORDER BY total_amount DESC
        LIMIT 10
    """
    return db.execute(query)

def this_month_spending(db):
    """ Get net spending for the current month """
    query = """
        SELECT 
            SUM(CASE WHEN r.income = 0 THEN r.amount ELSE 0 END) as total_spent,
            SUM(CASE WHEN r.income = 1 THEN r.amount ELSE 0 END) as total_income
        FROM receipts r
        WHERE strftime('%Y-%m', r.date) = strftime('%Y-%m', 'now')
    """
    result = db.execute(query)
    logging.info("This month spending result %s %s", result[0]['total_spent'], result[0]['total_income'])
    try:
        net_spending = round(result[0]['total_spent'] - result[0]['total_income'], 2)
        logging.info("This month spending result: %s", net_spending)
        return net_spending
    except Exception as e:
        logging.error("Error calculating net spending: %s", e)
        return False

def this_month_receipts(db):
    """ Get all receipts for the current month """
    query = """
        SELECT *
        FROM receipts
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        ORDER BY date DESC
    """
    return db.execute(query)