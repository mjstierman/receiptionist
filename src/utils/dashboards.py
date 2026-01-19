def topTenCategories(db):
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

def thisMonthSpending(db):
    """ Get net spending for the current month """
    query = """
        SELECT 
            SUM(CASE WHEN r.income = 0 THEN r.amount ELSE 0 END) as total_spent,
            SUM(CASE WHEN r.income = 1 THEN r.amount ELSE 0 END) as total_income
        FROM receipts r
        WHERE strftime('%Y-%m', r.date) = strftime('%Y-%m', 'now')
    """
    result = db.execute(query)
    net_spending = result[0]['total_spent'] - result[0]['total_income']
    return net_spending

def thisMonthsReceipts(db):
    """ Get all receipts for the current month """
    query = """
        SELECT *
        FROM receipts
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        ORDER BY date DESC
    """
    return db.execute(query)