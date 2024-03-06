import React, { useRef } from "react";
import {
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  IconButton,
} from "@chakra-ui/react";
import { CgGoogleTasks } from "react-icons/cg";
import AddTodo from "../AddTodo/AddTodo";

const AddTodoForm = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <>
      <IconButton
        onClick={onOpen}
        as="button"
        icon={<CgGoogleTasks />}
        border={"none"}
        w={"60px"}
        h={"60px"}
        borderRadius={"50%"}
        cursor={"pointer"}
        bgColor="black"
        color="white"
        _hover={{
          backgroundColor: "white",
          color: "black",
          boxShadow: "rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px",
        }}
      />
      <Drawer isOpen={isOpen} placement="right" onClose={onClose} size="sm">
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton border={"none"} />
          <DrawerHeader fontWeight={"400"}>Créer votre tâche</DrawerHeader>

          <DrawerBody><AddTodo /></DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
};

export default AddTodoForm;
