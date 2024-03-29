def print_sandwich(bread, meat, *args): 
    print(f'{meat} on {bread}', end=' ') 
    if len(args) > 1: 
        print('with', end=' ') 
    for extra in args: 
        print(extra, end=' ') 
    print('')

print_sandwich('sourdough', 'turkey', 'lettuce', 'mayo')
print_sandwich('wheat', 'ham', 'mustard', 'tomato', 'lettuce')