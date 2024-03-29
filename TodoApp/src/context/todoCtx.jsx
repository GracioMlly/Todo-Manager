import {
  createContext,
  useContext,
  useEffect,
  useReducer,
  useState,
} from "react";
import axios from "axios";
import Category from "../classes/Category/Category";

const todoCtx = createContext();

const todosReducer = (state, action) => {
  const { type, payload } = action;

  switch (type) {
    case "getAllTodos": {
      return payload;
    }

    default: {
      return state;
    }
  }
};

const categoriesReducer = (state, action) => {
  const { type, payload } = action;

  switch (type) {
    case "getAllCategories": {
      return payload;
    }

    default: {
      return state;
    }
  }
};

const TodoProvider = ({ children }) => {
  const [todos, dispatchTodos] = useReducer(todosReducer, []);
  const [categories, dispatchCategories] = useReducer(categoriesReducer, []);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState({
    id: "1",
    name: "",
  });
  const [selectedSubcat, setSelectedSubcat] = useState(new Category(""));

  const getAllTodos = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get("http://localhost:8000/tasks");
      const data = response.data;
      dispatchTodos({ type: "getAllTodos", payload: data });
    } catch (error) {
      console.error(error);
      dispatchTodos({ type: "error" });
    } finally {
      setIsLoading(false);
    }
  };

  const getAllCategories = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get("http://localhost:8000/categories");
      const data = response.data;
      dispatchCategories({ type: "getAllCategories", payload: data });
    } catch (error) {
      dispatchCategories({ type: "error" });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    getAllTodos();
    getAllCategories();
  }, []);
  // console.log(`todos :`, todos);
  // console.log(`categories :`, categories);

  return (
    <todoCtx.Provider
      value={{
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
      }}
    >
      {children}
    </todoCtx.Provider>
  );
};

export const useTodos = () => {
  const {
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
  } = useContext(todoCtx);
  return [
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
  ];
};

export default TodoProvider;
