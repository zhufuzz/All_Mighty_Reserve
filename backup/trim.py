# abc = " abc "
# print abc.trim()


abc = " tag1, tag2, tag4, ,"
result =[]
tagList1 = abc.strip().split(',')
for tag in tagList1:
    if (tag is not None) and (tag.strip() != ""):
        result.append(tag.strip())

print result