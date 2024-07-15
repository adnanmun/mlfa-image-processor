import json

def getImgInfo(json_file):
    json_data = json.load(json_file)
    json_data = {k.lower(): v for k, v in json_data.items()}
    
    attributes = {}
    if 'lightfieldattributes' in json_data:
        light_field_attributes = {k.lower(): v for k, v in json_data['lightfieldattributes'].items()}
        attributes = {
            'hogelDimensions': light_field_attributes.get('hogeldimensions', 'N/A'),
            'directionalResolution': light_field_attributes.get('directionalresolution', 'N/A'),
            'displayFOV': light_field_attributes.get('displayfov', 'N/A'),
            'file': light_field_attributes.get('file', 'N/A')
        }
        print("Attributes extracted:", attributes)
    else:
        print("LightFieldAttributes not found in JSON data")
        attributes = {'hogelDimensions': 'N/A', 'directionalResolution': 'N/A', 'displayFOV': 'N/A', 'file': 'N/A'}
    return attributes