# compressed all duplicate code into this 1 function using list comprehension 
def get_stats(records):
    # go through each dict in records, grab every value in it, and put them all into one list
    # e.g. [{"amount": 100}, {"amount": 250}] -> [100, 250]
    values = [value for record in records for value in record.values()]
    total = sum(values)
    average = total / len(values) if values else 0
    return {"total": total, "average": average, "highest": max(values), "lowest": min(values)}

def print_report(title, records):
    stats = get_stats(records)
    print(f"{title} Report")
    print(f"  Total:   ${stats['total']:.2f}")
    print(f"  Average: ${stats['average']:.2f}")
    print(f"  Highest: ${stats['highest']:.2f}")
    print(f"  Lowest:  ${stats['lowest']:.2f}")

# For this challenge, do not change the following 3 lines:
sales = [{"amount": 100}, {"amount": 250}, {"amount": 75}]
marketing = [{"budget": 500}, {"budget": 300}, {"budget": 800}]
engineering = [{"hours": 40}, {"hours": 35}, {"hours": 45}]

print_report("Sales", sales)
print_report("Marketing", marketing)
print_report("Engineering", engineering)

