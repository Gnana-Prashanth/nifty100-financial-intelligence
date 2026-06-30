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


from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr
)

print("1. Normal:")
print(calculate_cagr(100, 200, 5, 5))

print("\n2. Decline to Loss:")
print(calculate_cagr(100, -20, 5, 5))

print("\n3. Turnaround:")
print(calculate_cagr(-50, 100, 5, 5))

print("\n4. Both Negative:")
print(calculate_cagr(-100, -50, 5, 5))

print("\n5. Zero Base:")
print(calculate_cagr(0, 100, 5, 5))

print("\n6. Insufficient Data:")
print(calculate_cagr(100, 200, 5, 3))



print("\nRevenue CAGR")

print("3 Year")
print(revenue_cagr(100, 150, 3, 3))

print("5 Year")
print(revenue_cagr(100, 220, 5, 5))

print("10 Year")
print(revenue_cagr(100, 420, 10, 10))



print("\nPAT CAGR")

print("3 Year")
print(pat_cagr(50, 100, 3, 3))

print("5 Year")
print(pat_cagr(50, 150, 5, 5))

print("10 Year")
print(pat_cagr(50, 300, 10, 10))



print("\nEPS CAGR")

print("3 Year")
print(eps_cagr(5, 8, 3, 3))

print("5 Year")
print(eps_cagr(5, 12, 5, 5))

print("10 Year")
print(eps_cagr(5, 20, 10, 10))