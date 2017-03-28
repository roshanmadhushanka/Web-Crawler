from io_my import FileHandler

file_handler = FileHandler(file_name='company_list')
lst = ['asdas/asdasd', 'sdasd/asdads', 'asdasd/asdasd']
file_handler.write(lst)