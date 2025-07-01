# from subdirectory.filename import function_name

#from functions.write_file import write_file
from functions.run_python import run_python_file
#from functions.get_files_info import get_files_info
#from functions.get_file_content import get_file_content

#print(get_files_info("calculator", "."))
#print(get_files_info("calculator", "pkg"))
#print(get_files_info("calculator", "/bin"))
#print(get_files_info("calculator", "../"))


#print(get_file_content("main.py"))
#print(get_file_content("calculator", "pkg/calculator.py"))
#print(get_file_content("calculator", "/bin/cat"))


#print(write_file("main.txt", "This is main"))
#print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
#print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


#print(run_python_file("calculator", "main.py"))
print(run_python_file("tests.py"))
#print(run_python_file("calculator", "../main.py"))
#print(run_python_file("calculator", "nonexistent.py"))
#print(run_python_file("calculator", "lorem.txt"))