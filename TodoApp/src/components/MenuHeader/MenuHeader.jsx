import React, { useState } from "react";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuItemOption,
  MenuGroup,
  MenuOptionGroup,
  MenuDivider,
  Button,
  Box,
} from "@chakra-ui/react";
import axios from "axios";
import { MdKeyboardArrowDown } from "react-icons/md";
import { useTodos } from "../../context/todoCtx";

const MenuHeader = () => {
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

  const [filterType, setFilterType] = useState("Défaut");

  const filterTodo = async (filtering = "") => {
    try {
      setIsLoading(true);
      const response = await axios.get(
        `http://localhost:8000/tasks${filtering}`
      );
      const data = response.data;
      dispatchTodos({ type: "getAllTodos", payload: data });
    } catch (error) {
      console.error(error);
      dispatchTodos({ type: "error" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Menu>
      <MenuButton
        ml={[0, 0, "auto", "auto"]}
        as={Button}
        rightIcon={<MdKeyboardArrowDown />}
        bgColor="#fff"
        _hover=""
        _active={{ color: "white", bgColor: "black" }}
      >
        Filtrer par
      </MenuButton>
      <MenuList>
        <MenuItem onClick={() => filterTodo()}>Défaut</MenuItem>
        <MenuItem onClick={() => filterTodo("?filter=date")}>
          Date de priorité
        </MenuItem>
        <MenuItem onClick={() => filterTodo("?filter=order")}>
          Ordre de priorité
        </MenuItem>
      </MenuList>
    </Menu>
  );
};

export default MenuHeader;
