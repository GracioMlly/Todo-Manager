import React, { useState } from "react";
import {
  Box,
  Input,
  InputLeftElement,
  InputGroup,
  Icon,
  InputRightElement,
  IconButton,
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useToast,
} from "@chakra-ui/react";
import { AiOutlinePlus } from "react-icons/ai";
import { RiSendPlaneLine } from "react-icons/ri";
import { useTodos } from "../../context/todoCtx";
import Category from "../../classes/Category/Category";
import axios from "axios";

const AddSubcategoryModal = ({ isOpen, onClose, categoryId }) => {
  const toast = useToast();
  const [, , , , setIsLoading, , , getAllCategories] = useTodos();
  const [subcategoryName, setSubcategoryName] = useState("");

  const create_subcategory = (event) => {
    event.preventDefault();
    console.log(categoryId)
    if (subcategoryName) {
      setIsLoading(true);
      const subcategory = new Category(subcategoryName);
      axios
        .post(`http://localhost:8000/categories/${categoryId}`, subcategory)
        .then((response) => {
          const {
            data: {
              message,
              "sous-catégorie": { name },
            },
          } = response;
          setSubcategoryName("");
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
    <>
      <Modal isOpen={isOpen} onClose={onClose} isCentered>
        <ModalOverlay />
        <ModalContent bgColor="#f5f5f5">
          <ModalHeader
            fontSize={["1rem", "1rem", "1rem", "1rem", "1rem", "1.5rem"]}
          >
            Créer une sous-catégorie
          </ModalHeader>
          <ModalCloseButton border="none" cursor={"pointer"} />
          <ModalBody justifyContent={"center"}>
            <InputGroup as="form" onSubmit={create_subcategory}>
              <InputLeftElement h="100%">
                <Icon as={AiOutlinePlus} />
              </InputLeftElement>
              <Input
                placeholder="Créer une sous-catégorie"
                variant="filled"
                borderRadius="999rem"
                height="48px"
                _focus={{
                  border: "",
                }}
                value={subcategoryName}
                onChange={(e) => setSubcategoryName(e.target.value)}
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
          </ModalBody>

          <ModalFooter>
            <Button
              border="none"
              bgColor="gray.600"
              color={"white"}
              _hover={{ bgColor: "gray.700" }}
              cursor={"pointer"}
              onClick={onClose}
            >
              Fermer
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default AddSubcategoryModal;
