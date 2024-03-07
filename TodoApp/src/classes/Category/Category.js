import { v4 as uuid4 } from "uuid";
class Category {
    constructor(name){
        this.id = uuid4()
        this.name = name
        this.tasks = []
    }
}

export default Category