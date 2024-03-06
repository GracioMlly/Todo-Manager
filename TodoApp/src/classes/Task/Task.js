import { v4 as uuid4 } from "uuid";
class Task {
  constructor(description, priority, deadline, category = "") {
    this.id = uuid4();
    this.description = description;
    this.priority = Number(priority);
    this.deadline = deadline;
    this.category = category;
  }
}

export default Task;