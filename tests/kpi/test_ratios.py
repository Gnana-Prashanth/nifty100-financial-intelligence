import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)


from src.analytics.ratios import net_profit_margin

print("Normal Case")
print(net_profit_margin(100, 1000))

print("Zero Sales:")
print(net_profit_margin(100,0))



from src.analytics.ratios import operating_profit_margin

print("\n Operaating Profit Margin:")

print("Normal Case:")
print(operating_profit_margin(250, 1000))

print("Zero Sales:")
print(operating_profit_margin(250, 0))



from src.analytics.ratios import opm_cross_check
print("\nOPM Cross Check:")
print(opm_cross_check(25.0, 25.5)) #False
print(opm_cross_check(25.0, 27.5)) #True



from src.analytics.ratios import return_on_equity

print("\nReturn on Equity:")

print("Normal Case:")
print(return_on_equity(200, 100, 900))

print("Zero Equity:")
print(return_on_equity(200, 100, -100))

print("Negative Equity:")
print(return_on_equity(200, -50, -100))



from src.analytics.ratios import return_on_capital_employed

print("\nReturn on Capital Employed:")

print("Normal Case:")
print(return_on_capital_employed(300, 100, 600, 300))

print("Zero Capital:")
print(return_on_capital_employed(300, 100, -100, 0))

print("Negative Capital:")
print(return_on_capital_employed(300, -100, -200, 0))



from src.analytics.ratios import return_on_assets

print("\nReturn on Assets:")

print("Normal Case:")
print(return_on_assets(150, 3000))

print("Zero Assets:")
print(return_on_assets(150, 0))

print("Negative Assets:")
print(return_on_assets(150, -500))



from src.analytics.ratios import debt_to_equity

print("\nDebt-to-Equity:")

print("Normal Case:")
print(debt_to_equity(500, 100, 900))

print("Debt Free:")
print(debt_to_equity(0, 100, 900))

print("Zero Equity:")
print(debt_to_equity(500, 100, -100))



from src.analytics.ratios import high_leverage_flag

print("\nHigh Leverage Flag:")

print(high_leverage_flag(6, "Technology"))

print(high_leverage_flag(6, "Financials"))

print(high_leverage_flag(3, "Technology"))

print(high_leverage_flag(None, "Technology"))



from src.analytics.ratios import interest_coverage_ratio

print("\nInterest Coverage Ratio:")

print("Normal Case:")
print(interest_coverage_ratio(400, 100, 50))

print("Debt Free:")
print(interest_coverage_ratio(400, 100, 0))



from src.analytics.ratios import icr_label

print("\nICR Label:")

print(icr_label(None))

print(icr_label(10))



from src.analytics.ratios import icr_warning_flag

print("\nICR Warning Flag:")

print(icr_warning_flag(1.2))

print(icr_warning_flag(2.5))

print(icr_warning_flag(None))



from src.analytics.ratios import net_debt

print("\nNet Debt:")

print("Normal Case:")
print(net_debt(500, 150))

print("More Investments:")
print(net_debt(100, 150))



from src.analytics.ratios import asset_turnover

print("\nAsset Turnover:")

print("Normal Case:")
print(asset_turnover(1000, 500))

print("Zero Assets:")
print(asset_turnover(1000, 0))