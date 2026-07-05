todos = []
done = []


def add_todos(new_todos: list) -> str:
    todos.extend(new_todos)
    delim = "\n - "
    print(f"\nTodo list:{delim.join(todos)}")
    return f"Added {len(new_todos)} to todo list. Now have {len(todos)} todos."


def mark_todo_done(todo: str) -> str:
    if todo in todos:
        todos.remove(todo)
        done.append(todo)
        return f"Marked the following todo as done:\n {todo}"
    else:
        return f"Todo list doesn't include todo:\n {todo}"


def check_todos() -> str:
    if todos:
        return str(todos)
    return "The todo list is empty."


def check_done_todos() -> str:
    if done:
        return str(done)
    return "No tasks have been marked done."


def print_status():
    print("\n" + "-" * 40)
    print("📋 TODO LIST STATUS")
    print("-" * 40)
    print(f"\n⏳ Pending: {check_todos()}")
    print(f"\n✅ Done: {check_done_todos()}")