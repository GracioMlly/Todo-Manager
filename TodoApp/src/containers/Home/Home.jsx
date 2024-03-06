import React from "react";
import classes from "./Home.module.scss";
import Header from "../../components/Header/Header";
import TodoList from "../../components/TodoList/TodoList";
import AddTodo from "../../components/AddTodo/AddTodo";
import AddTodoForm from "../../components/AddTodoForm/AddTodoForm";

const Home = () => {
  return <div className={classes.home}>
  <Header />
  <TodoList />
  <AddTodoForm />
  </div>;
};

export default Home;
