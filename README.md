# EDUCATION SYSTEM

This README provides an overview of the project architecture and instructions for using the API and populating the database. Please follow the guidelines below to ensure smooth execution.

## Getting Started

### Project Architecture

The project architecture consists of three models: Group, Product, and Lesson. You can find the implementation of these models in the edu_connect/models.py file.

### Database Setup

To set up the database and make the necessary migrations, follow these step:

1. Open the terminal and run the following commands:

```python
python manage.py makemigrations
python manage.py migrate 
```

### Creating Entities in the Shell

To create groups, users, products, and lessons in the shell, follow these steps:

1. Open the terminal and run the following command:
```python
python manage.py shell
```

2. Import the required functions by executing the following command inside the shell:
```python
from edu_connect.views import create_group, create_user, create_product, create_lesson
```
3. Use the provided commands to create the desired entities:

- To create a new user, use the following command:
```python
?NAME_OF_USER? = create_user("?USERNAME?" -> str)
```
- To create a new product, use the following command:
```python
?PRODUCT? = create_product("?USERNAME_OF_CREATOR?" -> str, "?NAME_OF_PRODUCT?" -> str, "START_DATE" -> str, COST_OF_PRODUCT -> int, MIN_USERS_IN_GROUP -> int, MAX_USERS_IN_GROUP -> int)
```
- To create a new group, use the following command:
```python
?NAME_OF_GROUP? = create_group("?NAME_OF_PRODUCT?" -> str, "?NAME_OF_GROUP?" -> str)
```
- To create a new lesson, use the following command:
```python
?NAME_OF_LESSON? = create_lesson("?NAME_OF_PRODUCT?" -> str, "?NAME_OF_LESSON?" -> str, "?VIDEO_LINK?" -> None)
```

### Granting User Access to a Product
To provide a user with access to a product, you need to add the user to a group. Follow these steps:
1. Import the required function by executing the following command in the shell:
```python
from edu_connect.views import get_user_id
```

2. Use the following command to add the user to the group:
```python
?PRODUCT?.add_student_to_group(get_user_id(?NAME_OF_USER?))
```

### Balancing Users in Groups
If a product hasn't started yet and you want to balance the number of users in groups, use the following command:
```python
?PRODUCT?.balance_group_try()
```

### Running the API
To run the API, follow these steps:
1. Open the terminal and run the following command:
```python
python manage.py runserver
```
2. Open your web browser and go to http://127.0.0.1:8000/ to access the API.

### API Endpoints
1. **API for a list of products available for purchase:** This endpoint provides basic information about the available products and the number of lessons associated with each product. The API response will include two sections:
- "upcoming_products": This section contains a list of available products.
- "ongoing_products": This section contains a list of products that are currently ongoing.

2. **API for a list of lessons for a specific product:** This endpoint displays a list of lessons for a specific product to which the user has access. To access this API, append the username of the user to the URL in the following format: http://127.0.0.1:8000/lessons/?username=?NAME_OF_USER?. After making this request, you will receive a list of available lessons for the user.

3. The API is not working correctly and does not display the group fill percentage accurately.