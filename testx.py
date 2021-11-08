i=0
list=[]
while i<91:
    i+=1
    list.append(i)
    i+=1
    list.append(i)
    i+=1
    i+=1

list.reverse()
print(list)

# create a list of prime numbers
prime_numbers = [2, 3, 5, 7]

# reverse the order of list elements
prime_numbers.reverse()


print('Reversed List:', prime_numbers)

# Output: Reversed List: [7, 5, 3, 2]