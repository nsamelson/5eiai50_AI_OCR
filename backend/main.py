from flask import Flask
app = Flask(__name__)

# create a list to store our "database"
my_list = [1,2,3]


@app.route('/')
def hello_world():
   return "hey baby"

# define a route that returns the contents of our list
@app.route('/list', methods=['GET'])
def get_list():
    return jsonify(my_list)

# define a route that allows us to add items to our list
@app.route('/list', methods=['POST'])
def add_to_list():
    # get the item from the request body
    item = request.get_json()
    # append the item to our list
    my_list.append(item)
    # return the updated list
    return jsonify(my_list)

# define a route that allows us to update an item in our list
@app.route('/list/<int:index>', methods=['PUT'])
def update_list_item(index):
    # get the item from the request body
    item = request.get_json()
    # update the item in our list at the specified index
    my_list[index] = item
    # return the updated list
    return jsonify(my_list)

# define a route that allows us to delete an item from our list
@app.route('/list/<int:index>', methods=['DELETE'])
def delete_from_list(index):
    # delete the item from our list at the specified index
    del my_list[index]
    # return the updated list
    return jsonify(my_list)



if __name__ == '__main__':
   app.run()