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


from src.analytics.cashflow import free_cash_flow

print("Free Cash Flow")

print(free_cash_flow(500,-150))
print(free_cash_flow(100,-250))



from src.analytics.cashflow import cfo_quality_score

print("\nCFO Quality")

print(cfo_quality_score(600,500))
print(cfo_quality_score(350,500))
print(cfo_quality_score(150,500))
print(cfo_quality_score(100,0))



from src.analytics.cashflow import capex_intensity

print("\nCapEx Intensity")

print(capex_intensity(-60, 3000))      # 2% -> Asset Light
print(capex_intensity(-120, 3000))     # 4% -> Moderate
print(capex_intensity(-500, 3000))     # 16.67% -> Capital Intensive
print(capex_intensity(-100, 0))        # None



from src.analytics.cashflow import fcf_conversion_rate

print("\nFCF Conversion Rate")

print(fcf_conversion_rate(300, 400))
print(fcf_conversion_rate(150, 300))
print(fcf_conversion_rate(100, 0))



from src.analytics.cashflow import capital_allocation_pattern

print("\nCapital Allocation Pattern")

print(capital_allocation_pattern(100,-50,-30))
print(capital_allocation_pattern(100,-50,-30,"High Quality"))
print(capital_allocation_pattern(100,50,-20))
print(capital_allocation_pattern(-50,20,40))
print(capital_allocation_pattern(100,-30,40))
print(capital_allocation_pattern(100,20,40))
print(capital_allocation_pattern(-100,-50,-20))
print(capital_allocation_pattern(-10,-20,30))