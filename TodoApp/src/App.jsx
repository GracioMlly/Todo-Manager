import React from "react";
import "./styles/App.scss";
import "./styles/reset.scss";
import Sidebar from "./containers/Sidebar/Sidebar";
import Home from "./containers/Home/Home";
import TodoProvider from "./context/todoCtx";
import AddTodoForm from "./components/AddTodoForm/AddTodoForm";

const App = () => {
  return (
    <>
      <TodoProvider>
        <Sidebar />
        <Home />
      </TodoProvider>
    </>
  );
};

export default App;
