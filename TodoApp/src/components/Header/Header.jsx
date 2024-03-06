import React from "react";
import classes from "./Header.module.scss";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { useTodos } from "../../context/todoCtx";
import { Spinner } from "@chakra-ui/react";

const Header = () => {
  const options = {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  };
  const date = new Date().toLocaleDateString(undefined, options);

  const [, , , isLoading] = useTodos();

  return (
    <div className={classes.header}>
      <p className="emphasize">Bienvenue, Utilisateur!👋</p>
      <p>Aujourd'hui, {date}</p>

      {isLoading && (
        <Spinner
          as="svg"
          thickness="2px"
          speed="0.75s"
          emptyColor="gray.200"
          color="black"
          boxSize="18px"
        />
      )}
    </div>
  );
};

export default Header;
