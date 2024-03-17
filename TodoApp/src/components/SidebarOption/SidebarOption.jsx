import React from "react";
import classes from "./SidebarOption.module.scss";
import { useTodos } from "../../context/todoCtx";
import { IconButton, Box, useToast, useDisclosure } from "@chakra-ui/react";
import { AiOutlineDelete } from "react-icons/ai";
import { MdSubject } from "react-icons/md";
import axios from "axios";
import AddSubcategoryModal from "../AddSubcategoryModal/AddSubcategoryModal";

const SidebarOption = ({ category, selectCategory, selectedCategory }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
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
      onClick={() => selectCategory(category)}
    >
      <div>
        <p>{name}</p>
      </div>
      <Box as="p" ml="auto" mr="8px">
        {numberOfTask}
      </Box>
      {id === selectedCategory.id && (
        <>
          <AddSubcategoryModal
            isOpen={isOpen}
            onClose={onClose}
            categoryId={id}
          />
          <IconButton
            icon={<MdSubject />}
            border="none"
            w="40px"
            h="40px"
            _hover={{
              backgroundColor: "#fff",
            }}
            borderRadius="50%"
            backgroundColor="inherit"
            cursor="pointer"
            onClick={onOpen}
          />
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
            onClick={delete_category}
          />
        </>
      )}
    </li>
  );
};

export default SidebarOption;
