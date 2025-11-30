# Social Media Feed Backend

A scalable, high-performance backend for a social media feed, built with Django, PostgreSQL, and GraphQL.

## Features

-   **GraphQL API**: Flexible querying for posts, users, and interactions.
-   **Authentication**: Secure JSON Web Token (JWT) authentication.
-   **Post Management**: Create, read, and manage posts.
-   **Interactions**: Like and comment on posts.
-   **Pagination**: Relay-style pagination for infinite scrolling.
-   **Filtering**: Advanced filtering by content, author, and date.
-   **Optimization**: Efficient database queries using `select_related` and `prefetch_related`.
-   **Dockerized**: Easy deployment with Docker and Docker Compose.
-   **Background Tasks**: Celery and Redis configuration for async tasks.

## Tech Stack

-   **Backend**: Django 5.0, Python 3.11
-   **API**: Graphene-Django (GraphQL)
-   **Database**: PostgreSQL 15
-   **Cache/Queue**: Redis 7
-   **Task Queue**: Celery 5.3

## Database Schema

You can view the Entity Relationship Diagram (ERD) in [ERD.md](ERD.md).

## Getting Started

### Prerequisites

-   Docker and Docker Compose installed.

### Installation

1.  Clone the repository.
2.  Create a `.env` file (optional, defaults provided in `docker-compose.yml`).
3.  Build and start the services:

    ```bash
    docker-compose up --build
    ```

4.  Apply migrations:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  Create a superuser:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

6.  Access the GraphQL Playground at `http://localhost:8000/graphql`.

## API Usage

### Postman Collection

A `postman_collection.json` file is included in the root directory. You can import this into Postman to easily test the API endpoints.

### Authentication

**Obtain Token:**

```graphql
mutation {
  tokenAuth(username: "youruser", password: "yourpassword") {
    token
  }
}
```

### Posts

**Query All Posts (with Pagination & Filtering):**

```graphql
query {
  allPosts(first: 10, content_Icontains: "hello") {
    edges {
      node {
        id
        content
        author {
          username
        }
        likeCount
        commentCount
      }
    }
  }
}
```

**Create Post:**

```graphql
mutation {
  createPost(content: "Hello World!") {
    post {
      id
      content
    }
  }
}
```

## Testing

Run the test suite:

```bash
docker-compose exec web python manage.py test
```
