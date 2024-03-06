import React from "react";
import classes from "./SidebarOption.module.scss";
import { useTodos } from "../../context/todoCtx";

const SidebarOption = ({ category}) => {
  const numberOfTask = category.tasks.length
  const name = category.name

  return (
    <li className={classes.sidebarOption}>
      <div>
        {/* <img src={""} alt="#" /> */}
        <p>{name}</p>
      </div>
      <p>{numberOfTask}</p>
    </li>
  );
};

export default SidebarOption;
