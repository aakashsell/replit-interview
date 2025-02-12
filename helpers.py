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
        
    if isinstance(output, object): 
        output = handle_objects(output)

    print("output = " + str(output))
  
    return str(output)

def handle_objects(obj):
    output = {}
    references = {}
    traverse_graph(obj, references)
    return references
    
def traverse_graph(obj, references):
    object_id = id(obj)
    if object_id in references:
        return {"ref": f"%{object_id}%"}
    
    references[object_id] =  {"id": object_id, "value": None}

    if isinstance(obj, dict):
        references[object_id]["value"] = {k: traverse_graph(v, references) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        references[object_id]["value"] = [traverse_graph(item, references) for item in obj]
    else:
        references[object_id]["value"] = obj  

    return {"ref": object_id} 
    
    

