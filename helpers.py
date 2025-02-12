def execute_code(code, global_vars, local_vars):
    #try using eval
    output = ""
    try:
        output = eval(code, global_vars, local_vars)
        print(output)
    except Exception as e1:
        #try using exec
        print("eval didn't work, trying exec ")
        error = e1
        try:
           output = exec(code, global_vars, local_vars) 
           print(output)
        except Exception as e2:
            error = e2
            print("exec didn't work, retuning 0 ")
            return {'error': error}
        
    
    output = handle_objects(output)
    
    print("output = " + str(output))
  
    return output

def handle_objects(obj):
    output = {}
    references = {}
    traverse_graph(obj, references)
    output['root'] = id(obj)
    output['data'] = references
    return output
    
def traverse_graph(obj, references):
    object_id = id(obj)
    if object_id in references:
        return {"ref": object_id}
    
    references[object_id] =  {"id": object_id, "value": None}

    if isinstance(obj, dict):
        references[object_id]["value"] = {k: traverse_graph(v, references) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        references[object_id]["value"] = [traverse_graph(item, references) for item in obj]
    else:
        references[object_id]["value"] = obj  

    return {"ref": object_id} 
    
    

