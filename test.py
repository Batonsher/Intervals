import mathmodel


model = mathmodel.Bahriddin("genetech2504x38", nominal_features_set=True)

# print(model)
# model.print_df()

RS1 = model.generalized_estimate_func2([34,10,13,20,22,37,17,18])
# RS2 = model.generalized_estimate_func2([2])
# print(model.original_df[0], model.original_df[32])
# model.scatter(RS1, RS2)
# model.scatter(model.original_df[0], model.original_df[32])
print('#'*10)
for el in RS1.items():
    print(el)


# print(model.generalized_estimate)
