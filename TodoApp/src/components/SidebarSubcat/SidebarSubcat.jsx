import React from "react";
import classes from "./SidebarOption.module.scss";
import { useTodos } from "../../context/todoCtx";
import { IconButton, Box, useToast } from "@chakra-ui/react";
import { AiOutlineDelete } from "react-icons/ai";
import axios from "axios";

const SidebarSubcat = ({ category, selectCategory, selectedSubCategory }) => {
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
    selectedCategory,
    setSelectedCategory,
    selectedSubcat,
    setSelectedSubcat,
  ] = useTodos();

  const delete_subcategory = () => {
    setIsLoading(true);
    axios
      .delete(`http://localhost:8000/categories/${selectedCategory.id}/${id}`)
      .then((response) => {
        const {
          data: {
            message,
            "sous-catégorie": { name },
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
        id === selectedSubCategory.id ? classes.isSelected : ""
      }`}
      onClick={() => selectCategory(category, true)}
    >
      <div>
        <p>{name}</p>
      </div>
      <Box as="p" ml="auto" mr="8px">
        {numberOfTask}
      </Box>
      {id === selectedSubCategory.id && (
        <>
          <IconButton
            icon={<AiOutlineDelete />}
            border="none"
            w="40px"
            h="40px"
            _hover={{
              backgroundColor: "#fff",
            }}
            borderRadius="50%"
            backgroundColor="inherit"
            cursor="pointer"
            onClick={delete_subcategory}
          />
        </>
      )}
    </li>
  );
};

export default SidebarSubcat;
