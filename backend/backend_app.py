from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from operator import itemgetter
from storage import fetch_posts, fetch_post_by_id, update_storage


class BackendApp:
    """This handles the entire blog code"""

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)  # This will enable CORS for all routes
        self.setup_routes()

    def setup_routes(self):
        """This code sets up the routes"""
        self.app.route('/api/posts', methods=['GET'])(
            self.get_posts)

        self.app.route('/api/posts', methods=['POST'])(
            self.add_post)

        self.app.route('/api/posts/<int:post_id>', methods=['DELETE'])(
            self.delete_post)

        self.app.route('/api/posts/<int:post_id>', methods=['PUT'])(
            self.update_post)

        self.app.route('/api/posts/search', methods=['GET'])(
            self.search_posts)

    @staticmethod
    def get_posts():
        """This code gets all the posts"""
        sort_data = request.args.get('sort')
        order = request.args.get('order')

        if sort_data is not None or order is not None:
            if order != "asc" and order != "desc" and order is not None:
                return f"order must be asc or desc, you inputed {order}", 400

            order_flag = False
            if order == "desc":
                order_flag = True

            try:
                blog_posts = fetch_posts()
                sorted_data = sorted(blog_posts, key=itemgetter(sort_data),
                                     reverse=order_flag)

                return jsonify(sorted_data)
            except KeyError:
                return f"{sort_data} has to be either title or content", 400
        else:
            return jsonify(fetch_posts())

    @staticmethod
    def add_post():
        """This code adds a post and saves it"""
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        blog_posts = fetch_posts()

        max_id = 0
        for post in blog_posts:
            if 'id' in post and post['id'] > max_id:
                max_id = post['id']

        new_post = {
            'id': max_id + 1,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)
        update_storage(blog_posts)
        return redirect('/api/posts')

    @staticmethod
    def delete_post(post_id):
        """This code deletes posts"""
        blog_posts = fetch_posts()

        for id_dict in blog_posts:
            if id_dict["id"] == post_id:
                blog_posts.remove(id_dict)
                break

        update_storage(blog_posts)
        return redirect('/api/posts')

    @staticmethod
    def update_post(post_id):
        """This code lets you update posts"""
        post_edit, post_index = fetch_post_by_id(post_id)
        if post_edit is None:
            return "Post not found", 404

        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        edited_text = {
            'id': post_id,
            'title': title,
            'content': content
        }

        blog_posts = fetch_posts()
        blog_posts[post_index] = edited_text
        update_storage(blog_posts)

        return redirect('/api/posts')

    @staticmethod
    def search_posts():
        """This code lets you search through posts"""
        search_query = request.args.get('title')

        is_content = False
        if search_query is None:
            search_query = request.args.get('content')
            is_content = True

        if search_query:
            blog_posts = fetch_posts()

            search_results = []
            for post in blog_posts:
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

    def run(self):
        self.app.run(host="0.0.0.0", port=5002, debug=True)


if __name__ == '__main__':
    app = BackendApp()
    app.run()
