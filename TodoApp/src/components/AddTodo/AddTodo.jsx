import React, { useState } from "react";
import classes from "./AddTodo.module.scss";
import { AiOutlinePlus } from "react-icons/ai";
import { RiSendPlaneLine } from "react-icons/ri";
import { useTodos } from "../../context/todoCtx";
import Task from "../../classes/Task/Task";
import axios from "axios";
import { Select, Input } from "@chakra-ui/react";

const AddTodo = () => {
  const [
    todos,
    dispatchTodos,
    getAllTodos,
    isLoading,
    setIsLoading,
    categories,
    dispatchCategories,
    getAllCategories,
  ] = useTodos();

  const [formState, setFormState] = useState({
    id: "",
    description: "",
    priority: "",
    deadline: "",
    category: "",
  });

  const handleChange = (event) => {
    setFormState((prevState) => {
      return {
        ...prevState,
        [event.target.name]: event.target.value,
      };
    });
  };

  const createTodo = (event) => {
    event.preventDefault();
    if (formState.priority && formState.deadline && formState.description) {
      setIsLoading(true);
      const { description, priority, deadline, category } = formState;
      const todo = new Task(description, priority, deadline, category);
      console.log(todo);
      axios
        .post("http://localhost:8000/tasks", todo)
        .then(() => {
          getAllTodos();
          getAllCategories();
          setFormState({
            id: "",
            description: "",
            priority: "",
            deadline: "",
            category: "",
          });
        })
        .catch((error) => {
          console.error(error);
          setIsLoading(false);
          dispatchTodos({ type: "error" });
        });
    }
  };

  return (
    <>
      <Select
        variant="filled"
        cursor="pointer"
        placeholder="Catégorie"
        name="category"
        value={formState.category}
        onChange={handleChange}
      >
        {categories.map((category) => (
          <option key={category.id} value={category.name}>
            {category.name}
          </option>
        ))}
      </Select>

      <Select
        placeholder="Priorité"
        variant="filled"
        marginTop="40px"
        cursor="pointer"
        name="priority"
        value={formState.priority}
        onChange={handleChange}
      >
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
      </Select>
      <Input
        placeholder="Basic usage"
        variant="filled"
        marginTop="40px"
        border={"none"}
        type="date"
        _hover={{
          border: "1px solid blue.300",
        }}
        cursor="pointer"
        name="deadline"
        value={formState.deadline}
        onChange={handleChange}
      />
      <form className={classes.addTodo} onSubmit={createTodo}>
        <div>
          <AiOutlinePlus />
          <input
            autoComplete="off"
            type="text"
            placeholder="Créer une nouvelle tâche"
            name="description"
            value={formState.description}
            onChange={handleChange}
          />
        </div>

        <button>
          <RiSendPlaneLine />
        </button>
      </form>
    </>
  );
};

export default AddTodo;
