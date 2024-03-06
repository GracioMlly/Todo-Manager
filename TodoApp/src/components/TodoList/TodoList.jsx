import React from "react";
import classes from "./TodoList.module.scss";
import Todo from "../Todo/Todo";
import { useTodos } from "../../context/todoCtx";

const TodoList = () => {
  const [todos] = useTodos();

  return (
    <ul className={classes.todoList}>
      {todos.map((todo) => (
        <Todo key={todo.id} todo={todo} />
      ))}
    </ul>
  );
};

export default TodoList;
