import React from "react";
import classes from "./Header.module.scss";
import { useTodos } from "../../context/todoCtx";
import { Spinner, Box } from "@chakra-ui/react";
import MenuHeader from "../MenuHeader/MenuHeader";

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
      <div>
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

      <MenuHeader />
    </div>
  );
};

export default Header;
