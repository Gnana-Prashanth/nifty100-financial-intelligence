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