#lesson with list
list1=["rohan",["ankit",["pappu","karan","nikku"]]]
##print (list1)
##print (list1[1])
##print (list1.pop())
##list1.extend(["vishal","anish"])
##print (list1)
##list1.remove("ankit")
##print (list1)
##list1.insert(1,"rahul")
##print (list1)

#iteration
for item in list1:
    print (item)

c=0
while c<len(list1):
    print (list1[c])
    c=c+1
print (isinstance(list1,list))

#functions

def print_lol(the_list):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item)
        else:
            print (item)

print_lol(list1)


