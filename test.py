
from util.write_excel import init_data, write_to_excel

source = '胡杖子'
data = init_data(source)
fileName = f'/Users/yunfeiwang/Desktop/{source}.xls'
write_to_excel(data, fileName)
