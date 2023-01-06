import mathmodel


model = mathmodel.Bahriddin("test1")

print(model)
model.print_df()

print('#'*10)
for el in model.generalized_estimate.items():
    print(el)

# print(model.generalized_estimate)
