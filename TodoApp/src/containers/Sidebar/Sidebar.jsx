import React, { useState } from "react";
import classes from "./Sidebar.module.scss";
import SidebarOption from "../../components/SidebarOption/SidebarOption";
import { useTodos } from "../../context/todoCtx";
import AddCategory from "../../components/AddCategory/AddCategory";
import SidebarAllCategory from "../../components/SidebarAllCategory/SidebarAllCategory";
import { Box } from "@chakra-ui/react";
import "../../components/SidebarSubcat/SidebarSubcat";
import SidebarSubcat from "../../components/SidebarSubcat/SidebarSubcat";
const Sidebar = () => {
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
    selectedSubcat,
    setSelectedSubcat,
  ] = useTodos();

  const subcategories = selectedCategory.subcategories ?? [];

  const selectCategory = (cat, isSelectingSubcat = false) => {
    if (!isSelectingSubcat) {
      setSelectedCategory(cat);
      setSelectedSubcat({ id: "", name: "" });
    } else {
      setSelectedSubcat(cat);
    }
  };

  return (
    <div className={classes.sidebar}>
      <p className="emphasize">Catégories</p>
      <ul>
        <SidebarAllCategory
          selectCategory={selectCategory}
          selectedCategory={selectedCategory}
        />
        {categories.map((category) => (
          <SidebarOption
            key={category.id}
            category={category}
            selectCategory={selectCategory}
            selectedCategory={selectedCategory}
          />
        ))}
      </ul>
      <AddCategory />
      <p className="emphasize">Sous-catégories</p>
      <Box
        as="ul"
        flex={"1 1 auto"}
        overflowY={"auto"}
        maxH={"100px"}
        display={"flex"}
        flexDirection={"column"}
        rowGap={"18px"}
        paddingInlineEnd={"12px"}
      >
        {subcategories.map((category) => (
          <SidebarSubcat
            key={category.id}
            category={category}
            selectCategory={selectCategory}
            selectedSubCategory={selectedSubcat}
          />
        ))}
      </Box>
    </div>
  );
};

export default Sidebar;
