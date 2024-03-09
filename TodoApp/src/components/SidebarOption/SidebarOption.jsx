import React from "react";
import classes from "./SidebarOption.module.scss";
import { useTodos } from "../../context/todoCtx";
import { IconButton, Box, useToast } from "@chakra-ui/react";
import { AiOutlineDelete } from "react-icons/ai";
import axios from "axios";

const SidebarOption = ({ category, selectCategory, selectedCategory }) => {
  const toast = useToast();
  const numberOfTask = category.tasks.length;
  const name = category.name;
  const id = category.id;
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

  const delete_category = () => {
    setIsLoading(true);
    axios
      .delete(`http://localhost:8000/categories/${id}`)
      .then((response) => {
        const {
          data: {
            message,
            catégorie: { name },
          },
        } = response;
        getAllTodos();
        getAllCategories();
        selectCategory({ id: "1" });
        toast({
          position: "top-left",
          duration: "2000",
          status: "success",
          title: message,
          description: name,
        });
      })
      .catch((error) => {
        console.error(error);
        dispatchCategories({ type: "error" });
      })
      .finally(() => setIsLoading(false));
  };

  return (
    <li
      className={`${classes.sidebarOption} ${
        id === selectedCategory.id ? classes.isSelected : ""
      }`}
      onClick={() => selectCategory({ id: id, name: name })}
    >
      <div>
        <p>{name}</p>
      </div>
      <Box as="p" ml="auto" mr="8px">
        {numberOfTask}
      </Box>
      {id === selectedCategory.id && (
        <IconButton
          icon={<AiOutlineDelete />}
          border="none"
          h="100%"
          backgroundColor="inherit"
          cursor="pointer"
          onClick={delete_category}
        />
      )}
    </li>
  );
};

export default SidebarOption;
