import json

def getImgInfo(json_file):
    hogel_dimensions = None
    directional_resolution = None
    file = None

    json_content = json_file.read()
    json_string = json_content.decode('utf-8')
    json_data = json.loads(json_string)

    if 'lightFieldAttributes' in json_data:
        light_field_attributes = json_data['lightFieldAttributes']
        if 'hogelDimensions' in light_field_attributes:
            hogel_dimensions = light_field_attributes['hogelDimensions']
            print("Hogel dimensions:", hogel_dimensions)
        else:
            print("Hogel dimensions not found in LightFieldAttributes")
        if 'directionalResolution' in light_field_attributes:
            directional_resolution = light_field_attributes['directionalResolution']
            print("Directional Resolution:", directional_resolution)
        else:
            print("Directional Resolution not found in LightFieldAttributes")
        if 'file' in light_field_attributes:
            file = light_field_attributes['file']
            print("file:", file)
        else:
            print("file not found in LightFieldAttributes")

    else:
        print("LightFieldAttributes not found in JSON data")

    return hogel_dimensions, directional_resolution, file