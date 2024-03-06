import React from "react";
import {
  Input,
  InputLeftElement,
  InputGroup,
  Box,
  Icon,
  InputRightElement,
} from "@chakra-ui/react";
import { AiOutlinePlus } from "react-icons/ai";
import { RiSendPlaneLine } from "react-icons/ri";
const AddCategory = () => {
  const create_category = (event) => {
    event.preventDefault();
  };
  return (
    <form onSubmit={create_category}>
      <InputGroup display="flex" alignItems="center">
        <InputLeftElement>
          
        </InputLeftElement>
        <Input
          placeholder="Créer une catégorie"
          variant="filled"
          borderRadius="999rem"
          height="48px"
          _focus={{
            border: "",
          }}
        />
        <InputRightElement>
          <RiSendPlaneLine />
        </InputRightElement>
      </InputGroup>
    </form>
  );
};

export default AddCategory;
