import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
  const [users, setUsers] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(""); // For adding recipes
  const [newUserName, setNewUserName] = useState("");
  const [newUserEmail, setNewUserEmail] = useState("");
  const [recipeTitle, setRecipeTitle] = useState("");
  const [recipeDescription, setRecipeDescription] = useState("");

  const API_URL = "http://127.0.0.1:8000";

  // Fetch users
  const fetchUsers = async () => {
    try {
      const res = await axios.get(`${API_URL}/users`);
      setUsers(res.data);
      if (res.data.length > 0) setSelectedUserId(res.data[0].id);
    } catch (err) {
      console.error("Failed to fetch users:", err);
    }
  };

  // Fetch recipes
  const fetchRecipes = async () => {
    try {
      const res = await axios.get(`${API_URL}/recipes`);
      setRecipes(res.data);
    } catch (err) {
      console.error("Failed to fetch recipes:", err);
    }
  };

  useEffect(() => {
    fetchUsers();
    fetchRecipes();
  }, []);

  // Add user
  const handleAddUser = async () => {
    if (!newUserName || !newUserEmail) {
      alert("Please enter user name and email");
      return;
    }

    try {
      const res = await axios.post(`${API_URL}/users`, {
        name: newUserName,
        email: newUserEmail,
        password: "123456", // default password
      });
      setUsers([...users, res.data]);
      setNewUserName("");
      setNewUserEmail("");
      setSelectedUserId(res.data.id);
    } catch (err) {
      console.error("Failed to add user:", err);
      alert("Failed to add user. Check console for details.");
    }
  };

  // Add recipe
  const handleAddRecipe = async () => {
    if (!recipeTitle || !selectedUserId) {
      alert("Please enter a title and select a user");
      return;
    }

    try {
      const res = await axios.post(`${API_URL}/recipes`, {
        title: recipeTitle,
        description: recipeDescription,
        user_id: selectedUserId,
      });
      setRecipes([...recipes, res.data]);
      setRecipeTitle("");
      setRecipeDescription("");
    } catch (err) {
      console.error("Failed to add recipe:", err);
      alert("Failed to add recipe. Check console for details.");
    }
  };

  return (
    <div style={{ maxWidth: "700px", margin: "0 auto", padding: "20px", fontFamily: "Arial" }}>
      <h1>Recipe Manager 🍳</h1>

      {/* Add User */}
      <div style={{ marginBottom: "20px" }}>
        <h2>Add User</h2>
        <input
          type="text"
          placeholder="Name"
          value={newUserName}
          onChange={(e) => setNewUserName(e.target.value)}
          style={{ width: "48%", padding: "8px", marginRight: "4%" }}
        />
        <input
          type="email"
          placeholder="Email"
          value={newUserEmail}
          onChange={(e) => setNewUserEmail(e.target.value)}
          style={{ width: "48%", padding: "8px" }}
        />
        <button onClick={handleAddUser} style={{ marginTop: "10px", padding: "10px 20px" }}>
          Add User
        </button>
      </div>

      {/* Add Recipe */}
      <div style={{ marginBottom: "20px" }}>
        <h2>Add Recipe</h2>
        <select
          value={selectedUserId}
          onChange={(e) => setSelectedUserId(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        >
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name} ({user.email})
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Recipe Title"
          value={recipeTitle}
          onChange={(e) => setRecipeTitle(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        />
        <textarea
          placeholder="Description"
          value={recipeDescription}
          onChange={(e) => setRecipeDescription(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        />
        <button onClick={handleAddRecipe} style={{ padding: "10px 20px" }}>
          Add Recipe
        </button>
      </div>

      {/* Recipe List */}
      <div>
        <h2>Recipes List:</h2>
        {recipes.length === 0 ? (
          <p>No recipes found.</p>
        ) : (
          <ul>
            {recipes.map((recipe) => (
              <li key={recipe.id}>
                <strong>{recipe.title}</strong> - {recipe.description || "No description"} (User ID: {recipe.user_id})
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default App;
