# pizza = [
#     {"item": "journal", "qty": 25, "size": {
#         "h": 14, "w": 21, "uom": "cm"}, "status": "A"},
#     {"item": "notebook", "qty": 50, "size": {
#         "h": 8.5, "w": 11, "uom": "in"}, "status": "A"},
#     {"item": "paper", "qty": 100, "size": {
#         "h": 8.5, "w": 11, "uom": "in"}, "status": "D"},
#     {"item": "planner", "qty": 75, "size": {
#         "h": 22.85, "w": 30, "uom": "cm"}, "status": "D"},
#     {"item": "postcard", "qty": 45, "size": {
#         "h": 10, "w": 15.25, "uom": "cm"}, "status": "A"}
# ]

# pizza1 = pizza.find({status:"A","size.w":21})


pizza = [
    {item: "journal", qty: 25, tags: ["blank", "red"], dim_cm: [14, 21]},
    {item: "notebook", qty: 50, tags: ["red", "blank"], dim_cm: [14, 21]},
    {item: "paper", qty: 100, tags: [
        "red", "blank", "plain"], dim_cm: [14, 21]},
    {item: "planner", qty: 75, tags: ["blank", "red"], dim_cm: [22.85, 30]},
    {item: "postcard", qty: 45, tags: ["blue"], dim_cm: [10, 15.25]}
]
pizza.find({item:"paper",tags:"blank",dim_cm:21})
db.inventory.find( { "dim_cm.1": { $gt: 25 } } )