# API Documentation

## Base URL

`http://127.0.0.1:8000/api/`

---

## Endpoints

### Task Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **GET**     | `/task/tasks/`                                        | Retrieve a list of tasks                          | None         | List of tasks                         |
| **POST**    | `/task/tasks/`                                        | Create a new task                                 | Task data    | Created task                          |
| **GET**     | `/task/tasks/{id}/`                                   | Retrieve a specific task                          | None         | Task data                             |
| **PUT**     | `/task/tasks/{id}/`                                   | Update a specific task                            | Updated task data | Updated task data                  |
| **DELETE**  | `/task/tasks/{id}/`                                   | Delete a specific task                            | None         | Success message                       |

### Tag Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **GET**     | `/task/tags/`                                         | Retrieve a list of tags                           | None         | List of tags                          |
| **POST**    | `/task/tags/`                                         | Create a new tag                                  | Tag data     | Created tag                           |
| **GET**     | `/task/tags/{id}/`                                    | Retrieve a specific tag                           | None         | Tag data                              |
| **PUT**     | `/task/tags/{id}/`                                    | Update a specific tag                             | Updated tag data | Updated tag data                    |
| **DELETE**  | `/task/tags/{id}/`                                    | Delete a specific tag                             | None         | Success message                       |

### Timer Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **POST**    | `/task/{task_id}/start-timer-session/`                | Start a timer session for a task                  | None         | Timer session started (ID, time)      |
| **POST**    | `/task/save-timer-session/{session_id}/`              | save a timer session for a task                   | None         | Timer session stopped (duration)      |
| **DELETE**  | `/task/cancel-timer-session/{session_id}/`            | Cancel a timer session                            | None         | Success message                       |
               |

### Dashboard Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **GET**     | `/task/dashboard/`                                     | Get the user's dashboard data (task count, points) | None         | Dashboard data                        |

### Tag List Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **GET**     | `/task/milestones/`                                    | Get a list of tags with total and completed task counts and tags rewards | None         | Tags data with task completion info   |
