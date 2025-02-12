def execute_code(code, global_vars, local_vars):
    #try using eval
    output = ""
    try:
        output = eval(code, global_vars, local_vars)
    except Exception as e1:
        #try using exec
        print("eval didn't work, trying exec ")
        try:
           output = exec(code, global_vars, local_vars) 
        except Exception as e2:
            print("exec didn't work, retuning 0 ")
            return 0
    print(output)
    return output
    