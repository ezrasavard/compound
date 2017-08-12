import datetime
import mapper

"""
Provide methods for executing common queries against the DB
"""

"""
Fetch all transactions within the given time range [t0, t1)
@param t0: datetime object for inclusive start of query
@param t1: datetime object for exclusive end of query
@return: list of mapper.Transaction objects
"""
def get_transactions_by_time_range(t0, t1):
    mapper.Transaction.objects()
