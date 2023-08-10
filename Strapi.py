import requests


def get_classes_data(data):
    class_id_program_id_map = {}

    for class_entry in data:
        livelike_program_id = class_entry.get('attributes').get('livelikeProgramId')
        class_id = class_entry.get('id')
        print(f'{class_entry} ')
        if class_id is not None and livelike_program_id is not None:
            class_id_program_id_map[class_id] = livelike_program_id

    return class_id_program_id_map


def strapi_classes(org_id):
    url = f"https://cms.getsetuplive.com/api/organisations?filters[organisationId][$eq]={org_id}&populate=logo" \
          f"&populate[0]=classes&populate[1]=classes.instructor&populate[2]=classes.coverImages&populate[" \
          f"3]=classes.category&populate[4]=classes.tags&populate[5]=classes.instructor.profilePictureImage&populate[" \
          f"6]=featured_classes&populate[7]=featured_classes.instructor&populate[" \
          f"8]=featured_classes.coverImages&populate[9]=featured_classes.category&populate[" \
          f"10]=featured_classes.tags&populate[11]=featured_classes.instructor.profilePictureImage&populate[" \
          f"12]=featured_tags&populate[13]=featured_classes.coverImages2.image&populate[14]=classes.coverImages2.image"

    class_id_program_id_map = {}

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data and len(data) > 0:
            classes = data[0].get('attributes', {}).get('classes', {}).get('data', [])
            class_id_program_id_map = get_classes_data(classes)
    else:
        print(f"Unable to get info from Strapi for org {org_id}")

    return class_id_program_id_map
