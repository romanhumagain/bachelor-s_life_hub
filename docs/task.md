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


#### Task request body (for adding task)
``` json 
{
    "title": "Test Title",
    "description": "Description for this task.",
    "due_date": "2025-03-20",
    "status": "todo",
    "priority": "medium",
    "estimated_time": 120,
    "tags": [
        {"name":"project"}, 
        {"name":"academic"}
    ]
}

```

### Tag Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **GET**     | `/task/tags/`                                         | Retrieve a list of tags                           | None         | List of tags                          |
| **POST**    | `/task/tags/`                                         | Create a new tag                                  | Tag data     | Created tag                           |
| **GET**     | `/task/tags/{id}/`                                    | Retrieve a specific tag                           | None         | Tag data                              |
| **PUT**     | `/task/tags/{id}/`                                    | Update a specific tag                             | Updated tag data | Updated tag data                    |
| **DELETE**  | `/task/tags/{id}/`                                    | Delete a specific tag                             | None         | Success message    

                   |

### Timer Endpoints


| HTTP Method | Endpoint                                              | Description                                          | Request Body                                                | Response Body                                  |
|-------------|-------------------------------------------------------|------------------------------------------------------|-------------------------------------------------------------|------------------------------------------------|
- Opt1.

| **POST**    | `/task/{task_id}/spent-time/`                          | Update the time spent on a specific task.            | ```json { "time_spent": "00:20:10" } ```                     | ```json { "detail": "Time duration saved.", "duration": "00:20:10", "total_spent_time": "01:41:10" } ``` |

- Opt2.

| **POST**    | `/task/{task_id}/start-timer-session/`                 | Start a timer session for a task (Returns session_id)| None                                                        | ```json { "message": "Timer started.", "session_id": 31, "start_time": "2025-03-15T07:31:34.138334Z", "total_time_spent": "00:07:51" } ``` |
| **POST**    | `/task/save-timer-session/{session_id}/`               | Save a timer session for a task                      | None                                                        | ```json { "message": "Timer stopped.", "session_id": 31, "duration": "00:00:28", "total_time_spent": "00:08:19" } ``` |
| **DELETE**  | `/task/cancel-timer-session/{session_id}/`             | Cancel a timer session                               | None                                                        | ```json { "message": "Timer session canceled successfully." } ``` |



**Note**  Option (1)
         - `for starting timer session hit the start-timer-session api`
         - `for saving a time session hit the save-timer-session api`
         - `Time duration will be calculated between the start-timer-session and save-timer-session`
         - `To cancel the session hit the cancel-timer-session , you cannot cancel the session that is already saved`
         
         Option (2)
         - Directly update spent time with this endpoint `/task/{task_id}/spent-time/` as described in the above table 



### Dashboard Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **GET**     | `/task/dashboard/`                                     | Get the user's dashboard data (task count, points) | None         | Dashboard data                        |

### Tag List Endpoints

| HTTP Method | Endpoint                                              | Description                                        | Request Body | Response Body                         |
|-------------|-------------------------------------------------------|----------------------------------------------------|--------------|---------------------------------------|
| **GET**     | `/task/milestones/`                                    | Get a list of tags with total and completed task counts and tags rewards | None         | Tags data with task completion info   |



