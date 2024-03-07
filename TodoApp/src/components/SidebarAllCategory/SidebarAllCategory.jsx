import React from "react";
import { CgGoogleTasks } from "react-icons/cg";
import { Box, Icon } from "@chakra-ui/react";
import classes from "./SidebarAllCategory.module.scss";
import { useTodos } from "../../context/todoCtx";

const SidebarAllCategory = ({ selectedCategory, selectCategory }) => {
  const id = "1";
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
  const numberOfTask = todos.length;
  return (
    <Box
      as="li"
      listStyleType="none"
      padding="12px"
      h="48px"
      borderRadius="8px"
      cursor="pointer"
      display="flex"
      alignItems="center"
      columnGap="12px"
      className={`${id === selectedCategory.id ? classes.isSelected : ""}`}
      onClick={() => selectCategory({ id: "1" })}
    >
      <Icon as={CgGoogleTasks} />
      <p>Toutes les tâches</p>
      <Box
        as="p"
        ml="auto"
        fontSize={["0.694rem", "0.79rem"]}
        borderRadius="50%"
        mr="8px"
        w="25px"
        h="25px"
        display="flex"
        justifyContent="center"
        alignItems="center"
        textAlign="center"
        bgColor="#f5f5f5"
      >
        {numberOfTask}
      </Box>
    </Box>
  );
};

export default SidebarAllCategory;
