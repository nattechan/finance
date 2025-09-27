import QuantLib as ql
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)

ql.Settings.instance().evaluationDate = ql.Date(15, ql.January, 2024)

schedule = ql.MakeSchedule(
    effectiveDate=ql.Date(8, ql.February, 2021),
    terminationDate=ql.Date(8, ql.February, 2026),
    frequency=ql.Semiannual,
    calendar=ql.Canada(),
    convention=ql.Following,
    backwards=True,
)

for d in schedule:
    log.info(d)

day_count = ql.Thirty360(ql.Thirty360.BondBasis)

fixed_coupons = ql.FixedRateLeg(
    schedule=schedule,
    couponRates=[0.03],
    dayCount=day_count,
    nominals=[10_000],
)

settlement_days = 3
issue_date = ql.Date(5, ql.February, 2021)

bond1 = ql.Bond(
    settlement_days,
    ql.TARGET(),
    issue_date,
    fixed_coupons,
)

data = []
for cf in bond1.cashflows():
    c = ql.as_coupon(cf)
    if c is not None:
        data.append((c.date(), c.nominal(), c.rate(), c.amount()))
    else:
        data.append((cf.date(), None, None, cf.amount()))

bond_df = pd.DataFrame(data, columns=["date", "nominal", "rate", "amount"])

log.info(bond_df)

price = ql.BondPrice(98.0, ql.BondPrice.Clean)
b = bond1.bondYield(price, day_count, ql.Compounded, ql.Semiannual)

log.info(f"Yield: {b:.6%}")