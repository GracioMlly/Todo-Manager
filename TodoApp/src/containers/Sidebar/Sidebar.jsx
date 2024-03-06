import React from "react";
import classes from "./Sidebar.module.scss";
import SidebarOption from "../../components/SidebarOption/SidebarOption";
import homeIcon from "../../assets/images/home_icon.png";
import { useTodos } from "../../context/todoCtx";
import { Input, IconButton } from "@chakra-ui/react";
import AddCategory from "../../components/AddCategory/AddCategory";
const Sidebar = () => {
  const categories = useTodos().at(5);

  return (
    <div className={classes.sidebar}>
      <p className="emphasize">Catégories</p>
      <ul>
        {categories.map((category) => (
          <SidebarOption
            key={category.id}
            category={category}
          />
        ))}
      </ul>
      <AddCategory />
    </div>
  );
};

export default Sidebar;
