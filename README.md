# Django RESTful API for a simple blogging platform

Take-home assignment for First Principles Publishing.

## Overview

This is a Django application that meets the specified requirements. It includes functionality for creating, reading, updating, and deleting blog posts via a RESTful API, and an admin interface for managing blog posts.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed on your local machine.
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed on your local machine.

## Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Hercules2013/django-blog.git
    cd django-blog
    ```

2. **Add a database password**:

    Create a `secrets/password.txt` file and add a password. The contents don't actually matter.

3. **Start the application using Docker Compose**:

    ```bash
    docker-compose up
    ```

4. **Access the site**:

    Open your browser and navigate to [http://localhost:8000/admin/](http://localhost:8000/admin/).

5. **Login to the admin site**:

    - Username: `admin`
    - Password: `password`

## Using the API

This application uses [Django REST Framework Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) for token-based authentication.

### Obtain JWT Tokens

1. **Get a JWT token**:

    POST your username and password to the endpoint `/api/token/`:

    ```bash
    curl -X POST http://localhost:8000/api/token/ \
    -H "Content-Type: application/json" \
    -d '{"username": "your_username", "password": "your_password"}'
    ```

    The response will contain `access` and `refresh` tokens:

    ```json
    {
      "refresh": "your_refresh_token",
      "access": "your_access_token"
    }
    ```

2. **Use the access token in requests**:

    Include the access token in the `Authorization` header for authenticated requests:

    ```bash
    curl -H "Authorization: Bearer <your_access_token>" \
    http://localhost:8000/blogposts/
    ```

### Refresh JWT Token

If you receive a 403 error, refresh your token using the `refresh` token:

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
-H "Content-Type: application/json" \
-d '{"refresh": "your_refresh_token"}'
```

## API Endpoints

- `POST /blogposts/` - Creating a new blog post.
- `GET /blogposts/` - Retrieving a list of all blog posts.
- `GET /blogposts/<pk>/` - Retrieving a single blog post by its ID.
- `PUT /blogposts/<pk>/` - Updating an existing blog post.
- `DELETE /blogposts/<pk>/` - Deleting a blog post.
