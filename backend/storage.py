import json


def fetch_posts():
    """This fetches posts"""

    with open("data.json") as fileobj:
        blog_posts = json.load(fileobj)
        return blog_posts


def fetch_post_by_id(post_id):
    """This code searches for posts, grabs them by their id,
    and then deletes the dict"""

    blog_posts = fetch_posts()
    for id_dict in blog_posts:
        if id_dict["id"] == post_id:
            dict_return = id_dict
            dict_location = blog_posts.index(id_dict)
            return dict_return, dict_location
    else:
        return None, None


def update_storage(data):
    """This code updates the data.json file"""
    with open('data.json', 'w') as file:
        json.dump(data, file)
