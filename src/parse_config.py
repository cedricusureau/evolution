def parse_config_file(config_path):
    line = [i.replace("\n","") for i in open(config_path, "r")]
    variables = {}
    for i in line:
        i = i.replace(" ","")
        splitted = i.split("=")
        try:
            variables[splitted[0]] = int(splitted[1])
        except:
            variables[splitted[0]] = [float(i) for i in splitted[1].split("-")]

    variables["width"] = variables["map_size"] * variables["img_size"]
    variables["height"] = variables["map_size"] * variables["img_size"]
    variables["screen_size"] = variables["width"], variables["height"]

    return variables