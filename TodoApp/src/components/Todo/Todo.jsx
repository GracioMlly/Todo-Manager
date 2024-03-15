import React, { useState } from "react";
import classes from "./Todo.module.scss";
import { AiOutlineDelete } from "react-icons/ai";
import { HiOutlinePencilSquare } from "react-icons/hi2";
import { AiOutlinePlus } from "react-icons/ai";
import { RiSendPlaneLine } from "react-icons/ri";
import { useTodos } from "../../context/todoCtx";
import axios from "axios";
import {
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  Select,
  Input,
  Badge,
  useToast,
} from "@chakra-ui/react";

const Todo = ({ todo }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const deadline = new Date(todo.deadline).toLocaleDateString();
  const toast = useToast();
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

  const handleClick = () => {
    onOpen();
    setFormState(todo);
  };

  const updateTodo = (event) => {
    event.preventDefault();
    setIsLoading(true);
    const data = structuredClone(formState);
    axios
      .put(`http://localhost:8000/tasks/${todo.id}`, data)
      .then((response) => {
        const {
          data: {
            message,
            tâche: { description },
          },
        } = response;
        getAllTodos();
        getAllCategories();
        toast({
          position: "top-left",
          duration: "2000",
          title: message,
          description: description,
        });
      })
      .catch((error) => {
        console.error(error);
        dispatchTodos({ type: "error" });
      })
      .finally(() => setIsLoading(false));
  };

  const deleteTodo = () => {
    setIsLoading(true);
    axios
      .delete(`http://localhost:8000/tasks/${todo.id}`)
      .then((response) => {
        const {
          data: {
            message,
            tâche: { description },
          },
        } = response;
        getAllTodos();
        getAllCategories();
        toast({
          position: "top-left",
          duration: "2000",
          title: message,
          description: description,
        });
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
        dispatchTodos({ type: "error" });
      });
  };

  return (
    <>
      <li className={classes.todo}>
        <p>{todo.description}</p>

        <div>
          <Badge
            as="p"
            display="flex"
            justifyContent="center"
            alignItems="center"
            fontSize="12px"
          >
            {todo.category}
          </Badge>
          <Badge
            as="p"
            display="flex"
            justifyContent="center"
            alignItems="center"
            fontSize="12px"
            flex="0 1 20px"
          >
            {todo.priority}
          </Badge>
          <Badge
            as="p"
            display="flex"
            justifyContent="center"
            alignItems="center"
            fontSize="12px"
            flex="0 1 80px"
          >
            {deadline}
          </Badge>
          <button className={classes.modify} onClick={handleClick}>
            <HiOutlinePencilSquare />
          </button>
          <button onClick={deleteTodo} className={classes.delete}>
            <AiOutlineDelete />
          </button>
        </div>
      </li>

      <Drawer isOpen={isOpen} placement="right" onClose={onClose} size="sm">
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton border={"none"} />
          <DrawerHeader fontWeight={"400"}>Modifier votre tâche</DrawerHeader>
          <DrawerBody>
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
            <form className={classes.addTodo} onSubmit={updateTodo}>
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
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
};

export default Todo;
