import json


def fetch_posts():
    """This function fetches posts"""
    with open("data.json") as fileobj:
        blog_posts = json.load(fileobj)
    return blog_posts


def fetch_post_by_id(post_id):
    """This function searches for posts by their id"""
    blog_posts = fetch_posts()
    for id_dict in blog_posts:
        if id_dict["id"] == post_id:
            return id_dict, blog_posts.index(id_dict)
    return None, None


def update_storage(data):
    """This function updates the data.json file"""
    with open('data.json', 'w') as file:
        json.dump(data, file)