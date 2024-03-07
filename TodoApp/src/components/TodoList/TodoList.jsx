import React, { useEffect } from "react";
import classes from "./TodoList.module.scss";
import Todo from "../Todo/Todo";
import { useTodos } from "../../context/todoCtx";

const TodoList = () => {
  const [
    todos,
    dispatchTodos,
    getAllTodos,
    isLoading,
    setIsLoading,
    categories,
    dispatchCategories,
    getAllCategories,
    selectedCategory,
    setSelectedCategory,
  ] = useTodos();

  let filteredTodos = [];
  if (selectedCategory.id == "1") {
    filteredTodos = structuredClone(todos);
  } else {
    const temp = structuredClone(todos);
    filteredTodos = temp.filter(
      (todo) => todo.category === selectedCategory.name
    );
  }

  return (
    <ul className={classes.todoList}>
      {filteredTodos.map((todo) => (
        <Todo key={todo.id} todo={todo} />
      ))}
    </ul>
  );
};

export default TodoList;
