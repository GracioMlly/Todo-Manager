import React, { useState } from "react";
import classes from "./Sidebar.module.scss";
import SidebarOption from "../../components/SidebarOption/SidebarOption";
import { useTodos } from "../../context/todoCtx";
import AddCategory from "../../components/AddCategory/AddCategory";
import SidebarAllCategory from "../../components/SidebarAllCategory/SidebarAllCategory";
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
  ] = useTodos();
  const [selectedCategoryId, setSelectedCategoryId] = useState("1");

  const selectCategory = (cat) => {
    setSelectedCategory({ id: cat.id, name: cat.name });
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
    </div>
  );
};

export default Sidebar;
