from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from backend import storage

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """This gets all the posts,
    and will sort it by title or content if commanded"""

    # possible values for sorting
    sort_data = request.args.get('sort')
    order = request.args.get('order')

    # This code determines if sorting is needed
    if sort_data is not None or order is not None:

        # this code determines if it's ascending or descending
        # default will be ascending
        order_flag = False

        if order == "desc":
            order_flag = True

        # this code sorts the data
        blog_posts = storage.fetch_posts()
        sorted_data = sorted(blog_posts, key=lambda x: x[sort_data].lower(),
                             reverse=order_flag)

        return jsonify(sorted_data)

    # this just returns jsonified data if the fields contain nothing
    else:
        return jsonify(storage.fetch_posts())


@app.route('/api/posts', methods=['POST'])
def addpost():
    """This adds posts using the field in html"""

    # Retrieve the JSON data from the request
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    # Retrieve the entire form
    blog_posts = storage.fetch_posts()

    # Get the maximum id from existing blog posts
    max_id = 0
    for post in blog_posts:
        if 'id' in post and post['id'] > max_id:
            max_id = post['id']

    # Create a new post dictionary with an incremented id
    new_post = {
        'id': max_id + 1,
        'title': title,
        'content': content
    }

    # Append the new post to the list of blog posts
    blog_posts.append(new_post)
    storage.update_storage(blog_posts)
    return redirect('/api/posts')


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    """This code allows you to delete things"""

    blog_posts = storage.fetch_posts()

    for id_dict in blog_posts:
        if id_dict["id"] == post_id:
            blog_posts.remove(id_dict)
            break

    storage.update_storage(blog_posts)

    return redirect('/api/posts')


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update(post_id):
    """This code allows you to update blog posts"""

    # Fetch the post and its index by ID
    post_edit, post_index = storage.fetch_post_by_id(post_id)
    if post_edit is None:
        # Post not found
        return "Post not found", 404

    # Retrieve the form data from the request
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    # Create a dictionary for the updated post
    edited_text = {
        'id': post_id,
        'title': title,
        'content': content
    }

    # Update the blog posts list
    blogposts = storage.fetch_posts()
    blogposts[post_index] = edited_text
    storage.update_storage(blogposts)

    return redirect('/api/posts')


@app.route('/api/posts/search', methods=['GET'])
def search():
    """This code allows you to search"""
    # Get the title query from the request URL parameters
    search_query = request.args.get('title')

    is_content = False
    if search_query is None:
        search_query = request.args.get('content')
        is_content = True

    if search_query:
        # Fetch all posts
        blog_posts = storage.fetch_posts()

        # Filter the posts based on the title query
        search_results = []
        for post in blog_posts:
            # Check if the title query matches the title of the post
            if is_content is False:
                if search_query.lower() in post['title'].lower():
                    search_results.append(post)
            else:
                if search_query.lower() in post['content'].lower():
                    search_results.append(post)

        if len(search_results) > 0:
            return jsonify(search_results)
        else:
            return "No results", 404

    else:
        return "No title query provided", 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
