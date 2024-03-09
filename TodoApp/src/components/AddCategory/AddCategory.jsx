import React, { useState } from "react";
import {
  Input,
  InputLeftElement,
  InputGroup,
  Icon,
  InputRightElement,
  IconButton,
  useToast,
} from "@chakra-ui/react";
import { AiOutlinePlus } from "react-icons/ai";
import { RiSendPlaneLine } from "react-icons/ri";
import Category from "../../classes/Category/Category";
import { useTodos } from "../../context/todoCtx";
import axios from "axios";

const AddCategory = () => {
  const toast = useToast();
  const [, , , , setIsLoading, , , getAllCategories] = useTodos();
  const [categoryName, setCategoryName] = useState("");

  const create_category = (event) => {
    event.preventDefault();

    if (categoryName) {
      setIsLoading(true);
      const category = new Category(categoryName);
      axios
        .post("http://localhost:8000/categories", category)
        .then((response) => {
          const {
            data: {
              message,
              catégorie: { name },
            },
          } = response;
          setCategoryName("");
          getAllCategories();
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
        })
        .finally(() => setIsLoading(false));
    }
  };

  return (
    <form onSubmit={create_category}>
      <InputGroup>
        <InputLeftElement h="100%">
          <Icon as={AiOutlinePlus} />
        </InputLeftElement>
        <Input
          placeholder="Créer une catégorie"
          variant="filled"
          borderRadius="999rem"
          height="48px"
          _focus={{
            border: "",
          }}
          value={categoryName}
          onChange={(e) => setCategoryName(e.target.value)}
        />
        <InputRightElement h="100%" pr="16px">
          <IconButton
            as="button"
            type="submit"
            icon={<RiSendPlaneLine />}
            border="none"
            boxSize="36px"
            borderRadius="50%"
            bgColor="inherit"
            _hover={{ bgColor: "black", color: "white" }}
            cursor="pointer"
          />
        </InputRightElement>
      </InputGroup>
    </form>
  );
};

export default AddCategory;
