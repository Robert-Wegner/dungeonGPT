import pandas as pd

data = [
    {"name": "John Doe", "age": 30, "income": 70000},
    {"name": "Jane Doe", "age": 28, "income": 80000},
    {"name": "Jim Doe", "age": 35, "income": 60000},
    {"name": "Jill Doe", "age": 32, "income": 75000}
]

df = pd.DataFrame(data)

data2 = [
    {"name": "Alice", "age": 25, "profession": "Engineer"},
    {"name": "Bob", "age": 30, "profession": "Doctor"},
    {"name": "Charlie", "age": 35, "profession": "Teacher"},
    {"name": "Diana", "age": 40, "profession": "Scientist"}
]
df2 = pd.DataFrame(data2)




df3 = pd.concat([
    df[['name', 'age']].assign(Type='one'),
    df2[['name', 'age']].assign(Type='two')
], ignore_index=True)

print(df3)


